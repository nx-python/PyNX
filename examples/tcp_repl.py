import socket
import sys
import code


DEBUG_PORT = 1337


if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("0.0.0.0", DEBUG_PORT))
    sock.listen(1)
    print("Waiting for remote debug connection on port {}.".format(DEBUG_PORT), flush=True)

    conn, addr = sock.accept()

    print("Accepted remote debug connection from '{}'.".format(addr[0]))

    sys.stdout.flush()
    sys.stderr.flush()
    stdin_bak, stdout_bak, stderr_bak = sys.stdin, sys.stdout, sys.stderr
    rfile = conn.makefile("r")
    wfile = conn.makefile("w")
    sys.stdin, sys.stdout, sys.stderr = rfile, wfile, wfile

    try:
        code.interact(local=locals())
    except SystemExit:
        pass

    conn.close()
    sock.close()
    sys.stdin, sys.stdout, sys.stderr = stdin_bak, stdout_bak, stderr_bak
