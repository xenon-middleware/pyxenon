import pytest
from xenon import (
    FileSystem, CredentialMap, PasswordCredential, UserCredential)

import socket
from contextlib import closing


def check_socket(host, port):
    """Checks if port is open on host. This is used to check if the
    Xenon-GRPC server is running."""
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        return sock.connect_ex((host, port)) == 0


@pytest.mark.skipif(
        not check_socket('localhost', 10022),
        reason="Needs the Xenon-slurm docker container open on port 10022.")
def test_password_credential(xenon_server, tmpdir):
    location = 'localhost:10022'
    username = 'xenon'
    password = 'javagat'

    credential = PasswordCredential(
        username=username,
        password=password)

    fs = FileSystem.create(
        adaptor='sftp',
        location=location,
        password_credential=credential,
        properties={
                'xenon.adaptors.filesystems.sftp.strictHostKeyChecking': 'false'
            })

    assert fs.get_adaptor_name() == 'sftp'
    fs.close()


@pytest.mark.skipif(
        not check_socket('localhost', 10022),
        reason="Needs the Xenon-slurm docker container open on port 10022.")
def test_credential_map(xenon_server, tmpdir):
    location = 'localhost:10022'
    username = 'xenon'
    password = 'javagat'

    credential = CredentialMap(
        entries={
            'localhost:10022': UserCredential(
                password_credential=PasswordCredential(
                    username=username,
                    password=password))
        })

    fs = FileSystem.create(
        adaptor='sftp',
        location=location,
        credential_map=credential,
        properties={
                'xenon.adaptors.filesystems.sftp.strictHostKeyChecking': 'false'
            })

    assert fs.get_adaptor_name() == 'sftp'
    fs.close()
