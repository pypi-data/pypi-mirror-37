import os, sys, json, shutil, os.path
import socket, errno
import argparse
import uuid
import yaml

from tensorflow.python.client import device_lib

from worker.worker_start import *

# Helper function
def register_single_worker(toplevel_workdir, master_endpoint, base_port, is_gpu_worker, resource_id, secrete):
    port = base_port
    worker_workdir_name = "workdir_{}".format(str(uuid.uuid4())[:8])
    worker_workdir = os.path.join(toplevel_workdir, worker_workdir_name)
    os.mkdir(worker_workdir)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            if port >= 65535:
                print("[Error] invalid port number: {}".format(port))
                return False, None, None, None

            s.bind(("127.0.0.1", port))
            s.close()
            print("[Register] found available port: {}".format(port))
            break
        except socket.error as e:
            port = ((port // 100) + 1) * 100
            if e.errno == errno.EADDRINUSE:
                continue
            else:
                # something else raised the socket.error exception
                print("[Error] {}".format(e))
                return False, None, None, None
        except Exception as e:
            print("[Error] uncaught error: {}".format(str(e)))
            return False, None, None, None

    worker = Worker(master_endpoint, port, worker_workdir)
    register_is_success, worker_uuid = worker.register(is_gpu_worker, resource_id, secrete)
    if not register_is_success:
        print("[Error] worker failed to register")
        return False, None, None, None

    print("[Register] registered worker {}".format(worker_uuid))
    return True, worker_uuid, worker_workdir, port

################################################################################

def register(master_endpoint, metafile, toplevel_workdir, cpu_worker_count, gpu_count, gpu_worker_count, secrete):
    if cpu_worker_count < 0:
        cpu_worker_count = 0

    if gpu_worker_count < 0:
        gpu_worker_count = 0

    if gpu_count < 0:
        gpu_count = 0

    print("Start worker registration")
    print("\t[master_endpoint url]: {}".format(master_endpoint))
    print("\t[toplevel working directory]: {}".format(toplevel_workdir))
    print("\t[cpu worker count] : {}".format(cpu_worker_count))
    print("\t[gpu worker count] : {} (/{} GPU)".format(gpu_worker_count, gpu_count))
    print("\t[secrete] : {}".format(secrete))
    if gpu_worker_count > gpu_count:
        print("\t** There are {} GPU workers more than GPUs... Some GPU works might have bad performance".format(gpu_worker_count - gpu_count))

    if cpu_worker_count == 0 and gpu_worker_count == 0:
        print("[Error] Will not register anything...")
        return

    if not os.path.isdir(toplevel_workdir):
        print("[Error] Workdir {} does not exist...".format(toplevel_workdir))
        return

    port = 10000
    worker_registered = {}
    # Register all the workers.
    register_matrix = [(i, False, -1) for i in range(cpu_worker_count)] +\
                      [(i, True, (i if i < gpu_count else -1)) for i in range(cpu_worker_count)]

    for index, is_gpu_worker, resource_id in register_matrix:
        success, workder_uuid, worker_workdir, worker_port = register_single_worker(
            toplevel_workdir,
            master_endpoint,
            port,
            is_gpu_worker,
            resource_id,
            secrete)

        if not success:
            continue

        worker_registered[workder_uuid] = {
            "workdir" : worker_workdir,
            "port" : worker_port
        }

        port = ((worker_port // 100) + 1) * 100
        if port >= 65535:
            print("[Error] Running out of port! Abort further registration!")
            break

    # Write the worker meta file.
    if worker_registered:
        set_config(metafile, worker_registered)
    return

def get_config(metafile):
    try:
        with open(metafile, "r") as meta:
            config = yaml.load(meta)
            return config
    except:
        return {}

def set_config(metafile, config):
    with open(metafile, 'w') as outfile:
        yaml.dump(config, outfile, default_flow_style=False)
    return

def get_tf_device_count():
    local_device_protos = device_lib.list_local_devices()
    cpus = [x for x in local_device_protos if x.device_type == 'CPU']
    gpus = [x for x in local_device_protos if x.device_type == 'GPU']
    return len(cpus), len(gpus)