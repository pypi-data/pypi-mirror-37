import tensorflow as tf
from os.path import join

from worker.worker_util.worker_util import WorkerFinishQueueItem


class SignalFinishHook(tf.train.SessionRunHook):
    def __init__(self, input_queue, output_queue):
        self.input_queue = input_queue
        self.output_queue = output_queue

    def end(self, session):
        # Put a WorkerFinishQueueItem in the output queue
        # TODO: distinguish between session failure vs success.
        print("worker_exec::SignalFinishHook signal worker exec finish")
        self.output_queue.put(WorkerFinishQueueItem())


class SaveAtEndHook(tf.train.SessionRunHook):
    def __init__(self, checkpoint_location):
        self.checkpoint_location = checkpoint_location
        self._saver = tf.train.Saver()

    def end(self, session):
        self._saver.save(session, join(self.checkpoint_location, 'result/model-finish.ckpt'))
