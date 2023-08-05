__author__ = 'Lorenzo Gaggini'
__email__ = 'lg@lgaggini.net'
__url__ = 'https://github.com/lgaggini/pysshops'
__version__ = '0.1.2'

from .pysshops import SshOps, SftpOps

from .pysshops import SshNetworkException, SftpNetworkException
from .pysshops import SshCommandBlockingException, SftpCommandException

__all__ = [
        'SshOps',
        'SshCommandBlockingException',
        'SshNetworkException',
     ]
