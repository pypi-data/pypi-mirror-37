# pysshops

pysshops is a comodity pacakge to build python operations tools working on ssh and powered by [paramiko](https://github.com/paramiko/paramiko).

## Quickstart
```python
from pysshops import SshOps
sshops = SshOps('hostname.domain.it', 'username')
with sshops as ssh:
    ssh.remote_command('ls -l /var/tmp')
```

```python
from pysshops import SftpOps
sftpops = SftpOps('hostname.domain.it', 'username')
with sftpops as sftp:
    sftp.deploy('pysshops_sftp', '/tmp/pysshops_sftp')
```
## Install
### Git
```
git clone
cd pysshops
python setup.py install
```

### Pip
```
pip install pysshops
```

## Features
* simple
* powered by rock-solid paramiko
* python2/3 compatibility
* both ssh and sftp facilities
* external key based authentication at os level
