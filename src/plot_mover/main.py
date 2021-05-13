# When chia writes to the dest dir, it uses a postfix. A finished file has the extension .plot

import getopt
import logging
import os
import shutil
import sys
import time

from src import utils

EXTENSION_CHIA_PLOT_DONE = ".plot"
LOG_PATH = "/var/log/chia-manager/plot-mover.log"


if __name__ == '__main__':
    logger = logging.getLogger()

    try:
        path_fin_plots = ""
        path_archived_plots = ""

        opts, args = getopt.getopt(sys.argv[1:], "h:w:d:", ["help", "watchdirpath", "destdirpath"])

        if not opts or len(opts) > 2:
            print("Not enough args, run with  -h for help")
            sys.exit()

        for opt, arg in opts:
            if opt in ("-h", "--help"):
                print(
                    "Make sure /var/log/chia-manager/ is writable for the user that runs this script."
                    "Usage: python this_script_name -w chia_fin_plots_path -d chia_archived_plots_path")
                sys.exit()
            elif opt in (["-w", "--watchdirpath"]):
                path_fin_plots = arg
            elif opt in (["-d", "--destdirpath"]):
                path_archived_plots = arg
    except getopt.GetoptError as e:
        print(e)
        sys.exit(2)

    try:
        utils.configure_logger(logger, LOG_PATH)
        logger.info(f"Started with args: {opts}")

        while True:
            files = os.listdir(path_fin_plots)
            logger.info(f"Found files: {files}")

            for file in files:
                fn, fextension = os.path.splitext(file)

                if fextension == EXTENSION_CHIA_PLOT_DONE:
                    fp = path_fin_plots + os.sep + file
                    logger.info(f"Moving: {fp} to {path_archived_plots}")
                    shutil.move(fp, path_archived_plots)
            time.sleep(60)
    except Exception as e:
        logger.exception(e)
        sys.exit(2)
