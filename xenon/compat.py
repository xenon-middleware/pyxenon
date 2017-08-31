"""
Define cross-platform methods.
"""

from pathlib import Path
import logging
import subprocess
import os
import sys

from xdg import XDG_CONFIG_HOME

from .create_keys import create_self_signed_cert

# ======================= Linux department ====================================
if os.name == 'posix':
    import fcntl
    import signal

    def find_xenon_grpc_jar():
        """Find the Xenon-GRPC jar file. This first looks for the `xenon-grpc`
        shell script by running `which xenon-grcp` and then takes the relative
        path `../lib/xenon-grpc-0.0.1-all.jar` from there.

        TODO: install xenon-grpc jar-file in the Python distribution."""
        logger = logging.getLogger('xenon')
        which_xenon = subprocess.run(
            ['which', 'xenon-grpc'],
            universal_newlines=True,
            stdout=subprocess.PIPE)
        if which_xenon.returncode != 0:
            return None

        xenon_prefix = Path(which_xenon.stdout).parent.parent
        xenon_jar_path = xenon_prefix / 'lib' / 'xenon-grpc-1.0.0-all.jar'
        logger.info("Found Xenon-GRPC at: {}".format(xenon_jar_path))
        return str(xenon_jar_path)

    def start_xenon_server(port=50051, disable_tls=False):
        """Start the server."""
        jar_file = find_xenon_grpc_jar()
        if not jar_file:
            raise RuntimeError("Could not find 'xenon-grpc' jar file.")

        cmd = ['java', '-jar', jar_file, '-p', str(port)]

        if not disable_tls:
            create_self_signed_cert()
            crt_file = Path(XDG_CONFIG_HOME) / 'xenon-grpc' / 'server.crt'
            key_file = Path(XDG_CONFIG_HOME) / 'xenon-grpc' / 'server.key'

            cmd.extend([
                '--server-cert-chain', str(crt_file),
                '--server-private-key', str(key_file),
                '--client-cert-chain', str(crt_file)])

        process = subprocess.Popen(
            cmd,
            bufsize=1,
            universal_newlines=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            preexec_fn=os.setsid)
        return process

    def kill_process(process):
        """Kill the process group associated with the given process. (posix)"""
        logger = logging.getLogger('xenon')
        logger.info('Terminating Xenon-GRPC server.')
        # os.kill(self.process.pid, signal.SIGINT)
        os.killpg(os.getpgid(process.pid), signal.SIGINT)
        process.wait()

    def print_streams(process, event):
        """Reads stdout and stderr of process by settings both files
        in non-blocking mode, and polling every 0.1 seconds. The loop
        is broken by setting the event. Only works on POSIX (linux) systems."""
        def set_nonblocking(file):
            """Sets the file io to non-blocking using fcntl calls. (posix
            only)"""
            file_descriptor = file.fileno()
            file_flags = fcntl.fcntl(file_descriptor, fcntl.F_GETFL)
            fcntl.fcntl(
                file_descriptor, fcntl.F_SETFL, file_flags | os.O_NONBLOCK)

        def forward_lines(file, name):
            """Forward lines from file to logger."""
            logger = logging.getLogger('xenon.{}'.format(name))

            line = ''
            while True:
                try:
                    char = file.read(1)
                    if char == '':
                        break
                    if char == '\n':
                        logger.info('{} {}'.format(name, line))
                        line = ''
                    else:
                        line += char

                except:
                    pass

        set_nonblocking(process.stdout)
        set_nonblocking(process.stderr)

        while not event.is_set():
            event.wait(0.1)
            forward_lines(process.stdout, '[out]')
            forward_lines(process.stderr, '[err]')


# ===================== Windows department ====================================
elif os.name == 'nt':
    def find_xenon_grpc_jar():
        """Find the Xenon-GRPC jar-file, windows version."""
        jar_file = Path(sys.prefix) / 'lib' / 'xenon-grpc-1.0.0-all.jar'

        if not jar_file.exists():
            return None
        else:
            return str(jar_file)

    def start_xenon_server(port=50051, disable_tls=False):
        """Start the server, windows version."""
        jar_file = find_xenon_grpc_jar()
        if not jar_file:
            raise RuntimeError("Could not find 'xenon-grpc' jar file.")

        cmd = ['java', '-jar', jar_file, '-p', str(port)]

        if not disable_tls:
            create_self_signed_cert()
            crt_file = Path(XDG_CONFIG_HOME) / 'xenon-grpc' / 'server.crt'
            key_file = Path(XDG_CONFIG_HOME) / 'xenon-grpc' / 'server.key'

            cmd.extend([
                '--server-cert-chain', str(crt_file),
                '--server-private-key', str(key_file),
                '--client-cert-chain', str(crt_file)])

        process = subprocess.Popen(
            cmd,
            bufsize=1,
            universal_newlines=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        return process
