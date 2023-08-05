#! /usr/bin/env python

import logging
from paramiko import SSHClient, WarningPolicy
from socket import error, herror, gaierror, timeout
import os


logger = logging.getLogger('pysshops')


class SshOps:
    hostname = ''
    port = 22
    username = ''
    password = ''
    key_filename = ''
    ssh = None

    def __init__(self, hostname, username=None, port=22, password=None,
                 key_filename=None):
        """ init a hostname and username for ssh connection """
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.key_filename = key_filename

    def __enter__(self):
        """ get a ssh connection to hostname """
        logger.info('opening ssh connection to %s as %s on port %s'
                    % (self.hostname, self.username, self.port))
        ssh = SSHClient()
        ssh.set_missing_host_key_policy(WarningPolicy())
        try:
            ssh.connect(self.hostname, username=self.username, port=self.port,
                        password=self.password, key_filename=self.key_filename)
        except (error, herror, gaierror, timeout) as neterr:
            msg = 'network problem: %s' % (neterr)
            logger.error(msg)
            raise SshNetworkException(msg)
        self.ssh = ssh
        return self

    def __check_exit(self, exitcode, stdout, stderr, block=True):
        """ check the exit code and if not 0 log stderror and exit
        (if blocking command) """
        if exitcode == 0:
            return exitcode, stdout
        else:
            msg = 'ssh command failed with exit code %s: %s' \
                   % (str(exitcode), stderr)
            logger.error(msg)
            if block:
                raise SshCommandBlockingException(msg)
            else:
                return exitcode, stderr

    def remote_command(self, command, block=True):
        """ execute a remote command by the ssh connection """
        logger.info('running %s on %s' % (command, self.hostname))
        stdin, stdout, stderr = self.ssh.exec_command(command)
        stdout_str = ' ,'.join(stdout.readlines())
        stderr_str = ' ,'.join(stderr.readlines())
        logger.debug('stdout: ' + stdout_str)
        logger.debug('stderr: ' + stderr_str)
        return self.__check_exit(stdout.channel.recv_exit_status(),
                                 stdout_str,
                                 stderr_str,
                                 block)

    def __exit__(self, exc_type, exc_value, traceback):
        """ close the ssh connection at the end """
        logger.info('closing ssh connection to %s' % self.hostname)
        self.ssh.close()


class SftpOps:
    hostname = ''
    port = 22
    username = ''
    password = ''
    key_filename = ''
    ssh = None
    sftp = None

    def __init__(self, hostname, username=None, port=22, password=None,
                 key_filename=None):
        """ init a hostname and username for sftp connection """
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.key_filename = key_filename

    def __enter__(self):
        """ get a sftp connection to hostname """
        logger.info('opening sftp connection to %s as %s on port %s'
                    % (self.hostname, self.username, self.port))
        ssh = SSHClient()
        sftp = None
        ssh.set_missing_host_key_policy(WarningPolicy())
        try:
            ssh.connect(hostname=self.hostname, username=self.username,
                        port=self.port, password=self.password,
                        key_filename=self.key_filename)
            sftp = ssh.open_sftp()
        except (error, herror, gaierror, timeout) as neterr:
            msg = 'network problem: %s' % (neterr)
            logger.error(msg)
            raise SftpNetworkException(msg)
        self.ssh = ssh
        self.sftp = sftp
        return self

    def deploy(self, src, dst, block=False):
        """ deploy a local file to remote host """
        if not os.path.exists(src):
            logger.warning('Missing %s file and will not be deployed' % src)
            return
        logger.info('deploying file %s to %s on %s' %
                    (src, dst, self.hostname))
        try:
            self.sftp.put(src, dst)
        except Exception as ex:
            msg = 'SFTP deploy exception: %s' % (ex)
            logger.error(msg)
            if block:
                raise SftpCommandException(msg)
        logger.info('verify the deployed file')
        command = 'sudo ls -l %s' % (dst)
        stdin, stdout, stderr = self.ssh.exec_command(command)
        exitcode = stdout.channel.recv_exit_status()
        if exitcode != 0:
            msg = 'deploy of %s to %s failed: %s, exitcode %s' \
                   % (src, dst, stderr, str(exitcode))
            logger.error(msg)
        logger.info('file %s correctly deployed to %s' % (src, dst))

    def chmod(self, dst, perm, block=False):
        """ chmod of a remote file """
        logger.info('chmodding file %s on %s to %s' % (dst,
                                                       self.hostname,
                                                       perm))
        try:
            self.sftp.chmod(dst, perm)
        except Exception as ex:
            msg = 'SFTP chmod exception: %s' % (ex)
            logger.error(msg)
            if block:
                raise SftpCommandException(msg)

    def __exit__(self, exc_type, exc_value, traceback):
        """ close the sftp connection at the end """
        logger.info('closing sftp connection to %s' % self.hostname)
        self.sftp.close()
        self.ssh.close()


class SshNetworkException(Exception):
    pass


class SshCommandBlockingException(Exception):
    pass


class SftpNetworkException(Exception):
    pass


class SftpCommandException(Exception):
    pass
