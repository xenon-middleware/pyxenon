"""
Certificate creation.
"""

import logging
from socket import gethostname
from pathlib import Path

from xdg import BaseDirectory
from OpenSSL import crypto


def create_self_signed_cert():
    """Creates a self-signed certificate key pair."""
    config_dir = Path(BaseDirectory.xdg_config_home) / 'xenon-grpc'
    config_dir.mkdir(parents=True, exist_ok=True)
    crt_file = config_dir / 'server.crt'
    key_file = config_dir / 'server.key'

    if crt_file.exists() and key_file.exists():
        return

    logger = logging.getLogger('xenon')
    logger.info("Creating authentication keys for xenon-grpc.")

    # create a key pair
    k = crypto.PKey()
    k.generate_key(crypto.TYPE_RSA, 1024)

    # create a self-signed cert
    cert = crypto.X509()
    cert.get_subject().CN = gethostname()
    cert.set_serial_number(1000)
    cert.gmtime_adj_notBefore(0)
    # valid for almost ten years!
    cert.gmtime_adj_notAfter(10 * 365 * 24 * 3600)
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(k)
    cert.sign(k, 'sha256')

    open(str(crt_file), "wb").write(
        crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
    open(str(key_file), "wb").write(
        crypto.dump_privatekey(crypto.FILETYPE_PEM, k))
