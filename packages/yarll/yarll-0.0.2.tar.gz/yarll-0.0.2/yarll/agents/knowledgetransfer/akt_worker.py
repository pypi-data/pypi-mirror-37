#!/usr/bin/env python
# -*- coding: utf8 -*-

import os
import queue
import argparse
import time
import tensorflow as tf
import numpy as np

tf.logging.set_verbosity(tf.logging.ERROR)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '5'

from yarll.environment.registration import make
from yarll.misc.network_ops import factorized_conv2d, flatten, normalized_columns_initializer, create_sync_net_op, add_initializers
from yarll.misc.utils import discount_rewards, FastSaver, load, json_to_dict, cluster_spec
from yarll.agents.actorcritic.actor_critic import actor_critic_discrete_loss
from yarll.agents.actorcritic.a3c_worker import RunnerThread


class AKTTask(object):
    """Asynchronous knowledge transfer learner thread. Used to learn using one specific variation of a task."""

    def __init__(self, env, task_id, target_task, cluster, monitor_path, config, video=False):
        super(AKTTask, self).__init__()
        self.env = env
        self.task_id = task_id
        self.target_task = target_task
        self.monitor_path = monitor_path
        self.config = config
        self.add_accum_grad = None  # To be filled in later

        # Only used (and overwritten) by agents that use an RNN
        self.initial_features = None

        self.first_source_or_target_task = self.task_id == 0 or (
            self.target_task and self.task_id == self.config["n_tasks"] - self.config["n_target_tasks"])

        state_shape = env.observation_space.shape
        self.states = tf.placeholder(tf.float32, [None] + list(state_shape), name="states")
        self.adv = tf.placeholder(tf.float32, name="advantage")
        self.actions_taken = tf.placeholder(tf.float32, name="actions_taken")
        self.r = tf.placeholder(tf.float32, [None], name="r")
        worker_device = "/job:worker/task:{}/cpu:0".format(task_id)
        # Global network
        shared_device = tf.train.replica_device_setter(1, worker_device=worker_device)
        with tf.device(shared_device):
            with tf.variable_scope("global"):
                self.build_shared_network()
                self._global_step = tf.get_variable(
                    "global_step",
                    [],
                    tf.int32,
                    initializer=tf.constant_initializer(0, dtype=tf.int32),
                    trainable=False)
                self.global_shared_vars = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES,
                                                            tf.get_variable_scope().name)

        with tf.device(worker_device):
            with tf.variable_scope("local"):
                with tf.variable_scope("shared"):
                    # Part of the network that is shared between all tasks (by copying from global)
                    knowledge_bases = self.build_shared_network()
                    self.local_shared_vars = tf.get_collection(
                        tf.GraphKeys.TRAINABLE_VARIABLES, tf.get_variable_scope().name)
                with tf.variable_scope("task"):
                    # Part of the network that is specific for the task and not shared
                    self.action, self.value, entropy, self.loss, \
                    self.losses, self.sparse_representations = self.build_task_network(knowledge_bases)
                    # Add L1 loss for sparse representations weights of source tasks
                    if not self.target_task and self.config["l1_coef"] > 0.0:
                        regularizer = tf.contrib.layers.l1_regularizer(self.config["l1_coef"])
                        self.l1_loss = 0
                        for w in self.sparse_representations:
                            self.l1_loss += regularizer(w)
                        self.loss += self.l1_loss
                        self.losses[-1] = self.loss
                    self.task_vars = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, tf.get_variable_scope().name)

                with tf.variable_scope("optimizer"):
                    optimizer = tf.train.AdamOptimizer(self.config["learning_rate"], name="optim")
                    grad_vars = (self.local_shared_vars if not(target_task) else []) + self.task_vars
                    grads = tf.gradients(self.loss, grad_vars)
                    grads, _ = tf.clip_by_global_norm(grads, self.config["gradient_clip_value"])

                    # Apply gradients to the weights of the master network
                    apply_vars = (self.global_shared_vars if not(target_task) else []) + self.task_vars
                    apply_grads = optimizer.apply_gradients(zip(grads, apply_vars))
                    self.optimizer_vars = tf.get_collection(
                        tf.GraphKeys.GLOBAL_VARIABLES, tf.get_variable_scope().name)

            self.n_steps = tf.shape(self.states)[0]
            inc_step = self._global_step.assign_add(self.n_steps)

            self.train_op = tf.group(apply_grads, inc_step, name="train")

            self.sync_net = create_sync_net_op(self.global_shared_vars, self.local_shared_vars)

            n_steps = tf.to_float(self.n_steps)
            actor_loss_summary = tf.summary.scalar("model/actor_loss", self.losses[0] / n_steps)
            critic_loss_summary = tf.summary.scalar("model/critic_loss", self.losses[1] / n_steps)
            id_loss_summary = tf.summary.scalar("model/id_loss", self.losses[2])
            entropy_summary = tf.summary.scalar("model/entropy", -tf.reduce_mean(entropy))
            mean, std = tf.nn.moments(self.value, axes=[0])
            mean_q_summary = tf.summary.scalar("model/q/mean", mean)
            std_q_summary = tf.summary.scalar("model/q/std", std)
            loss_summary = tf.summary.scalar("model/loss", self.loss / n_steps)
            summary_grad_norm = tf.summary.scalar("model/grad_global_norm", tf.global_norm(grads))
            summary_var_norm = tf.summary.scalar("model/var_global_norm",
                                                 tf.global_norm(self.local_shared_vars + self.task_vars))
            summaries = [actor_loss_summary, critic_loss_summary, id_loss_summary, loss_summary,
                         entropy_summary,
                         mean_q_summary, std_q_summary,
                         summary_grad_norm, summary_var_norm]
            if not self.target_task and self.config["l1_coef"] > 0.0:
                l1_loss_summary = tf.summary.scalar("model/l1_loss", self.l1_loss)
                summaries.append(l1_loss_summary)
            self.summary_op = tf.summary.merge(summaries)

            if self.first_source_or_target_task:
                histogram_summaries = []
                for v in self.global_shared_vars:
                    histogram_summaries.append(tf.summary.histogram(v.name, v))
                for v in self.task_vars:
                    histogram_summaries.append(tf.summary.histogram("task{}/{}".format(self.task_id, v.name), v))
                self.histogram_summary_op = tf.summary.merge(histogram_summaries)

        self.runner = RunnerThread(self.env, self, self.config["n_local_steps"], task_id == 0 and video)

        variables_to_save = self.global_shared_vars + self.task_vars
        init_op = tf.variables_initializer(self.global_shared_vars + [self._global_step])
        init_all_op = tf.global_variables_initializer()
        saver = FastSaver(variables_to_save)

        # Write the summary of each task in a different directory
        self.writer = tf.summary.FileWriter(os.path.join(monitor_path, "task{}".format(self.task_id)))

        self.server = tf.train.Server(
            cluster,
            job_name="worker",
            task_index=task_id,
            config=tf.ConfigProto(intra_op_parallelism_threads=1, inter_op_parallelism_threads=2)
        )

        local_init_op = tf.variables_initializer(self.task_vars + self.optimizer_vars)

        def init_fn(scaffold, sess):
            sess.run(init_all_op)

        self.scaffold = tf.train.Scaffold(
            init_op=init_op if not(self.target_task) else self.sync_net,
            ready_for_local_init_op=tf.report_uninitialized_variables(self.global_shared_vars),
            local_init_op=local_init_op,
            init_fn=init_fn if not(self.target_task) else None,
            saver=saver,
            ready_op=tf.report_uninitialized_variables(variables_to_save)
        )

        self.config_proto = tf.ConfigProto(
            device_filters=["/job:ps", "/job:worker/task:{}/cpu:0".format(task_id)])

        self.session = None
        self.local_steps = 0 # Number of updates done

    def build_shared_network(self):
        raise NotImplementedError()

    def build_task_network(self, knowledge_bases):
        raise NotImplementedError()

    @property
    def global_step(self):
        return self._global_step.eval(session=self.session)

    def get_critic_value(self, states, features):
        feed_dict = {
            self.states: states
        }
        if features is not None:
            feed_dict[self.rnn_state_in] = features
        return self.session.run(self.value, feed_dict=feed_dict)[0]

    def choose_action(self, state, features):
        """Choose an action."""
        feed_dict = {
            self.states: [state]
        }
        fetches = [self.action, self.value]
        if features is not None:
            feed_dict[self.rnn_state_in] = features
            fetches += [self.rnn_state_out]
        outputs = self.session.run(fetches, feed_dict=feed_dict)
        return dict(zip(["action", "value", "features"], outputs))

    def get_env_action(self, action):
        return np.argmax(action)

    def pull_batch_from_queue(self):
        """
        Take a trajectory from the queue.
        Also immediately try to extend it if the episode
        wasn't over and more transitions are available.
        """
        trajectory = self.runner.queue.get(timeout=600.0)
        while not trajectory.terminal:
            try:  # Maybe the full trajectory is already available
                trajectory.extend(self.runner.queue.get_nowait())
            except queue.Empty:
                break
        return trajectory

    def learn(self):
        # Assume global shared parameter vectors θ and θv and global shared counter T = 0
        # Assume thread-specific parameter vectors θ' and θ'v
        if self.task_id != 0 and not self.target_task:
            time.sleep(5)
        stop_at = self.config["switch_at_steps"] if not(self.target_task) else self.config["T_max"]
        with tf.train.MonitoredTrainingSession(
            master=self.server.target,
            is_chief=self.first_source_or_target_task,
            config=self.config_proto,
            save_summaries_secs=30,
            scaffold=self.scaffold
        ) as sess:
            tf.get_default_graph().finalize()
            self.session = sess
            sess.run(self.sync_net) # Runner may use vars before the sync net in the while loop
            self.runner.start_runner(sess, self.writer)
            while not sess.should_stop() and self.global_step < stop_at:
                # Synchronize thread-specific parameters θ' = θ and θ'v = θv
                sess.run(self.sync_net)
                trajectory = self.pull_batch_from_queue()
                v = 0 if trajectory.terminal else self.get_critic_value(
                    np.asarray(trajectory.states)[None, -1], trajectory.features[-1])
                rewards_plus_v = np.asarray(trajectory.rewards + [v])
                vpred_t = np.asarray(trajectory.values + [v])
                delta_t = trajectory.rewards + self.config["gamma"] * vpred_t[1:] - vpred_t[:-1]
                batch_r = discount_rewards(rewards_plus_v, self.config["gamma"])[:-1]
                batch_adv = discount_rewards(delta_t, self.config["gamma"])
                fetches = [self.train_op]
                should_make_summaries = self.local_steps % 11 == 0
                if should_make_summaries:
                    if self.first_source_or_target_task:
                        fetches.append(self.histogram_summary_op)
                    fetches.append(self.summary_op)
                    fetches.append(self._global_step)
                states = np.asarray(trajectory.states)
                feed_dict = {
                    self.states: states,
                    self.actions_taken: np.asarray(trajectory.actions),
                    self.adv: batch_adv,
                    self.r: np.asarray(batch_r)
                }
                feature = trajectory.features[0]
                if feature != [] and feature is not None:
                    feed_dict[self.rnn_state_in] = feature
                results = sess.run(fetches, feed_dict)
                if should_make_summaries:
                    global_step = results[-1]
                    self.writer.add_summary(results[-2], global_step)
                    if self.first_source_or_target_task:
                        self.writer.add_summary(results[-3], global_step)
                    self.writer.flush()
                self.local_steps += 1
            self.runner.stop_requested = True

class AKTTaskDiscrete(AKTTask):
    def __init__(self, env, task_id, target_task, cluster, monitor_path, config, video=False):
        self.nA = env.action_space.n
        super(AKTTaskDiscrete, self).__init__(env, task_id, target_task, cluster, monitor_path, config, video=video)

    def build_shared_network(self):
        knowledge_base = tf.get_variable("knowledge_base",
                                         [self.states.get_shape()[-1].value, self.config["n_hidden_units"]],
                                         initializer=normalized_columns_initializer(0.01))
        return [knowledge_base]

    def build_task_network(self, knowledge_bases):
        knowledge_base = knowledge_bases[0]
        sparse_representation_L1 = tf.get_variable(
            "L1/sparse",
            [self.config["n_hidden_units"], self.config["n_hidden_units"]],
            initializer=add_initializers(normalized_columns_initializer(0.01),
                                         tf.constant_initializer(np.identity(self.config["n_hidden_units"],
                                                                             dtype=np.float32))))
            # initializer=normalized_columns_initializer(0.01))
        L1_bias = tf.get_variable(
            "L1/b",
            [self.config["n_hidden_units"]],
            initializer=tf.constant_initializer(0.0))

        W = tf.matmul(knowledge_base, sparse_representation_L1)
        L1 = tf.tanh(tf.nn.xw_plus_b(self.states, W, L1_bias))

        logits = tf.contrib.layers.fully_connected(
            inputs=L1,
            num_outputs=self.nA,
            activation_fn=None,
            weights_initializer=normalized_columns_initializer(0.01),
            biases_initializer=tf.zeros_initializer(),
            scope="logits"
        )

        value = tf.contrib.layers.fully_connected(
            inputs=L1,
            num_outputs=1,
            activation_fn=None,
            weights_initializer=normalized_columns_initializer(1.0),
            biases_initializer=tf.zeros_initializer(),
            scope="value"
        )
        value = tf.reshape(value, [-1], name="value")
        sparse_representations = [sparse_representation_L1]

        probs = tf.nn.softmax(logits, name="probs")

        action_entropy = probs * tf.nn.log_softmax(logits)

        action = tf.squeeze(tf.multinomial(logits - tf.reduce_max(logits, [1], keepdims=True), 1), [1])
        action = tf.squeeze(tf.one_hot(action, self.nA), name="action")

        actor_loss, critic_loss, loss = actor_critic_discrete_loss(logits,
                                                                   probs,
                                                                   value,
                                                                   self.actions_taken,
                                                                   self.adv,
                                                                   self.r,
                                                                   vf_coef=self.config["vf_coef"])
        id_loss = tf.reduce_sum(tf.square(sparse_representation_L1 - tf.constant(np.identity(self.config["n_hidden_units"], dtype=np.float32))))
        loss += self.config["id_coef"] * id_loss
        losses = [actor_loss, critic_loss, id_loss, loss]
        return action, value, action_entropy, loss, losses, sparse_representations

class AKTTaskDiscreteCNNRNN(AKTTaskDiscrete):
    """A3CThread for a discrete action space."""

    def __init__(self, env, task_id, target_task, cluster, monitor_path, config, video=False):
        super(AKTTaskDiscreteCNNRNN, self).__init__(
            env,
            task_id,
            target_task,
            cluster,
            monitor_path,
            config,
            video=video)
        self.initial_features = self.state_init

    def build_shared_network(self):
        x = self.states
        # Convolution layers
        # for i in range(4):
        #     x = tf.nn.elu(conv2d(x, 32, "l{}".format(i + 1), [3, 3], [2, 2]))
        # # Flatten
        # L1 = tf.expand_dims(flatten(x), [0], name="cnns_output")

        # knowledge_base = tf.get_variable("knowledge_base",
        #                                  [self.config["lstm_size"], self.config["n_sparse_units"]],
        #                                  initializer=normalized_columns_initializer(0.01))

        knowledge_bases = []
        n_input_channels = x.get_shape()[3]
        filter_size = (3, 3)
        n_filters = 32
        dtype = tf.float32
        for i in range(4):
            knowledge_base = tf.get_variable(
                "l{}/knowledge_base".format(i + 1),
                [int(filter_size[0] * filter_size[1] * n_input_channels * n_filters) / 4, 4],
                dtype
            )
            print(knowledge_base.get_shape())
            knowledge_bases.append(knowledge_base)
            n_input_channels = n_filters
        return knowledge_bases

    def build_task_network(self, knowledge_bases):
        sparse_representations = []
        x = self.states
        for i in range(4):
            x, sparse = factorized_conv2d(x, knowledge_bases[i], "l{}".format(i + 1), 32, (3, 3), (2, 2))
            x = tf.nn.elu(x)
            sparse_representations.append(sparse)
        x = tf.expand_dims(flatten(x), [0], name="cnns_output")
        lstm_size = self.config["lstm_size"]
        enc_cell = tf.contrib.rnn.BasicLSTMCell(lstm_size)
        lstm_state_size = enc_cell.state_size
        c_init = np.zeros((1, lstm_state_size.c), np.float32)
        h_init = np.zeros((1, lstm_state_size.h), np.float32)
        self.state_init = [c_init, h_init]
        self.rnn_state_in = enc_cell.zero_state(1, tf.float32)
        tf.add_to_collection("rnn_state_in_c", self.rnn_state_in.c)
        tf.add_to_collection("rnn_state_in_h", self.rnn_state_in.h)
        x, self.rnn_state_out = tf.nn.dynamic_rnn(cell=enc_cell,
                                                  inputs=x,
                                                  initial_state=self.rnn_state_in,
                                                  dtype=tf.float32)
        tf.add_to_collection("rnn_state_out_c", self.rnn_state_out.c)
        tf.add_to_collection("rnn_state_out_h", self.rnn_state_out.h)
        x = tf.reshape(x, [-1, lstm_size], name="rnn_output")

        logits = tf.contrib.layers.fully_connected(
            inputs=x,
            num_outputs=self.nA,
            activation_fn=None,
            weights_initializer=normalized_columns_initializer(0.01),
            biases_initializer=tf.zeros_initializer(),
            scope="logits"
        )

        value = tf.contrib.layers.fully_connected(
            inputs=x,
            num_outputs=1,
            activation_fn=None,
            weights_initializer=normalized_columns_initializer(1.0),
            biases_initializer=tf.zeros_initializer(),
            scope="value"
        )
        value = tf.reshape(value, [-1], name="value_output")

        probs = tf.nn.softmax(logits, name="probs")
        action_entropy = probs * tf.nn.log_softmax(logits)

        action = tf.squeeze(tf.multinomial(logits - tf.reduce_max(logits, [1], keepdims=True), 1), [1])
        action = tf.squeeze(tf.one_hot(action, self.nA), name="action")

        actor_loss, critic_loss, loss = actor_critic_discrete_loss(logits,
                                                                   probs,
                                                                   value,
                                                                   self.actions_taken,
                                                                   self.adv,
                                                                   self.r,
                                                                   vf_coef=self.config["vf_coef"],
                                                                   entropy_coef=self.config["entropy_coef"])
        id_loss = 0
        for s in sparse_representations:
            id_loss += tf.reduce_sum(tf.square(s - tf.constant(np.identity(s.get_shape()[0], dtype=np.float32))))
        loss += id_loss
        losses = [actor_loss, critic_loss, id_loss, loss]
        return action, value, action_entropy, loss, losses, sparse_representations

parser = argparse.ArgumentParser()

parser.add_argument("cls", type=str, help="Which class to use for the task.")
parser.add_argument("task_id", type=int, help="Task index.")
parser.add_argument("n_tasks", type=int, help="Total number of tasks in this experiment.")
parser.add_argument("config", type=str, help="Path to config file")
parser.add_argument("--target_task", default=False, action="store_true", help="Say that this is a target task.")
parser.add_argument("-seed", type=int, default=None, help="Seed to use for the environment.")
parser.add_argument("--monitor_path", type=str, help="Path where to save monitor files.")
parser.add_argument("--video", default=False, action="store_true", help="Generate video.")

def main():
    args = parser.parse_args()
    spec = cluster_spec(args.n_tasks, 1)
    cluster = tf.train.ClusterSpec(spec).as_cluster_def()
    cls = load("agents.knowledgetransfer.akt_worker:" + args.cls)
    config = json_to_dict(args.config)
    task = cls(
        make(**config["envs"][args.task_id]),
        args.task_id,
        args.target_task,
        cluster,
        args.monitor_path,
        config,
        video=args.video)
    try:
        task.learn()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
