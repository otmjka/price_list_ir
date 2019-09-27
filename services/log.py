import os
import logging
import sys

log_dir = os.path.join('.', 'tmp_log')
if not os.path.exists(log_dir):
  os.mkdir(log_dir)

logging.basicConfig(
  handlers=[
#   logging.FileHandler(os.path.join(log_dir, 'main.log')),
    logging.StreamHandler(sys.stdout)
  ],
  level=logging.DEBUG,
#  [%(processName)s]
  format="%(asctime)s \t%(levelname)s\t%(message)s",
)
