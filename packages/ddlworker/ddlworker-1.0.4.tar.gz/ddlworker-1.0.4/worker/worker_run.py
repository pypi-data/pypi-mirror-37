from os.path import join, exists
import shutil

import os
import sys

from common.global_variable import CODE_DIR_NAME, DATASET_DIR_NAME, OUTPUT_DIR_NAME, WORKER_FAILED_MARKER, WORKER_SUCCESS_MARKER
from worker.worker_util.worker_util import worker_prepare_gpu
from worker.worker_util.worker_util import create_tf_config


def worker_run(workdir_path, job_name, task_index, cluster_spec, resource_id, worker_type, task_uuid):
    resource_id = int(resource_id)
    task_index = int(task_index)
    workdir_code_path = None
    if job_name == "worker" or job_name == "ps":
        try:
            worker_prepare_gpu(worker_type, resource_id)

            # set up os.env for TF_CONFIG
            if task_index != -1:
                print("worker_run: distributed training")
                create_tf_config(job_name, task_index, cluster_spec)
            else:
                print("worker_run: single worker training")

            # update user python path
            workdir_code_path = join(workdir_path, CODE_DIR_NAME)
            sys.path.insert(0, workdir_code_path)

            # run user code

            out_dir = join(workdir_path, OUTPUT_DIR_NAME)
            if exists(out_dir):
                shutil.rmtree(out_dir)
            os.makedirs(out_dir)

            # log system success
            with open(join(workdir_path, WORKER_SUCCESS_MARKER), "w") as f:
                f.write("success")
        except Exception as ex:
            # log system exception
            with open(join(workdir_path, WORKER_FAILED_MARKER), "w") as f:
                f.write(str(ex))
            return

        sys.stdout = open(join(workdir_path, OUTPUT_DIR_NAME, "{}.log".format(task_uuid)), "w")
        sys.stderr = open(join(workdir_path, OUTPUT_DIR_NAME, "{}.error.log".format(task_uuid)), "w")

        print("worker_code_path: {}".format(workdir_code_path))
        p = __import__("main")

        # invoke main function, <dataset_dir>, <model_dir>
        p.main(join(workdir_path, DATASET_DIR_NAME), join(workdir_path, OUTPUT_DIR_NAME))
    else:
        raise ValueError("unrecognized job name: {}".format(job_name))


worker_run(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7])
