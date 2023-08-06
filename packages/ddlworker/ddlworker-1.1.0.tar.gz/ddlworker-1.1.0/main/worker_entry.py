from worker.worker_start import *

def worker_entry(master_endpoint, workdir, port):
    worker = Worker(master_endpoint, port, workdir)
    while True:
        enroll_is_success = worker.enroll()
        if not enroll_is_success:
            raise RuntimeError("enroll failed")
        while True:
            poll_is_success, enroll_again = worker.poll()
            if not poll_is_success:
                if enroll_again:
                    # break polling loop and enroll again
                    break
                else:
                    raise RuntimeError("poll failed")