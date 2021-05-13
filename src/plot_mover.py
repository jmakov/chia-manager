"""
When chia writes to the dest dir, it uses a postfix. A finished file has the extension "plot".
Here we get all the paths where workers save finished plots from the config file and move plots to archive.
"""

import getopt
import glob
import logging
import os
import shutil
import sys
import time

import yaml

from utils import log

EXTENSION_CHIA_PLOT_DONE = "plot"
LOG_PATH = "/var/log/chia-manager/plot-mover.log"


if __name__ == '__main__':
    logger = logging.getLogger()
    log.configure_logger(logger, LOG_PATH)

    try:
        path_archived_plots = ""

        opts, args = getopt.getopt(sys.argv[1:], "h:d:", ["help", "destdirpath"])
        logger.info(f"Started with args: {opts}")

        if not opts or len(opts) < 1:
            raise RuntimeError("Not enough args, run with -h for help")

        for opt, arg in opts:
            if opt in ("-h", "--help"):
                logger.info(
                    "Make sure /var/log/chia-manager/ is writable for the user that runs this script."
                    "Usage: python this_script_name -w chia_fin_plots_path -d chia_archived_plots_path")
                sys.exit()
            elif opt in (["-d", "--destdirpath"]):
                path_archived_plots = arg
    except getopt.GetoptError as e:
        logger.exception(e)
        sys.exit(2)

    try:
        with open("/etc/chia-manager/config.yaml") as f:
            plotting_info = yaml.safe_load(f)["plotting_info"]

        # get all paths we have to scan for finished plots
        paths_fin_plots = []
        for worker_info in plotting_info["worker_info"]:
            paths_fin_plots.append(worker_info["path_fin_plots"])

        while True:
            # collect finished plots from all workers
            fpaths_to_move = []
            for path in paths_fin_plots:
                fpaths_to_move += glob.glob(path + os.sep + "*." + EXTENSION_CHIA_PLOT_DONE)
            logger.info(f"Paths to archive: {fpaths_to_move}")

            for fpath in fpaths_to_move:
                logger.info(f"Moving: {fpath} to {path_archived_plots}")
                shutil.move(fpath, path_archived_plots)

            time.sleep(60)
    except Exception as e:
        logger.exception(e)
        sys.exit(2)
