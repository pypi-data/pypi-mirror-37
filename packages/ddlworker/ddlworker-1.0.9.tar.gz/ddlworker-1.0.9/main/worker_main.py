import os, os.path
import argparse
import sys
import shutil
import multiprocessing as mp
from time import sleep

# Add the top-level directory to the PYTHONPATH
worker_main_dir_path = os.path.dirname(os.path.realpath(__file__))
worker_dir_path = os.path.abspath(os.path.join(worker_main_dir_path, os.pardir))
sys.path.insert(0, worker_dir_path)

from main.worker_entry import worker_entry
from main.utils import get_tf_device_count, register, get_config

def workers_start(master_endpoint, metafile, workdir):
    worker_meta = get_config(metafile)
    if not worker_meta:
        print("[Error] Malformed worker metafile at: {}!".format(metafile))
        return

    worker_processes = {}
    for worker_uuid in worker_meta.keys():
        worker_config = worker_meta[worker_uuid]
        p = mp.Process(target=worker_entry,
                       args=(master_endpoint,
                             worker_config["workdir"],
                             worker_config["port"]))

        worker_processes[worker_uuid] = {
            'process' : p,
            'config' : worker_config
        }

        p.start()

    if not worker_processes:
        return

    # If a worker is stopped, restart it.
    while True:
        for worker in worker_processes.keys():
            worker_context = worker_processes[worker]
            process = worker_context['process']
            if process.is_alive():
                continue

            process.join()
            worker_config = worker_context['config']
            p = mp.Process(target=worker_entry,
                           args=(master_endpoint,
                                 worker_config["workdir"],
                                 worker_config["port"]))

            worker_context['process'] = p
            p.start()

        sleep(300)

    return

def workers_register(master_endpoint, metafile, workdir, assume_cpu, assume_gpu, secrete):
    cpu_count, gpu_count = get_tf_device_count()
    if assume_cpu > 0:
        cpu_count = assume_cpu

    if assume_gpu > 0:
        gpu_count = assume_gpu
    register(master_endpoint, metafile, workdir, cpu_count, gpu_count, gpu_count, secrete)
    return

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--master_endpoint_override',
        type=str,
        default="http://dtf-masterserver-dev.us-west-1.elasticbeanstalk.com",
        help='master server endpoint')
    parser.add_argument(
        '--workdir',
        type=str,
        required=True,
        help='work directory for the worker, must be an absolute path')
    parser.add_argument(
        '--rebuild',
        type=bool,
        default=False,
        help='re-register all the workers')
    parser.add_argument(
        '--assume_gpu',
        type=int,
        default=0,
        help='manually input the gpu count')
    parser.add_argument(
        '--assume_cpu',
        type=int,
        default=0,
        help='manually input the cpu count')
    parser.add_argument(
        '--secrete',
        type=str,
        default=None,
        help='secrete')
    FLAGS, _ = parser.parse_known_args()

    rebuild = FLAGS.rebuild
    workdir = FLAGS.workdir
    assume_gpu = FLAGS.assume_gpu
    assume_cpu = FLAGS.assume_cpu
    master_endpoint = FLAGS.master_endpoint_override
    secrete = FLAGS.secrete

    # Make sure workdir and meta directory exists.
    if rebuild and os.path.isdir(workdir):
        shutil.rmtree(workdir, ignore_errors=True)

    if not os.path.isdir(workdir):
        os.mkdir(workdir)

    metadir = os.path.join(workdir, ".meta")
    if not os.path.isdir(metadir):
        os.mkdir(metadir)

    # Check if worker has already been registered.
    registered = True
    metafile = os.path.join(metadir, "worker_config.yaml")
    if not os.path.exists(metafile):
        registered = False

    # Register first...
    if not registered:
        workers_register(master_endpoint, metafile, workdir, assume_cpu, assume_gpu, secrete)

    workers_start(master_endpoint, metafile, workdir)
    return

if __name__ == '__main__':
    main()