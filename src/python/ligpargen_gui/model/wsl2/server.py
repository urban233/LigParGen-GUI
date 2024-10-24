import subprocess


class Server:
  def __init__(self):
    pass

  def start_request_loop(self):
    pass

  def ligpargen_command(self):
    subprocess.run(
      ["bash", "/home/alma_ligpargen/ligpargen_batch",
       "-s", "CCO",
       "-n", "Acy",
       "-p", "tmp_results/",  # IMPORTANT: Directory gets cleaned before result files are generated!!!
       "-c", "0",
       "-o", "3",
       "-cgen", "CM1A-LBCC"]
    )
