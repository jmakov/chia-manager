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


def print_script_help():
    print(
        "Usage: python plot_mover.py [OPTION] archive_path\n"
        "OPTIONS:"
        "   -d, --destdirpath\n"
        "       Path to archive finished plots.")


if __name__ == '__main__':
    logger = logging.getLogger()
    log.configure_logger(logger, LOG_PATH)

    try:
        path_archived_plots = ""

        opts, args = getopt.getopt(sys.argv[1:], "h:d:", ["help", "destdirpath="])
        logger.info(f"Started with args: {args}")

        if not opts or len(opts) < 1:
            print("No options or not enough options.")
            print_script_help()
            sys.exit(2)

        for opt, arg in opts:
            if opt in ("-h", "--help"):
                print_script_help()
                print(
                    "Make sure /var/log/chia-manager/ is writable for the user that runs this script."
                    "Usage: python this_script_name -w chia_fin_plots_path -d chia_archived_plots_path")
                sys.exit(2)
            elif opt in (["-d", "--destdirpath"]):
                path_archived_plots = arg
    except getopt.GetoptError as e:
        logger.exception(e)
        sys.exit(2)

    try:
        with open("/etc/chia-manager/config.yaml") as f:
            plotting_info = yaml.safe_load(f)["plotting_info"]

        # We always start from the upper part of the config file to move finished plots first from nvme storage.
        while True:
            for worker_info in plotting_info["worker_info"]:
                path_fin_plots = worker_info["path_fin_plots"]
                fpaths_to_move = glob.glob(path_fin_plots + os.sep + "*." + EXTENSION_CHIA_PLOT_DONE)

                if path_archived_plots in path_fin_plots:
                    # Skip moving from disk A to disk A
                    continue
                elif fpaths_to_move:
                    for fp in fpaths_to_move:
                        logger.info(f"Moving: {fp} to {path_archived_plots}")
                        shutil.move(fp, path_archived_plots)
                    break

            time.sleep(60)
    except Exception as e:
        logger.exception(e)
        sys.exit(2)
