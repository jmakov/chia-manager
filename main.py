# When chia writes to the dest dir, it uses a postfix. A finished file has the extension .plot

import getopt
import logging
from logging import handlers
import os
import shutil
import sys
import time

EXTENSION_CHIA_PLOT_DONE = ".plot"


def configure_logger(logger):
    logger.setLevel(logging.DEBUG)
    log_path = "/var/log/chia-manager/chia-manager.log"
    fh = handlers.RotatingFileHandler(log_path, backupCount=2, maxBytes=5000000)

    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s %(name)s.%(funcName)s:%(lineno)s:%(levelname)s:%(message)s")
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logging.info("Logger configured")


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
        configure_logger(logger)
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
