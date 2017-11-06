Adaptors
========
This section contains the adaptor documentation which is generated from the
information provided by the adaptors themselves.

.. note:: All supported property names should be prefixed with ``"xenon.adaptors."``.
    We've left this prefix out for readability of the tables.

.. contents::


File System
-----------

File
~~~~
This is the local file adaptor that implements file functionality for
local access.

+---------------------------+-------+
| field                     | value |
+===========================+=======+
| supports_third_party_copy | False |
+---------------------------+-------+
| can_create_symboliclinks  | False |
+---------------------------+-------+
| can_read_symboliclinks    | False |
+---------------------------+-------+
| is_connectionless         | False |
+---------------------------+-------+

location string:
    * `(null)`
    * `(empty string)`
    * `[/workdir]`
    * `driveletter:[/workdir]`

supported properties:

+-----------------------------+-------------------------------------------------------+-----------+---------+
| name                        | description                                           | data_type | default |
+=============================+=======================================================+===========+=========+
| filesystems.file.bufferSize | The buffer size to use when copying files (in bytes). | size      | `64K`   |
+-----------------------------+-------------------------------------------------------+-----------+---------+

Ftp
~~~
The FTP adaptor implements file access on remote ftp servers.

+---------------------------+-------+
| field                     | value |
+===========================+=======+
| supports_third_party_copy | False |
+---------------------------+-------+
| can_create_symboliclinks  | False |
+---------------------------+-------+
| can_read_symboliclinks    | False |
+---------------------------+-------+
| is_connectionless         | False |
+---------------------------+-------+

location string:
    * `host[:port][/workdir]`

supported properties:

+----------------------------+-------------------------------------------------------+-----------+---------+
| name                       | description                                           | data_type | default |
+============================+=======================================================+===========+=========+
| filesystems.ftp.bufferSize | The buffer size to use when copying files (in bytes). | size      | `64K`   |
+----------------------------+-------------------------------------------------------+-----------+---------+

Sftp
~~~~
The SFTP adaptor implements all file access functionality to remote
SFTP servers

+---------------------------+-------+
| field                     | value |
+===========================+=======+
| supports_third_party_copy | False |
+---------------------------+-------+
| can_create_symboliclinks  | False |
+---------------------------+-------+
| can_read_symboliclinks    | False |
+---------------------------+-------+
| is_connectionless         | False |
+---------------------------+-------+

location string:
    * `host[:port][/workdir]`

supported properties:

+----------------------------------------+--------------------------------------------+-----------+---------+
| name                                   | description                                | data_type | default |
+========================================+============================================+===========+=========+
| filesystems.sftp.autoAddHostKey        | Automatically add unknown host keys to     | boolean   | `true`  |
|                                        | known_hosts.                               |           |         |
+----------------------------------------+--------------------------------------------+-----------+---------+
| filesystems.sftp.strictHostKeyChecking | Enable strict host key checking.           | boolean   | `true`  |
+----------------------------------------+--------------------------------------------+-----------+---------+
| filesystems.sftp.loadKnownHosts        | Load the standard known_hosts file.        | boolean   | `true`  |
+----------------------------------------+--------------------------------------------+-----------+---------+
| filesystems.sftp.loadSshConfig         | Load the OpenSSH config file.              | boolean   | `true`  |
+----------------------------------------+--------------------------------------------+-----------+---------+
| filesystems.sftp.sshConfigFile         | OpenSSH config filename.                   | string    | (empty) |
+----------------------------------------+--------------------------------------------+-----------+---------+
| filesystems.sftp.agent                 | Use a (local) ssh-agent.                   | boolean   | `false` |
+----------------------------------------+--------------------------------------------+-----------+---------+
| filesystems.sftp.agentForwarding       | Use ssh-agent forwarding when setting up a | boolean   | `false` |
|                                        | connection.                                |           |         |
+----------------------------------------+--------------------------------------------+-----------+---------+
| filesystems.sftp.connection.timeout    | The timeout for creating and               | natural   | `10000` |
|                                        | authenticating connections (in             |           |         |
|                                        | milliseconds).                             |           |         |
+----------------------------------------+--------------------------------------------+-----------+---------+
| filesystems.sftp.bufferSize            | The buffer size to use when copying files  | size      | `64K`   |
|                                        | (in bytes).                                |           |         |
+----------------------------------------+--------------------------------------------+-----------+---------+

Webdav
~~~~~~
The webdav file adaptor implements file access to remote webdav
servers.

+---------------------------+-------+
| field                     | value |
+===========================+=======+
| supports_third_party_copy | False |
+---------------------------+-------+
| can_create_symboliclinks  | False |
+---------------------------+-------+
| can_read_symboliclinks    | False |
+---------------------------+-------+
| is_connectionless         | False |
+---------------------------+-------+

location string:
    * `http://host[:port][/workdir]`
    * `https://host[:port][/workdir]`

supported properties:

+-------------------------------+-------------------------------------------------------+-----------+---------+
| name                          | description                                           | data_type | default |
+===============================+=======================================================+===========+=========+
| filesystems.webdav.bufferSize | The buffer size to use when copying files (in bytes). | size      | `64K`   |
+-------------------------------+-------------------------------------------------------+-----------+---------+

S3
~~
The JClouds adaptor uses Apache JClouds to talk to s3 and others

+---------------------------+-------+
| field                     | value |
+===========================+=======+
| supports_third_party_copy | False |
+---------------------------+-------+
| can_create_symboliclinks  | False |
+---------------------------+-------+
| can_read_symboliclinks    | False |
+---------------------------+-------+
| is_connectionless         | False |
+---------------------------+-------+

location string:
    * `[http://host[:port]]/bucketname[/workdir]`

supported properties:

+---------------------------+-------------------------------------------------------+-----------+---------+
| name                      | description                                           | data_type | default |
+===========================+=======================================================+===========+=========+
| filesystems.s3.bufferSize | The buffer size to use when copying files (in bytes). | size      | `64K`   |
+---------------------------+-------------------------------------------------------+-----------+---------+


Scheduler
---------

Local
~~~~~
The local jobs adaptor implements all functionality by emulating a
local queue.

+----------------------+-------+
| field                | value |
+======================+=======+
| is_embedded          | True  |
+----------------------+-------+
| supports_interactive | True  |
+----------------------+-------+
| supports_batch       | True  |
+----------------------+-------+
| uses_file_system     | True  |
+----------------------+-------+

location string:
    * `[/workdir]`

supported properties:

+------------------------------------------------+--------------------------------------------+-----------+---------+
| name                                           | description                                | data_type | default |
+================================================+============================================+===========+=========+
| schedulers.local.queue.pollingDelay            | The polling delay for monitoring running   | long      | `1000`  |
|                                                | jobs (in milliseconds).                    |           |         |
+------------------------------------------------+--------------------------------------------+-----------+---------+
| schedulers.local.queue.multi.maxConcurrentJobs | The maximum number of concurrent jobs in   | integer   | `4`     |
|                                                | the multiq.                                |           |         |
+------------------------------------------------+--------------------------------------------+-----------+---------+

Ssh
~~~
The SSH job adaptor implements all functionality to start jobs on ssh
servers.

+----------------------+-------+
| field                | value |
+======================+=======+
| is_embedded          | True  |
+----------------------+-------+
| supports_interactive | True  |
+----------------------+-------+
| supports_batch       | True  |
+----------------------+-------+
| uses_file_system     | True  |
+----------------------+-------+

location string:
    * `host[:port][/workdir][ via:otherhost[:port]]*`

supported properties:

+----------------------------------------------+--------------------------------------------+-----------+---------+
| name                                         | description                                | data_type | default |
+==============================================+============================================+===========+=========+
| schedulers.ssh.autoAddHostKey                | Automatically add unknown host keys to     | boolean   | `true`  |
|                                              | known_hosts.                               |           |         |
+----------------------------------------------+--------------------------------------------+-----------+---------+
| schedulers.ssh.strictHostKeyChecking         | Enable strict host key checking.           | boolean   | `true`  |
+----------------------------------------------+--------------------------------------------+-----------+---------+
| schedulers.ssh.loadKnownHosts                | Load the standard known_hosts file.        | boolean   | `true`  |
+----------------------------------------------+--------------------------------------------+-----------+---------+
| schedulers.ssh.loadSshConfig                 | Load the OpenSSH config file.              | boolean   | `true`  |
+----------------------------------------------+--------------------------------------------+-----------+---------+
| schedulers.ssh.sshConfigFile                 | OpenSSH config filename.                   | string    | (empty) |
+----------------------------------------------+--------------------------------------------+-----------+---------+
| schedulers.ssh.agent                         | Use a (local) ssh-agent.                   | boolean   | `false` |
+----------------------------------------------+--------------------------------------------+-----------+---------+
| schedulers.ssh.agentForwarding               | Use ssh-agent forwarding                   | boolean   | `false` |
+----------------------------------------------+--------------------------------------------+-----------+---------+
| schedulers.ssh.timeout                       | The timeout for the connection setup and   | long      | `10000` |
|                                              | authetication (in milliseconds).           |           |         |
+----------------------------------------------+--------------------------------------------+-----------+---------+
| schedulers.ssh.queue.pollingDelay            | The polling delay for monitoring running   | long      | `1000`  |
|                                              | jobs (in milliseconds).                    |           |         |
+----------------------------------------------+--------------------------------------------+-----------+---------+
| schedulers.ssh.queue.multi.maxConcurrentJobs | The maximum number of concurrent jobs in   | integer   | `4`     |
|                                              | the multiq..                               |           |         |
+----------------------------------------------+--------------------------------------------+-----------+---------+
| schedulers.ssh.gateway                       | The gateway machine used to create an SSH  | string    | (empty) |
|                                              | tunnel to the target.                      |           |         |
+----------------------------------------------+--------------------------------------------+-----------+---------+

Gridengine
~~~~~~~~~~
The SGE Adaptor submits jobs to a (Sun/Ocacle/Univa) Grid Engine
scheduler. This adaptor uses either the local or the ssh scheduler
adaptor to run commands on the machine running Grid Engine,  and the
file or the stfp filesystem adaptor to gain access to the filesystem
of that machine.

+----------------------+-------+
| field                | value |
+======================+=======+
| is_embedded          | False |
+----------------------+-------+
| supports_interactive | False |
+----------------------+-------+
| supports_batch       | True  |
+----------------------+-------+
| uses_file_system     | True  |
+----------------------+-------+

location string:
    * `local://[/workdir]`
    * `ssh://host[:port][/workdir][ via:otherhost[:port]]*`

supported properties:

+------------------------------------------------+--------------------------------------------+-----------+---------+
| name                                           | description                                | data_type | default |
+================================================+============================================+===========+=========+
| schedulers.gridengine.ignore.version           | Skip version check is skipped when         | boolean   | `false` |
|                                                | connecting to remote machines. WARNING: it |           |         |
|                                                | is not recommended to use this setting in  |           |         |
|                                                | production environments!                   |           |         |
+------------------------------------------------+--------------------------------------------+-----------+---------+
| schedulers.gridengine.accounting.grace.time    | Number of milliseconds a job is allowed to | long      | `60000` |
|                                                | take going from the queue to the qacct     |           |         |
|                                                | output.                                    |           |         |
+------------------------------------------------+--------------------------------------------+-----------+---------+
| schedulers.gridengine.poll.delay               | Number of milliseconds between polling the | long      | `1000`  |
|                                                | status of a job.                           |           |         |
+------------------------------------------------+--------------------------------------------+-----------+---------+
| schedulers.ssh.autoAddHostKey                  | Automatically add unknown host keys to     | boolean   | `true`  |
|                                                | known_hosts.                               |           |         |
+------------------------------------------------+--------------------------------------------+-----------+---------+
| schedulers.ssh.strictHostKeyChecking           | Enable strict host key checking.           | boolean   | `true`  |
+------------------------------------------------+--------------------------------------------+-----------+---------+
| schedulers.ssh.loadKnownHosts                  | Load the standard known_hosts file.        | boolean   | `true`  |
+------------------------------------------------+--------------------------------------------+-----------+---------+
| schedulers.ssh.loadSshConfig                   | Load the OpenSSH config file.              | boolean   | `true`  |
+------------------------------------------------+--------------------------------------------+-----------+---------+
| schedulers.ssh.sshConfigFile                   | OpenSSH config filename.                   | string    | (empty) |
+------------------------------------------------+--------------------------------------------+-----------+---------+
| schedulers.ssh.agent                           | Use a (local) ssh-agent.                   | boolean   | `false` |
+------------------------------------------------+--------------------------------------------+-----------+---------+
| schedulers.ssh.agentForwarding                 | Use ssh-agent forwarding                   | boolean   | `false` |
+------------------------------------------------+--------------------------------------------+-----------+---------+
| schedulers.ssh.timeout                         | The timeout for the connection setup and   | long      | `10000` |
|                                                | authetication (in milliseconds).           |           |         |
+------------------------------------------------+--------------------------------------------+-----------+---------+
| schedulers.ssh.queue.pollingDelay              | The polling delay for monitoring running   | long      | `1000`  |
|                                                | jobs (in milliseconds).                    |           |         |
+------------------------------------------------+--------------------------------------------+-----------+---------+
| schedulers.ssh.queue.multi.maxConcurrentJobs   | The maximum number of concurrent jobs in   | integer   | `4`     |
|                                                | the multiq..                               |           |         |
+------------------------------------------------+--------------------------------------------+-----------+---------+
| schedulers.ssh.gateway                         | The gateway machine used to create an SSH  | string    | (empty) |
|                                                | tunnel to the target.                      |           |         |
+------------------------------------------------+--------------------------------------------+-----------+---------+
| schedulers.local.queue.pollingDelay            | The polling delay for monitoring running   | long      | `1000`  |
|                                                | jobs (in milliseconds).                    |           |         |
+------------------------------------------------+--------------------------------------------+-----------+---------+
| schedulers.local.queue.multi.maxConcurrentJobs | The maximum number of concurrent jobs in   | integer   | `4`     |
|                                                | the multiq.                                |           |         |
+------------------------------------------------+--------------------------------------------+-----------+---------+

Slurm
~~~~~
The Slurm Adaptor submits jobs to a Slurm scheduler.  This adaptor
uses either the local or the ssh scheduler adaptor to run commands on
the machine running Slurm,  and the file or the stfp filesystem
adaptor to gain access to the filesystem of that machine.

+----------------------+-------+
| field                | value |
+======================+=======+
| is_embedded          | False |
+----------------------+-------+
| supports_interactive | True  |
+----------------------+-------+
| supports_batch       | True  |
+----------------------+-------+
| uses_file_system     | True  |
+----------------------+-------+

location string:
    * `local://[/workdir]`
    * `ssh://host[:port][/workdir][ via:otherhost[:port]]*`

supported properties:

+------------------------------------------------+--------------------------------------------+-----------+---------+
| name                                           | description                                | data_type | default |
+================================================+============================================+===========+=========+
| schedulers.slurm.disable.accounting.usage      | Do not use accounting info of slurm, even  | boolean   | `false` |
|                                                | when available. Mostly for testing         |           |         |
|                                                | purposes                                   |           |         |
+------------------------------------------------+--------------------------------------------+-----------+---------+
| schedulers.slurm.poll.delay                    | Number of milliseconds between polling the | long      | `1000`  |
|                                                | status of a job.                           |           |         |
+------------------------------------------------+--------------------------------------------+-----------+---------+
| schedulers.ssh.autoAddHostKey                  | Automatically add unknown host keys to     | boolean   | `true`  |
|                                                | known_hosts.                               |           |         |
+------------------------------------------------+--------------------------------------------+-----------+---------+
| schedulers.ssh.strictHostKeyChecking           | Enable strict host key checking.           | boolean   | `true`  |
+------------------------------------------------+--------------------------------------------+-----------+---------+
| schedulers.ssh.loadKnownHosts                  | Load the standard known_hosts file.        | boolean   | `true`  |
+------------------------------------------------+--------------------------------------------+-----------+---------+
| schedulers.ssh.loadSshConfig                   | Load the OpenSSH config file.              | boolean   | `true`  |
+------------------------------------------------+--------------------------------------------+-----------+---------+
| schedulers.ssh.sshConfigFile                   | OpenSSH config filename.                   | string    | (empty) |
+------------------------------------------------+--------------------------------------------+-----------+---------+
| schedulers.ssh.agent                           | Use a (local) ssh-agent.                   | boolean   | `false` |
+------------------------------------------------+--------------------------------------------+-----------+---------+
| schedulers.ssh.agentForwarding                 | Use ssh-agent forwarding                   | boolean   | `false` |
+------------------------------------------------+--------------------------------------------+-----------+---------+
| schedulers.ssh.timeout                         | The timeout for the connection setup and   | long      | `10000` |
|                                                | authetication (in milliseconds).           |           |         |
+------------------------------------------------+--------------------------------------------+-----------+---------+
| schedulers.ssh.queue.pollingDelay              | The polling delay for monitoring running   | long      | `1000`  |
|                                                | jobs (in milliseconds).                    |           |         |
+------------------------------------------------+--------------------------------------------+-----------+---------+
| schedulers.ssh.queue.multi.maxConcurrentJobs   | The maximum number of concurrent jobs in   | integer   | `4`     |
|                                                | the multiq..                               |           |         |
+------------------------------------------------+--------------------------------------------+-----------+---------+
| schedulers.ssh.gateway                         | The gateway machine used to create an SSH  | string    | (empty) |
|                                                | tunnel to the target.                      |           |         |
+------------------------------------------------+--------------------------------------------+-----------+---------+
| schedulers.local.queue.pollingDelay            | The polling delay for monitoring running   | long      | `1000`  |
|                                                | jobs (in milliseconds).                    |           |         |
+------------------------------------------------+--------------------------------------------+-----------+---------+
| schedulers.local.queue.multi.maxConcurrentJobs | The maximum number of concurrent jobs in   | integer   | `4`     |
|                                                | the multiq.                                |           |         |
+------------------------------------------------+--------------------------------------------+-----------+---------+

Torque
~~~~~~
The Torque Adaptor submits jobs to a TORQUE batch system. This adaptor
uses either the local or the ssh scheduler adaptor to run commands on
the machine running TORQUE,  and the file or the stfp filesystem
adaptor to gain access to the filesystem of that machine.

+----------------------+-------+
| field                | value |
+======================+=======+
| is_embedded          | False |
+----------------------+-------+
| supports_interactive | False |
+----------------------+-------+
| supports_batch       | True  |
+----------------------+-------+
| uses_file_system     | True  |
+----------------------+-------+

location string:
    * `local://[/workdir]`
    * `ssh://host[:port][/workdir][ via:otherhost[:port]]*`

supported properties:

+------------------------------------------------+--------------------------------------------+-----------+---------+
| name                                           | description                                | data_type | default |
+================================================+============================================+===========+=========+
| schedulers.torque.ignore.version               | Skip version check is skipped when         | boolean   | `false` |
|                                                | connecting to remote machines. WARNING: it |           |         |
|                                                | is not recommended to use this setting in  |           |         |
|                                                | production environments!                   |           |         |
+------------------------------------------------+--------------------------------------------+-----------+---------+
| schedulers.torque.accounting.grace.time        | Number of milliseconds a job is allowed to | long      | `60000` |
|                                                | take going from the queue to the accinfo   |           |         |
|                                                | output.                                    |           |         |
+------------------------------------------------+--------------------------------------------+-----------+---------+
| schedulers.torque.poll.delay                   | Number of milliseconds between polling the | long      | `1000`  |
|                                                | status of a job.                           |           |         |
+------------------------------------------------+--------------------------------------------+-----------+---------+
| schedulers.ssh.autoAddHostKey                  | Automatically add unknown host keys to     | boolean   | `true`  |
|                                                | known_hosts.                               |           |         |
+------------------------------------------------+--------------------------------------------+-----------+---------+
| schedulers.ssh.strictHostKeyChecking           | Enable strict host key checking.           | boolean   | `true`  |
+------------------------------------------------+--------------------------------------------+-----------+---------+
| schedulers.ssh.loadKnownHosts                  | Load the standard known_hosts file.        | boolean   | `true`  |
+------------------------------------------------+--------------------------------------------+-----------+---------+
| schedulers.ssh.loadSshConfig                   | Load the OpenSSH config file.              | boolean   | `true`  |
+------------------------------------------------+--------------------------------------------+-----------+---------+
| schedulers.ssh.sshConfigFile                   | OpenSSH config filename.                   | string    | (empty) |
+------------------------------------------------+--------------------------------------------+-----------+---------+
| schedulers.ssh.agent                           | Use a (local) ssh-agent.                   | boolean   | `false` |
+------------------------------------------------+--------------------------------------------+-----------+---------+
| schedulers.ssh.agentForwarding                 | Use ssh-agent forwarding                   | boolean   | `false` |
+------------------------------------------------+--------------------------------------------+-----------+---------+
| schedulers.ssh.timeout                         | The timeout for the connection setup and   | long      | `10000` |
|                                                | authetication (in milliseconds).           |           |         |
+------------------------------------------------+--------------------------------------------+-----------+---------+
| schedulers.ssh.queue.pollingDelay              | The polling delay for monitoring running   | long      | `1000`  |
|                                                | jobs (in milliseconds).                    |           |         |
+------------------------------------------------+--------------------------------------------+-----------+---------+
| schedulers.ssh.queue.multi.maxConcurrentJobs   | The maximum number of concurrent jobs in   | integer   | `4`     |
|                                                | the multiq..                               |           |         |
+------------------------------------------------+--------------------------------------------+-----------+---------+
| schedulers.ssh.gateway                         | The gateway machine used to create an SSH  | string    | (empty) |
|                                                | tunnel to the target.                      |           |         |
+------------------------------------------------+--------------------------------------------+-----------+---------+
| schedulers.local.queue.pollingDelay            | The polling delay for monitoring running   | long      | `1000`  |
|                                                | jobs (in milliseconds).                    |           |         |
+------------------------------------------------+--------------------------------------------+-----------+---------+
| schedulers.local.queue.multi.maxConcurrentJobs | The maximum number of concurrent jobs in   | integer   | `4`     |
|                                                | the multiq.                                |           |         |
+------------------------------------------------+--------------------------------------------+-----------+---------+

