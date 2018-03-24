import socket
import sys
import code
import time

DEBUG_PORT = 1337

def remote_repl(local):
    sys.stdout.flush()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("0.0.0.0", DEBUG_PORT))
    s.listen(1)

    print("Waiting for remote debug connection on port {}.".format(DEBUG_PORT))

    conn, addr = s.accept()

    print("Accepted remote debug connection from '{}'.".format(addr[0]))

    sys.stdout.flush()
    sys.stderr.flush()
    stdin_bak, stdout_bak, stderr_bak = sys.stdin, sys.stdout, sys.stderr
    rfile = conn.makefile("r")
    wfile = conn.makefile("w")
    sys.stdin, sys.stdout, sys.stderr = rfile, wfile, wfile

    try:
        code.interact(local=local)
    except SystemExit:
        pass

    conn.close()
    s.close()
    sys.stdin, sys.stdout, sys.stderr = stdin_bak, stdout_bak, stderr_bak
    print("Remote debug session closed.")

while 1:
    remote_repl(locals())
    time.sleep(1)
