"""Contains main.py of server."""
import sys
sys.path.append("/home/alma_ligpargen/ligpargen_gui")

from wsl2 import server

if __name__ == '__main__':
  tmp_server = server.Server()
  # tmp.ligpargen_command()
  tmp_server.listen_for_job_input()
  tmp_server.run_job()
