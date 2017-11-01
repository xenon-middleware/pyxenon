import pytest
from xenon import (
    FileSystem, Path, CredentialMap, PasswordCredential,
    DefaultCredential, UserCredential)


@pytest.mark.skip(reason="Needs docker running.")
def test_password_credential(xenon_server, tmpdir):
    location = 'localhost:10022'
    username = 'xenon'
    password = 'javagat'

    credential=PasswordCredential(
        username=username,
        password=password)

    fs = FileSystem.create(
        adaptor='sftp',
        location=location,
        password_credential=credential)

    assert fs.get_adaptor_name() == 'sftp'
    fs.close()


@pytest.mark.skip(reason="Needs docker running.")
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
        credential_map=credential)

    assert fs.get_adaptor_name() == 'sftp'
    fs.close()
