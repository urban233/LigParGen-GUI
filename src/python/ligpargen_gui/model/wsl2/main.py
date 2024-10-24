"""Contains main.py of server."""
import sys
sys.path.append("/home/alma_ligpargen/ligpargen_gui")

from wsl2 import server

if __name__ == '__main__':
  tmp = server.Server()
  tmp.ligpargen_command()
