import zmq


class Client:
  def __init__(self):
    # Socket definitions
    context = zmq.Context()
    self._sender_socket = context.socket(zmq.PUSH)
    self._sender_socket.connect("tcp://127.0.0.1:8033")
    self._recv_socket = context.socket(zmq.PULL)
    self._recv_socket.connect("tcp://127.0.0.1:8034")

  def send_job_input(self, a_job_input_as_json: str):
    self._sender_socket.send_json(a_job_input_as_json)
