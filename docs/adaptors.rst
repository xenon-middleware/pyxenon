Adaptors
========
This section contains the adaptor documentation which is generated from the
information provided by the adaptors themselves.

.. contents::


File System
-----------

.. note:: Supported property names should be prefixed with
``"xenon.adaptors.filesystems"``.  We've left this prefix out to improve
readability of the tables.


S3
~~
The S3 adaptor uses Apache JClouds to talk to s3 and others. To
authenticate use PasswordCredential with access key id as username and
secret access key as password

+------------------------------------+----------------------+
| field                              | value                |
+====================================+======================+
| supports_third_party_copy          | False                |
+------------------------------------+----------------------+
| can_create_symboliclinks           | False                |
+------------------------------------+----------------------+
| can_read_symboliclinks             | False                |
+------------------------------------+----------------------+
| is_connectionless                  | True                 |
+------------------------------------+----------------------+
| supported_credentials              | `PasswordCredential` |
+------------------------------------+----------------------+
| can_append                         | False                |
+------------------------------------+----------------------+
| supports_reading_posix_permissions | False                |
+------------------------------------+----------------------+
| supports_setting_posix_permissions | False                |
+------------------------------------+----------------------+
| supports_rename                    | False                |
+------------------------------------+----------------------+
| needs_size_beforehand              | True                 |
+------------------------------------+----------------------+

location string:
    * `http[s]://host[:port]/bucketname[/workdir]`
    * `https://s3.region.amazonaws.com/bucketname[/workdir]`

supported properties:

+---------------+-------------------------------------------------------+-----------+---------+
| name          | description                                           | data_type | default |
+===============+=======================================================+===========+=========+
| s3.bufferSize | The buffer size to use when copying files (in bytes). | size      | `64K`   |
+---------------+-------------------------------------------------------+-----------+---------+

File
~~~~
This is the local file adaptor that implements file functionality for
local access.

+------------------------------------+---------------------+
| field                              | value               |
+====================================+=====================+
| supports_third_party_copy          | False               |
+------------------------------------+---------------------+
| can_create_symboliclinks           | True                |
+------------------------------------+---------------------+
| can_read_symboliclinks             | True                |
+------------------------------------+---------------------+
| is_connectionless                  | True                |
+------------------------------------+---------------------+
| supported_credentials              | `DefaultCredential` |
+------------------------------------+---------------------+
| can_append                         | True                |
+------------------------------------+---------------------+
| supports_reading_posix_permissions | True                |
+------------------------------------+---------------------+
| supports_setting_posix_permissions | True                |
+------------------------------------+---------------------+
| supports_rename                    | True                |
+------------------------------------+---------------------+
| needs_size_beforehand              | False               |
+------------------------------------+---------------------+

location string:
    * `(null)`
    * `(empty string)`
    * `[/workdir]`
    * `driveletter:[/workdir]`

supported properties:

+-----------------+-------------------------------------------------------+-----------+---------+
| name            | description                                           | data_type | default |
+=================+=======================================================+===========+=========+
| file.bufferSize | The buffer size to use when copying files (in bytes). | size      | `64K`   |
+-----------------+-------------------------------------------------------+-----------+---------+

Sftp
~~~~
The SFTP adaptor implements all file access functionality to remote
SFTP servers

+------------------------------------+----------------------------------------------------+
| field                              | value                                              |
+====================================+====================================================+
| supports_third_party_copy          | False                                              |
+------------------------------------+----------------------------------------------------+
| can_create_symboliclinks           | True                                               |
+------------------------------------+----------------------------------------------------+
| can_read_symboliclinks             | True                                               |
+------------------------------------+----------------------------------------------------+
| is_connectionless                  | False                                              |
+------------------------------------+----------------------------------------------------+
| supported_credentials              | `DefaultCredential`, `CertificateCredential`,      |
|                                    | `PasswordCredential`, `CredentialMap`              |
+------------------------------------+----------------------------------------------------+
| can_append                         | True                                               |
+------------------------------------+----------------------------------------------------+
| supports_reading_posix_permissions | True                                               |
+------------------------------------+----------------------------------------------------+
| supports_setting_posix_permissions | True                                               |
+------------------------------------+----------------------------------------------------+
| supports_rename                    | True                                               |
+------------------------------------+----------------------------------------------------+
| needs_size_beforehand              | False                                              |
+------------------------------------+----------------------------------------------------+

location string:
    * `host[:port][/workdir]`

supported properties:

+----------------------------+------------------------------------------------------------+-----------+---------+
| name                       | description                                                | data_type | default |
+============================+============================================================+===========+=========+
| sftp.strictHostKeyChecking | Enable strict host key checking.                           | boolean   | `true`  |
+----------------------------+------------------------------------------------------------+-----------+---------+
| sftp.loadKnownHosts        | Load the standard known_hosts file.                        | boolean   | `true`  |
+----------------------------+------------------------------------------------------------+-----------+---------+
| sftp.loadSshConfig         | Load the OpenSSH config file.                              | boolean   | `true`  |
+----------------------------+------------------------------------------------------------+-----------+---------+
| sftp.agent                 | Use a (local) ssh-agent.                                   | boolean   | `false` |
+----------------------------+------------------------------------------------------------+-----------+---------+
| sftp.agentForwarding       | Use ssh-agent forwarding when setting up a connection.     | boolean   | `false` |
+----------------------------+------------------------------------------------------------+-----------+---------+
| sftp.connection.timeout    | The timeout for creating and authenticating connections    | natural   | `10000` |
|                            | (in milliseconds).                                         |           |         |
+----------------------------+------------------------------------------------------------+-----------+---------+
| sftp.bufferSize            | The buffer size to use when copying files (in bytes).      | size      | `64K`   |
+----------------------------+------------------------------------------------------------+-----------+---------+

Ftp
~~~
The FTP adaptor implements file access on remote ftp servers.

+------------------------------------+-------------------------------------------+
| field                              | value                                     |
+====================================+===========================================+
| supports_third_party_copy          | False                                     |
+------------------------------------+-------------------------------------------+
| can_create_symboliclinks           | False                                     |
+------------------------------------+-------------------------------------------+
| can_read_symboliclinks             | True                                      |
+------------------------------------+-------------------------------------------+
| is_connectionless                  | False                                     |
+------------------------------------+-------------------------------------------+
| supported_credentials              | `DefaultCredential`, `PasswordCredential` |
+------------------------------------+-------------------------------------------+
| can_append                         | True                                      |
+------------------------------------+-------------------------------------------+
| supports_reading_posix_permissions | True                                      |
+------------------------------------+-------------------------------------------+
| supports_setting_posix_permissions | False                                     |
+------------------------------------+-------------------------------------------+
| supports_rename                    | True                                      |
+------------------------------------+-------------------------------------------+
| needs_size_beforehand              | False                                     |
+------------------------------------+-------------------------------------------+

location string:
    * `host[:port][/workdir]`

supported properties:

+----------------+-------------------------------------------------------+-----------+---------+
| name           | description                                           | data_type | default |
+================+=======================================================+===========+=========+
| ftp.bufferSize | The buffer size to use when copying files (in bytes). | size      | `64K`   |
+----------------+-------------------------------------------------------+-----------+---------+

Webdav
~~~~~~
The webdav file adaptor implements file access to remote webdav
servers.

+------------------------------------+-------------------------------------------+
| field                              | value                                     |
+====================================+===========================================+
| supports_third_party_copy          | False                                     |
+------------------------------------+-------------------------------------------+
| can_create_symboliclinks           | False                                     |
+------------------------------------+-------------------------------------------+
| can_read_symboliclinks             | False                                     |
+------------------------------------+-------------------------------------------+
| is_connectionless                  | True                                      |
+------------------------------------+-------------------------------------------+
| supported_credentials              | `DefaultCredential`, `PasswordCredential` |
+------------------------------------+-------------------------------------------+
| can_append                         | False                                     |
+------------------------------------+-------------------------------------------+
| supports_reading_posix_permissions | False                                     |
+------------------------------------+-------------------------------------------+
| supports_setting_posix_permissions | False                                     |
+------------------------------------+-------------------------------------------+
| supports_rename                    | True                                      |
+------------------------------------+-------------------------------------------+
| needs_size_beforehand              | False                                     |
+------------------------------------+-------------------------------------------+

location string:
    * `http://host[:port][/workdir]`
    * `https://host[:port][/workdir]`

supported properties:

+-------------------+-------------------------------------------------------+-----------+---------+
| name              | description                                           | data_type | default |
+===================+=======================================================+===========+=========+
| webdav.bufferSize | The buffer size to use when copying files (in bytes). | size      | `64K`   |
+-------------------+-------------------------------------------------------+-----------+---------+


Scheduler
---------

.. note:: Supported property names should be prefixed with
``"xenon.adaptors.schedulers"``.  We've left this prefix out to improve
readability of the tables.


Local
~~~~~
The local jobs adaptor implements all functionality by emulating a
local queue.

+-----------------------+---------------------+
| field                 | value               |
+=======================+=====================+
| is_embedded           | True                |
+-----------------------+---------------------+
| supports_interactive  | True                |
+-----------------------+---------------------+
| supports_batch        | True                |
+-----------------------+---------------------+
| uses_file_system      | True                |
+-----------------------+---------------------+
| supported_credentials | `DefaultCredential` |
+-----------------------+---------------------+

location string:
    * `[/workdir]`

supported properties:

+-------------------------------------+--------------------------------------------+-----------+---------+
| name                                | description                                | data_type | default |
+=====================================+============================================+===========+=========+
| local.queue.pollingDelay            | The polling delay for monitoring running   | long      | `1000`  |
|                                     | jobs (in milliseconds).                    |           |         |
+-------------------------------------+--------------------------------------------+-----------+---------+
| local.queue.multi.maxConcurrentJobs | The maximum number of concurrent jobs in   | integer   | `4`     |
|                                     | the multiq.                                |           |         |
+-------------------------------------+--------------------------------------------+-----------+---------+

Ssh
~~~
The SSH job adaptor implements all functionality to start jobs on ssh
servers.

+-----------------------+---------------------------------------------------------------------------------+
| field                 | value                                                                           |
+=======================+=================================================================================+
| is_embedded           | True                                                                            |
+-----------------------+---------------------------------------------------------------------------------+
| supports_interactive  | True                                                                            |
+-----------------------+---------------------------------------------------------------------------------+
| supports_batch        | True                                                                            |
+-----------------------+---------------------------------------------------------------------------------+
| uses_file_system      | True                                                                            |
+-----------------------+---------------------------------------------------------------------------------+
| supported_credentials | `DefaultCredential`, `CertificateCredential`, `PasswordCredential`,             |
|                       | `CredentialMap`                                                                 |
+-----------------------+---------------------------------------------------------------------------------+

location string:
    * `host[:port][/workdir][ via:otherhost[:port]]*`

supported properties:

+-----------------------------------+--------------------------------------------+-----------+---------+
| name                              | description                                | data_type | default |
+===================================+============================================+===========+=========+
| ssh.strictHostKeyChecking         | Enable strict host key checking.           | boolean   | `true`  |
+-----------------------------------+--------------------------------------------+-----------+---------+
| ssh.loadKnownHosts                | Load the standard known_hosts file.        | boolean   | `true`  |
+-----------------------------------+--------------------------------------------+-----------+---------+
| ssh.loadSshConfig                 | Load the OpenSSH config file.              | boolean   | `true`  |
+-----------------------------------+--------------------------------------------+-----------+---------+
| ssh.agent                         | Use a (local) ssh-agent.                   | boolean   | `false` |
+-----------------------------------+--------------------------------------------+-----------+---------+
| ssh.agentForwarding               | Use ssh-agent forwarding                   | boolean   | `false` |
+-----------------------------------+--------------------------------------------+-----------+---------+
| ssh.timeout                       | The timeout for the connection setup and   | long      | `10000` |
|                                   | authetication (in milliseconds).           |           |         |
+-----------------------------------+--------------------------------------------+-----------+---------+
| ssh.queue.pollingDelay            | The polling delay for monitoring running   | long      | `1000`  |
|                                   | jobs (in milliseconds).                    |           |         |
+-----------------------------------+--------------------------------------------+-----------+---------+
| ssh.queue.multi.maxConcurrentJobs | The maximum number of concurrent jobs in   | integer   | `4`     |
|                                   | the multiq..                               |           |         |
+-----------------------------------+--------------------------------------------+-----------+---------+

At
~~
The At Adaptor submits jobs to an at scheduler.  This adaptor uses
either the local or the ssh scheduler adaptor to run commands on the
machine running at,  and the file or the stfp filesystem adaptor to
gain access to the filesystem of that machine.

+-----------------------+---------------------------------------------------------------------------------+
| field                 | value                                                                           |
+=======================+=================================================================================+
| is_embedded           | False                                                                           |
+-----------------------+---------------------------------------------------------------------------------+
| supports_interactive  | False                                                                           |
+-----------------------+---------------------------------------------------------------------------------+
| supports_batch        | True                                                                            |
+-----------------------+---------------------------------------------------------------------------------+
| uses_file_system      | True                                                                            |
+-----------------------+---------------------------------------------------------------------------------+
| supported_credentials | `DefaultCredential`, `CertificateCredential`, `PasswordCredential`,             |
|                       | `CredentialMap`                                                                 |
+-----------------------+---------------------------------------------------------------------------------+

location string:
    * `local://[/workdir]`
    * `ssh://host[:port][/workdir][ via:otherhost[:port]]*`

supported properties:

+-------------------------------------+--------------------------------------------+-----------+---------+
| name                                | description                                | data_type | default |
+=====================================+============================================+===========+=========+
| at.poll.delay                       | Number of milliseconds between polling the | long      | `1000`  |
|                                     | status of a job.                           |           |         |
+-------------------------------------+--------------------------------------------+-----------+---------+
| ssh.strictHostKeyChecking           | Enable strict host key checking.           | boolean   | `true`  |
+-------------------------------------+--------------------------------------------+-----------+---------+
| ssh.loadKnownHosts                  | Load the standard known_hosts file.        | boolean   | `true`  |
+-------------------------------------+--------------------------------------------+-----------+---------+
| ssh.loadSshConfig                   | Load the OpenSSH config file.              | boolean   | `true`  |
+-------------------------------------+--------------------------------------------+-----------+---------+
| ssh.agent                           | Use a (local) ssh-agent.                   | boolean   | `false` |
+-------------------------------------+--------------------------------------------+-----------+---------+
| ssh.agentForwarding                 | Use ssh-agent forwarding                   | boolean   | `false` |
+-------------------------------------+--------------------------------------------+-----------+---------+
| ssh.timeout                         | The timeout for the connection setup and   | long      | `10000` |
|                                     | authetication (in milliseconds).           |           |         |
+-------------------------------------+--------------------------------------------+-----------+---------+
| ssh.queue.pollingDelay              | The polling delay for monitoring running   | long      | `1000`  |
|                                     | jobs (in milliseconds).                    |           |         |
+-------------------------------------+--------------------------------------------+-----------+---------+
| ssh.queue.multi.maxConcurrentJobs   | The maximum number of concurrent jobs in   | integer   | `4`     |
|                                     | the multiq..                               |           |         |
+-------------------------------------+--------------------------------------------+-----------+---------+
| local.queue.pollingDelay            | The polling delay for monitoring running   | long      | `1000`  |
|                                     | jobs (in milliseconds).                    |           |         |
+-------------------------------------+--------------------------------------------+-----------+---------+
| local.queue.multi.maxConcurrentJobs | The maximum number of concurrent jobs in   | integer   | `4`     |
|                                     | the multiq.                                |           |         |
+-------------------------------------+--------------------------------------------+-----------+---------+

Slurm
~~~~~
The Slurm Adaptor submits jobs to a Slurm scheduler.  This adaptor
uses either the local or the ssh scheduler adaptor to run commands on
the machine running Slurm,  and the file or the stfp filesystem
adaptor to gain access to the filesystem of that machine.

+-----------------------+---------------------------------------------------------------------------------+
| field                 | value                                                                           |
+=======================+=================================================================================+
| is_embedded           | False                                                                           |
+-----------------------+---------------------------------------------------------------------------------+
| supports_interactive  | True                                                                            |
+-----------------------+---------------------------------------------------------------------------------+
| supports_batch        | True                                                                            |
+-----------------------+---------------------------------------------------------------------------------+
| uses_file_system      | True                                                                            |
+-----------------------+---------------------------------------------------------------------------------+
| supported_credentials | `DefaultCredential`, `CertificateCredential`, `PasswordCredential`,             |
|                       | `CredentialMap`                                                                 |
+-----------------------+---------------------------------------------------------------------------------+

location string:
    * `local://[/workdir]`
    * `ssh://host[:port][/workdir][ via:otherhost[:port]]*`

supported properties:

+-------------------------------------+--------------------------------------------+-----------+---------+
| name                                | description                                | data_type | default |
+=====================================+============================================+===========+=========+
| slurm.disable.accounting.usage      | Do not use accounting info of slurm, even  | boolean   | `false` |
|                                     | when available. Mostly for testing         |           |         |
|                                     | purposes                                   |           |         |
+-------------------------------------+--------------------------------------------+-----------+---------+
| slurm.poll.delay                    | Number of milliseconds between polling the | long      | `1000`  |
|                                     | status of a job.                           |           |         |
+-------------------------------------+--------------------------------------------+-----------+---------+
| ssh.strictHostKeyChecking           | Enable strict host key checking.           | boolean   | `true`  |
+-------------------------------------+--------------------------------------------+-----------+---------+
| ssh.loadKnownHosts                  | Load the standard known_hosts file.        | boolean   | `true`  |
+-------------------------------------+--------------------------------------------+-----------+---------+
| ssh.loadSshConfig                   | Load the OpenSSH config file.              | boolean   | `true`  |
+-------------------------------------+--------------------------------------------+-----------+---------+
| ssh.agent                           | Use a (local) ssh-agent.                   | boolean   | `false` |
+-------------------------------------+--------------------------------------------+-----------+---------+
| ssh.agentForwarding                 | Use ssh-agent forwarding                   | boolean   | `false` |
+-------------------------------------+--------------------------------------------+-----------+---------+
| ssh.timeout                         | The timeout for the connection setup and   | long      | `10000` |
|                                     | authetication (in milliseconds).           |           |         |
+-------------------------------------+--------------------------------------------+-----------+---------+
| ssh.queue.pollingDelay              | The polling delay for monitoring running   | long      | `1000`  |
|                                     | jobs (in milliseconds).                    |           |         |
+-------------------------------------+--------------------------------------------+-----------+---------+
| ssh.queue.multi.maxConcurrentJobs   | The maximum number of concurrent jobs in   | integer   | `4`     |
|                                     | the multiq..                               |           |         |
+-------------------------------------+--------------------------------------------+-----------+---------+
| local.queue.pollingDelay            | The polling delay for monitoring running   | long      | `1000`  |
|                                     | jobs (in milliseconds).                    |           |         |
+-------------------------------------+--------------------------------------------+-----------+---------+
| local.queue.multi.maxConcurrentJobs | The maximum number of concurrent jobs in   | integer   | `4`     |
|                                     | the multiq.                                |           |         |
+-------------------------------------+--------------------------------------------+-----------+---------+

Gridengine
~~~~~~~~~~
The SGE Adaptor submits jobs to a (Sun/Oracle/Univa) Grid Engine
scheduler. This adaptor uses either the local or the ssh scheduler
adaptor to run commands on the machine running Grid Engine,  and the
file or the stfp filesystem adaptor to gain access to the filesystem
of that machine.

+-----------------------+---------------------------------------------------------------------------------+
| field                 | value                                                                           |
+=======================+=================================================================================+
| is_embedded           | False                                                                           |
+-----------------------+---------------------------------------------------------------------------------+
| supports_interactive  | False                                                                           |
+-----------------------+---------------------------------------------------------------------------------+
| supports_batch        | True                                                                            |
+-----------------------+---------------------------------------------------------------------------------+
| uses_file_system      | True                                                                            |
+-----------------------+---------------------------------------------------------------------------------+
| supported_credentials | `DefaultCredential`, `CertificateCredential`, `PasswordCredential`,             |
|                       | `CredentialMap`                                                                 |
+-----------------------+---------------------------------------------------------------------------------+

location string:
    * `local://[/workdir]`
    * `ssh://host[:port][/workdir][ via:otherhost[:port]]*`

supported properties:

+-------------------------------------+--------------------------------------------+-----------+---------+
| name                                | description                                | data_type | default |
+=====================================+============================================+===========+=========+
| gridengine.ignore.version           | Skip version check is skipped when         | boolean   | `false` |
|                                     | connecting to remote machines. WARNING: it |           |         |
|                                     | is not recommended to use this setting in  |           |         |
|                                     | production environments!                   |           |         |
+-------------------------------------+--------------------------------------------+-----------+---------+
| gridengine.accounting.grace.time    | Number of milliseconds a job is allowed to | long      | `60000` |
|                                     | take going from the queue to the qacct     |           |         |
|                                     | output.                                    |           |         |
+-------------------------------------+--------------------------------------------+-----------+---------+
| gridengine.poll.delay               | Number of milliseconds between polling the | long      | `1000`  |
|                                     | status of a job.                           |           |         |
+-------------------------------------+--------------------------------------------+-----------+---------+
| ssh.strictHostKeyChecking           | Enable strict host key checking.           | boolean   | `true`  |
+-------------------------------------+--------------------------------------------+-----------+---------+
| ssh.loadKnownHosts                  | Load the standard known_hosts file.        | boolean   | `true`  |
+-------------------------------------+--------------------------------------------+-----------+---------+
| ssh.loadSshConfig                   | Load the OpenSSH config file.              | boolean   | `true`  |
+-------------------------------------+--------------------------------------------+-----------+---------+
| ssh.agent                           | Use a (local) ssh-agent.                   | boolean   | `false` |
+-------------------------------------+--------------------------------------------+-----------+---------+
| ssh.agentForwarding                 | Use ssh-agent forwarding                   | boolean   | `false` |
+-------------------------------------+--------------------------------------------+-----------+---------+
| ssh.timeout                         | The timeout for the connection setup and   | long      | `10000` |
|                                     | authetication (in milliseconds).           |           |         |
+-------------------------------------+--------------------------------------------+-----------+---------+
| ssh.queue.pollingDelay              | The polling delay for monitoring running   | long      | `1000`  |
|                                     | jobs (in milliseconds).                    |           |         |
+-------------------------------------+--------------------------------------------+-----------+---------+
| ssh.queue.multi.maxConcurrentJobs   | The maximum number of concurrent jobs in   | integer   | `4`     |
|                                     | the multiq..                               |           |         |
+-------------------------------------+--------------------------------------------+-----------+---------+
| local.queue.pollingDelay            | The polling delay for monitoring running   | long      | `1000`  |
|                                     | jobs (in milliseconds).                    |           |         |
+-------------------------------------+--------------------------------------------+-----------+---------+
| local.queue.multi.maxConcurrentJobs | The maximum number of concurrent jobs in   | integer   | `4`     |
|                                     | the multiq.                                |           |         |
+-------------------------------------+--------------------------------------------+-----------+---------+

Torque
~~~~~~
The Torque Adaptor submits jobs to a TORQUE batch system. This adaptor
uses either the local or the ssh scheduler adaptor to run commands on
the machine running TORQUE,  and the file or the stfp filesystem
adaptor to gain access to the filesystem of that machine.

+-----------------------+---------------------------------------------------------------------------------+
| field                 | value                                                                           |
+=======================+=================================================================================+
| is_embedded           | False                                                                           |
+-----------------------+---------------------------------------------------------------------------------+
| supports_interactive  | False                                                                           |
+-----------------------+---------------------------------------------------------------------------------+
| supports_batch        | True                                                                            |
+-----------------------+---------------------------------------------------------------------------------+
| uses_file_system      | True                                                                            |
+-----------------------+---------------------------------------------------------------------------------+
| supported_credentials | `DefaultCredential`, `CertificateCredential`, `PasswordCredential`,             |
|                       | `CredentialMap`                                                                 |
+-----------------------+---------------------------------------------------------------------------------+

location string:
    * `local://[/workdir]`
    * `ssh://host[:port][/workdir][ via:otherhost[:port]]*`

supported properties:

+-------------------------------------+--------------------------------------------+-----------+---------+
| name                                | description                                | data_type | default |
+=====================================+============================================+===========+=========+
| torque.ignore.version               | Skip version check is skipped when         | boolean   | `false` |
|                                     | connecting to remote machines. WARNING: it |           |         |
|                                     | is not recommended to use this setting in  |           |         |
|                                     | production environments!                   |           |         |
+-------------------------------------+--------------------------------------------+-----------+---------+
| torque.accounting.grace.time        | Number of milliseconds a job is allowed to | long      | `60000` |
|                                     | take going from the queue to the accinfo   |           |         |
|                                     | output.                                    |           |         |
+-------------------------------------+--------------------------------------------+-----------+---------+
| torque.poll.delay                   | Number of milliseconds between polling the | long      | `1000`  |
|                                     | status of a job.                           |           |         |
+-------------------------------------+--------------------------------------------+-----------+---------+
| ssh.strictHostKeyChecking           | Enable strict host key checking.           | boolean   | `true`  |
+-------------------------------------+--------------------------------------------+-----------+---------+
| ssh.loadKnownHosts                  | Load the standard known_hosts file.        | boolean   | `true`  |
+-------------------------------------+--------------------------------------------+-----------+---------+
| ssh.loadSshConfig                   | Load the OpenSSH config file.              | boolean   | `true`  |
+-------------------------------------+--------------------------------------------+-----------+---------+
| ssh.agent                           | Use a (local) ssh-agent.                   | boolean   | `false` |
+-------------------------------------+--------------------------------------------+-----------+---------+
| ssh.agentForwarding                 | Use ssh-agent forwarding                   | boolean   | `false` |
+-------------------------------------+--------------------------------------------+-----------+---------+
| ssh.timeout                         | The timeout for the connection setup and   | long      | `10000` |
|                                     | authetication (in milliseconds).           |           |         |
+-------------------------------------+--------------------------------------------+-----------+---------+
| ssh.queue.pollingDelay              | The polling delay for monitoring running   | long      | `1000`  |
|                                     | jobs (in milliseconds).                    |           |         |
+-------------------------------------+--------------------------------------------+-----------+---------+
| ssh.queue.multi.maxConcurrentJobs   | The maximum number of concurrent jobs in   | integer   | `4`     |
|                                     | the multiq..                               |           |         |
+-------------------------------------+--------------------------------------------+-----------+---------+
| local.queue.pollingDelay            | The polling delay for monitoring running   | long      | `1000`  |
|                                     | jobs (in milliseconds).                    |           |         |
+-------------------------------------+--------------------------------------------+-----------+---------+
| local.queue.multi.maxConcurrentJobs | The maximum number of concurrent jobs in   | integer   | `4`     |
|                                     | the multiq.                                |           |         |
+-------------------------------------+--------------------------------------------+-----------+---------+

