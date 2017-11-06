Adaptors
========
This section contains the adaptor documentation which is generated from the
information provided by the adaptors themselves.

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

+------------+-------------------------------------------+------+-------+
| name       | description                               | data | defau |
|            |                                           | _typ | lt    |
|            |                                           | e    |       |
+============+===========================================+======+=======+
| bufferSize | The buffer size to use when copying files | size | `64K` |
|            | (in bytes).                               |      |       |
+------------+-------------------------------------------+------+-------+

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

+------------+-------------------------------------------+------+-------+
| name       | description                               | data | defau |
|            |                                           | _typ | lt    |
|            |                                           | e    |       |
+============+===========================================+======+=======+
| bufferSize | The buffer size to use when copying files | size | `64K` |
|            | (in bytes).                               |      |       |
+------------+-------------------------------------------+------+-------+

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

+-----------------------+----------------------------------+---------+---------+
| name                  | description                      | data_ty | default |
|                       |                                  | pe      |         |
+=======================+==================================+=========+=========+
| autoAddHostKey        | Automatically add unknown host   | boolean | `true`  |
|                       | keys to known_hosts.             |         |         |
+-----------------------+----------------------------------+---------+---------+
| strictHostKeyChecking | Enable strict host key checking. | boolean | `true`  |
+-----------------------+----------------------------------+---------+---------+
| loadKnownHosts        | Load the standard known_hosts    | boolean | `true`  |
|                       | file.                            |         |         |
+-----------------------+----------------------------------+---------+---------+
| loadSshConfig         | Load the OpenSSH config file.    | boolean | `true`  |
+-----------------------+----------------------------------+---------+---------+
| sshConfigFile         | OpenSSH config filename.         | string  | (empty) |
+-----------------------+----------------------------------+---------+---------+
| agent                 | Use a (local) ssh-agent.         | boolean | `false` |
+-----------------------+----------------------------------+---------+---------+
| agentForwarding       | Use ssh-agent forwarding when    | boolean | `false` |
|                       | setting up a connection.         |         |         |
+-----------------------+----------------------------------+---------+---------+
| connection.timeout    | The timeout for creating and     | natural | `10000` |
|                       | authenticating connections (in   |         |         |
|                       | milliseconds).                   |         |         |
+-----------------------+----------------------------------+---------+---------+
| bufferSize            | The buffer size to use when      | size    | `64K`   |
|                       | copying files (in bytes).        |         |         |
+-----------------------+----------------------------------+---------+---------+

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

+------------+-------------------------------------------+------+-------+
| name       | description                               | data | defau |
|            |                                           | _typ | lt    |
|            |                                           | e    |       |
+============+===========================================+======+=======+
| bufferSize | The buffer size to use when copying files | size | `64K` |
|            | (in bytes).                               |      |       |
+------------+-------------------------------------------+------+-------+

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

+------------+-------------------------------------------+------+-------+
| name       | description                               | data | defau |
|            |                                           | _typ | lt    |
|            |                                           | e    |       |
+============+===========================================+======+=======+
| bufferSize | The buffer size to use when copying files | size | `64K` |
|            | (in bytes).                               |      |       |
+------------+-------------------------------------------+------+-------+


Scheduler
---------

Local
~~~~~
The local jobs adaptor implements all functionality by emulating a
local queue.

+----------------------+------+
| field                | valu |
|                      | e    |
+======================+======+
| is_embedded          | True |
+----------------------+------+
| supports_interactive | True |
+----------------------+------+
| supports_batch       | True |
+----------------------+------+
| uses_file_system     | True |
+----------------------+------+

location string:
    * `[/workdir]`

supported properties:

+-------------------------------+-----------------------------+---------+--------+
| name                          | description                 | data_ty | defaul |
|                               |                             | pe      | t      |
+===============================+=============================+=========+========+
| queue.pollingDelay            | The polling delay for       | long    | `1000` |
|                               | monitoring running jobs (in |         |        |
|                               | milliseconds).              |         |        |
+-------------------------------+-----------------------------+---------+--------+
| queue.multi.maxConcurrentJobs | The maximum number of       | integer | `4`    |
|                               | concurrent jobs in the      |         |        |
|                               | multiq.                     |         |        |
+-------------------------------+-----------------------------+---------+--------+

Ssh
~~~
The SSH job adaptor implements all functionality to start jobs on ssh
servers.

+----------------------+------+
| field                | valu |
|                      | e    |
+======================+======+
| is_embedded          | True |
+----------------------+------+
| supports_interactive | True |
+----------------------+------+
| supports_batch       | True |
+----------------------+------+
| uses_file_system     | True |
+----------------------+------+

location string:
    * `host[:port][/workdir][ via:otherhost[:port]]*`

supported properties:

+-------------------------------+-----------------------------+---------+---------+
| name                          | description                 | data_ty | default |
|                               |                             | pe      |         |
+===============================+=============================+=========+=========+
| autoAddHostKey                | Automatically add unknown   | boolean | `true`  |
|                               | host keys to known_hosts.   |         |         |
+-------------------------------+-----------------------------+---------+---------+
| strictHostKeyChecking         | Enable strict host key      | boolean | `true`  |
|                               | checking.                   |         |         |
+-------------------------------+-----------------------------+---------+---------+
| loadKnownHosts                | Load the standard           | boolean | `true`  |
|                               | known_hosts file.           |         |         |
+-------------------------------+-----------------------------+---------+---------+
| loadSshConfig                 | Load the OpenSSH config     | boolean | `true`  |
|                               | file.                       |         |         |
+-------------------------------+-----------------------------+---------+---------+
| sshConfigFile                 | OpenSSH config filename.    | string  | (empty) |
+-------------------------------+-----------------------------+---------+---------+
| agent                         | Use a (local) ssh-agent.    | boolean | `false` |
+-------------------------------+-----------------------------+---------+---------+
| agentForwarding               | Use ssh-agent forwarding    | boolean | `false` |
+-------------------------------+-----------------------------+---------+---------+
| timeout                       | The timeout for the         | long    | `10000` |
|                               | connection setup and        |         |         |
|                               | authetication (in           |         |         |
|                               | milliseconds).              |         |         |
+-------------------------------+-----------------------------+---------+---------+
| queue.pollingDelay            | The polling delay for       | long    | `1000`  |
|                               | monitoring running jobs (in |         |         |
|                               | milliseconds).              |         |         |
+-------------------------------+-----------------------------+---------+---------+
| queue.multi.maxConcurrentJobs | The maximum number of       | integer | `4`     |
|                               | concurrent jobs in the      |         |         |
|                               | multiq..                    |         |         |
+-------------------------------+-----------------------------+---------+---------+
| gateway                       | The gateway machine used to | string  | (empty) |
|                               | create an SSH tunnel to the |         |         |
|                               | target.                     |         |         |
+-------------------------------+-----------------------------+---------+---------+

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

+-------------------------------+-----------------------------+---------+---------+
| name                          | description                 | data_ty | default |
|                               |                             | pe      |         |
+===============================+=============================+=========+=========+
| ignore.version                | Skip version check is       | boolean | `false` |
|                               | skipped when connecting to  |         |         |
|                               | remote machines. WARNING:   |         |         |
|                               | it is not recommended to    |         |         |
|                               | use this setting in         |         |         |
|                               | production environments!    |         |         |
+-------------------------------+-----------------------------+---------+---------+
| accounting.grace.time         | Number of milliseconds a    | long    | `60000` |
|                               | job is allowed to take      |         |         |
|                               | going from the queue to the |         |         |
|                               | qacct output.               |         |         |
+-------------------------------+-----------------------------+---------+---------+
| poll.delay                    | Number of milliseconds      | long    | `1000`  |
|                               | between polling the status  |         |         |
|                               | of a job.                   |         |         |
+-------------------------------+-----------------------------+---------+---------+
| autoAddHostKey                | Automatically add unknown   | boolean | `true`  |
|                               | host keys to known_hosts.   |         |         |
+-------------------------------+-----------------------------+---------+---------+
| strictHostKeyChecking         | Enable strict host key      | boolean | `true`  |
|                               | checking.                   |         |         |
+-------------------------------+-----------------------------+---------+---------+
| loadKnownHosts                | Load the standard           | boolean | `true`  |
|                               | known_hosts file.           |         |         |
+-------------------------------+-----------------------------+---------+---------+
| loadSshConfig                 | Load the OpenSSH config     | boolean | `true`  |
|                               | file.                       |         |         |
+-------------------------------+-----------------------------+---------+---------+
| sshConfigFile                 | OpenSSH config filename.    | string  | (empty) |
+-------------------------------+-----------------------------+---------+---------+
| agent                         | Use a (local) ssh-agent.    | boolean | `false` |
+-------------------------------+-----------------------------+---------+---------+
| agentForwarding               | Use ssh-agent forwarding    | boolean | `false` |
+-------------------------------+-----------------------------+---------+---------+
| timeout                       | The timeout for the         | long    | `10000` |
|                               | connection setup and        |         |         |
|                               | authetication (in           |         |         |
|                               | milliseconds).              |         |         |
+-------------------------------+-----------------------------+---------+---------+
| queue.pollingDelay            | The polling delay for       | long    | `1000`  |
|                               | monitoring running jobs (in |         |         |
|                               | milliseconds).              |         |         |
+-------------------------------+-----------------------------+---------+---------+
| queue.multi.maxConcurrentJobs | The maximum number of       | integer | `4`     |
|                               | concurrent jobs in the      |         |         |
|                               | multiq..                    |         |         |
+-------------------------------+-----------------------------+---------+---------+
| gateway                       | The gateway machine used to | string  | (empty) |
|                               | create an SSH tunnel to the |         |         |
|                               | target.                     |         |         |
+-------------------------------+-----------------------------+---------+---------+
| queue.pollingDelay            | The polling delay for       | long    | `1000`  |
|                               | monitoring running jobs (in |         |         |
|                               | milliseconds).              |         |         |
+-------------------------------+-----------------------------+---------+---------+
| queue.multi.maxConcurrentJobs | The maximum number of       | integer | `4`     |
|                               | concurrent jobs in the      |         |         |
|                               | multiq.                     |         |         |
+-------------------------------+-----------------------------+---------+---------+

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

+-------------------------------+-----------------------------+---------+---------+
| name                          | description                 | data_ty | default |
|                               |                             | pe      |         |
+===============================+=============================+=========+=========+
| disable.accounting.usage      | Do not use accounting info  | boolean | `false` |
|                               | of slurm, even when         |         |         |
|                               | available. Mostly for       |         |         |
|                               | testing purposes            |         |         |
+-------------------------------+-----------------------------+---------+---------+
| poll.delay                    | Number of milliseconds      | long    | `1000`  |
|                               | between polling the status  |         |         |
|                               | of a job.                   |         |         |
+-------------------------------+-----------------------------+---------+---------+
| autoAddHostKey                | Automatically add unknown   | boolean | `true`  |
|                               | host keys to known_hosts.   |         |         |
+-------------------------------+-----------------------------+---------+---------+
| strictHostKeyChecking         | Enable strict host key      | boolean | `true`  |
|                               | checking.                   |         |         |
+-------------------------------+-----------------------------+---------+---------+
| loadKnownHosts                | Load the standard           | boolean | `true`  |
|                               | known_hosts file.           |         |         |
+-------------------------------+-----------------------------+---------+---------+
| loadSshConfig                 | Load the OpenSSH config     | boolean | `true`  |
|                               | file.                       |         |         |
+-------------------------------+-----------------------------+---------+---------+
| sshConfigFile                 | OpenSSH config filename.    | string  | (empty) |
+-------------------------------+-----------------------------+---------+---------+
| agent                         | Use a (local) ssh-agent.    | boolean | `false` |
+-------------------------------+-----------------------------+---------+---------+
| agentForwarding               | Use ssh-agent forwarding    | boolean | `false` |
+-------------------------------+-----------------------------+---------+---------+
| timeout                       | The timeout for the         | long    | `10000` |
|                               | connection setup and        |         |         |
|                               | authetication (in           |         |         |
|                               | milliseconds).              |         |         |
+-------------------------------+-----------------------------+---------+---------+
| queue.pollingDelay            | The polling delay for       | long    | `1000`  |
|                               | monitoring running jobs (in |         |         |
|                               | milliseconds).              |         |         |
+-------------------------------+-----------------------------+---------+---------+
| queue.multi.maxConcurrentJobs | The maximum number of       | integer | `4`     |
|                               | concurrent jobs in the      |         |         |
|                               | multiq..                    |         |         |
+-------------------------------+-----------------------------+---------+---------+
| gateway                       | The gateway machine used to | string  | (empty) |
|                               | create an SSH tunnel to the |         |         |
|                               | target.                     |         |         |
+-------------------------------+-----------------------------+---------+---------+
| queue.pollingDelay            | The polling delay for       | long    | `1000`  |
|                               | monitoring running jobs (in |         |         |
|                               | milliseconds).              |         |         |
+-------------------------------+-----------------------------+---------+---------+
| queue.multi.maxConcurrentJobs | The maximum number of       | integer | `4`     |
|                               | concurrent jobs in the      |         |         |
|                               | multiq.                     |         |         |
+-------------------------------+-----------------------------+---------+---------+

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

+-------------------------------+-----------------------------+---------+---------+
| name                          | description                 | data_ty | default |
|                               |                             | pe      |         |
+===============================+=============================+=========+=========+
| ignore.version                | Skip version check is       | boolean | `false` |
|                               | skipped when connecting to  |         |         |
|                               | remote machines. WARNING:   |         |         |
|                               | it is not recommended to    |         |         |
|                               | use this setting in         |         |         |
|                               | production environments!    |         |         |
+-------------------------------+-----------------------------+---------+---------+
| accounting.grace.time         | Number of milliseconds a    | long    | `60000` |
|                               | job is allowed to take      |         |         |
|                               | going from the queue to the |         |         |
|                               | accinfo output.             |         |         |
+-------------------------------+-----------------------------+---------+---------+
| poll.delay                    | Number of milliseconds      | long    | `1000`  |
|                               | between polling the status  |         |         |
|                               | of a job.                   |         |         |
+-------------------------------+-----------------------------+---------+---------+
| autoAddHostKey                | Automatically add unknown   | boolean | `true`  |
|                               | host keys to known_hosts.   |         |         |
+-------------------------------+-----------------------------+---------+---------+
| strictHostKeyChecking         | Enable strict host key      | boolean | `true`  |
|                               | checking.                   |         |         |
+-------------------------------+-----------------------------+---------+---------+
| loadKnownHosts                | Load the standard           | boolean | `true`  |
|                               | known_hosts file.           |         |         |
+-------------------------------+-----------------------------+---------+---------+
| loadSshConfig                 | Load the OpenSSH config     | boolean | `true`  |
|                               | file.                       |         |         |
+-------------------------------+-----------------------------+---------+---------+
| sshConfigFile                 | OpenSSH config filename.    | string  | (empty) |
+-------------------------------+-----------------------------+---------+---------+
| agent                         | Use a (local) ssh-agent.    | boolean | `false` |
+-------------------------------+-----------------------------+---------+---------+
| agentForwarding               | Use ssh-agent forwarding    | boolean | `false` |
+-------------------------------+-----------------------------+---------+---------+
| timeout                       | The timeout for the         | long    | `10000` |
|                               | connection setup and        |         |         |
|                               | authetication (in           |         |         |
|                               | milliseconds).              |         |         |
+-------------------------------+-----------------------------+---------+---------+
| queue.pollingDelay            | The polling delay for       | long    | `1000`  |
|                               | monitoring running jobs (in |         |         |
|                               | milliseconds).              |         |         |
+-------------------------------+-----------------------------+---------+---------+
| queue.multi.maxConcurrentJobs | The maximum number of       | integer | `4`     |
|                               | concurrent jobs in the      |         |         |
|                               | multiq..                    |         |         |
+-------------------------------+-----------------------------+---------+---------+
| gateway                       | The gateway machine used to | string  | (empty) |
|                               | create an SSH tunnel to the |         |         |
|                               | target.                     |         |         |
+-------------------------------+-----------------------------+---------+---------+
| queue.pollingDelay            | The polling delay for       | long    | `1000`  |
|                               | monitoring running jobs (in |         |         |
|                               | milliseconds).              |         |         |
+-------------------------------+-----------------------------+---------+---------+
| queue.multi.maxConcurrentJobs | The maximum number of       | integer | `4`     |
|                               | concurrent jobs in the      |         |         |
|                               | multiq.                     |         |         |
+-------------------------------+-----------------------------+---------+---------+

