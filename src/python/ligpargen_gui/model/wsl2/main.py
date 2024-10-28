"""Contains main.py of server."""
import sys
sys.path.append("/home/alma_ligpargen/ligpargen_gui")

from wsl2 import server

if __name__ == '__main__':
  tmp_server = server.Server()
  tmp_server.listen_for_job_input()
  if not tmp_server.run_job():
    print("Job failed!")
  else:
    print("Job finished successfully!")
