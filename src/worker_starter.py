import logging
import multiprocessing
import os
import shutil
import sys
import time

import yaml

from utils import log

LOG_PATH = "/var/log/chia-manager/worker_starter.log"
LOG_PATH_WORKERS = "/var/log/chia-manager/workers"


if __name__ == '__main__':
    logger = logging.getLogger()

    log.configure_logger(logger, LOG_PATH)
    logger.info("Started")

    cpu_cores_available = multiprocessing.cpu_count()

    try:
        with open("/etc/chia-manager/config.yaml") as f:
            plotting_info = yaml.safe_load(f)["plotting_info"]

        path_chia_source = plotting_info["path_chia_source"]
        farmer_pubkey = plotting_info["farmer_pubkey"]
        pool_pubkey = plotting_info["pool_pubkey"]
        worker_infos = plotting_info["worker_info"]
        min_time_between_starting_workers = plotting_info["min_time_between_starting_workers"]
        logger.info(f"Worker infos: {worker_infos}")

        # init timekeeper and clean temp dirs
        workers_to_start = 0
        worker_timekeeper = {}
        for worker_info in worker_infos:
            workers_to_start += worker_info["workers"]

            # clean temp dirs
            path_tmp = worker_info["path_tmp"]
            logger.info(f"Deleting tmp dir: {path_tmp}")
            try:
                shutil.rmtree(path_tmp)
            except FileNotFoundError as e:
                logger.warning(e)

            # set init time so that the workers will be started in the first loop
            worker_timekeeper[worker_info["worker_name_prefix"]] = 0

            worker_info["workers_active"] = 0

        cpu_cores_used = 0
        _core_end = -1      # core count starts with 0
        while workers_to_start > 0:
            for worker_info in worker_infos:
                if worker_info["workers"] > 0:
                    time_now = time.time()
                    time_last_run = worker_timekeeper[worker_info["worker_name_prefix"]]
                    time_between_starting_workers = worker_info["time_between_starting_workers"]

                    if time_now - time_last_run > time_between_starting_workers:
                        threads_per_worker = worker_info["threads_per_worker"]
                        pin_to_core = worker_info["pin_to_core"]
                        ram_usage = worker_info["ram_usage"]
                        worker_timekeeper[worker_info["worker_name_prefix"]] = time_now
                        worker_name = worker_info["worker_name_prefix"]
                        path_tmp = worker_info["path_tmp"]
                        path_fin_plots = worker_info["path_fin_plots"]
                        worker_number = worker_info["workers_active"]
                        logger.info(f"Starting worker: {worker_name}{worker_number}")

                        if pin_to_core:
                            if threads_per_worker > 1:
                                _core_start = _core_end + 1
                                _core_end = _core_start + threads_per_worker - 1
                                taskset_cpu_list = f"{_core_start}-{_core_end}"
                            else:
                                taskset_cpu_list = cpu_cores_used

                            taskset_cmd = f"taskset --cpu-list {taskset_cpu_list}"
                        else:
                            taskset_cmd = ""

                        command_chia_plots = \
                            f"nohup {taskset_cmd} " \
                            f"{path_chia_source}/venv/bin/python3 " \
                            f"{path_chia_source}/venv/bin/chia plots create " \
                            f"-b{ram_usage} -u128 -r{threads_per_worker} -k32 -n100000 " \
                            f"-f{farmer_pubkey} " \
                            f"-p{pool_pubkey} " \
                            f"-t{path_tmp}/worker{worker_number} " \
                            f"-2{path_tmp}/worker{worker_number} " \
                            f"-d{path_fin_plots} > {LOG_PATH_WORKERS}/{worker_name}{worker_number}  2>&1 &"
                        logger.info(f"Running: {command_chia_plots}")
                        os.system(command_chia_plots)

                        worker_info["workers_active"] += 1
                        cpu_cores_used += 1
                        worker_info["workers"] -= 1
                        workers_to_start -= 1
                        logger.info(f"Cpu cores used: {cpu_cores_used}")

            if workers_to_start > 0:
                logger.info(f"Sleeping for {min_time_between_starting_workers}s")
                time.sleep(min_time_between_starting_workers)

        logger.info("Done. No more workers to start.")
    except Exception as e:
        logger.exception(e)
        sys.exit(2)
