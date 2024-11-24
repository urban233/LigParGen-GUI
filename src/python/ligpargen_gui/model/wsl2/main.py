"""Contains main.py of server."""
import sys
sys.path.append("/home/alma_ligpargen/ligpargen_gui")

import logging
from wsl2 import server
from wsl2 import default_logging, exception

logger = default_logging.setup_logger(__file__)


if __name__ == '__main__':
  default_logging.append_to_log_file(logger, "Instantiate server object.", logging.INFO)
  tmp_server = server.Server()
  try:
    default_logging.append_to_log_file(logger, "Listen for job input ...", logging.INFO)
    if not tmp_server.listen_for_job_input():
      default_logging.append_to_log_file(logger, "Invalid job input!", logging.FATAL)
      tmp_server.send_finished_signal("Job failed! There was an error in the internal job input!", has_failed=True)
      exit(0)
    default_logging.append_to_log_file(logger, "Running job ...", logging.INFO)
    if not tmp_server.run_job():
      default_logging.append_to_log_file(logger, "Job failed!", logging.FATAL)
      tmp_server.send_finished_signal("Job failed!", has_failed=True)
      exit(0)
    else:
      default_logging.append_to_log_file(logger, "Job finished.", logging.INFO)
      tmp_server.send_finished_signal("Job finished.")
      exit(0)
  except Exception as e:
    default_logging.append_to_log_file(logger, f"An error occurred: {e}", logging.FATAL)
    tmp_server.send_finished_signal("Job failed with an internal error.", has_failed=True)
    exit(0)
