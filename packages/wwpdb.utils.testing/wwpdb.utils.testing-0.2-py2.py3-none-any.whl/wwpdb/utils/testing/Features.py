##
# File:    Features.py
# Date:    8-Oct-2018
#
# Updates:
#
##
"""
Allows testing harness to determine features of running environment
to allow skiping of tests.
"""
__docformat__ = "restructuredtext en"
__author__ = "Ezra Peisach"
__email__ = "peisach@rcsb.rutgers.edu"
__license__ = "Creative Commons Attribution 3.0 Unported"
__version__ = "V0.01"

class Features(object):
    def haveApi(self):
        """Returns True is api services available"""
        return True

    def haveMySqlTestServer(self):
        """Returns True if MySql server available for testing"""
        return False

    def haveRbmqTestServer(self):
        """Returns True if MySql server available for testing"""
        return False

    def haveCvsTestServer(self):
        """Returns True if CVS server available for testing"""
        return False

    def haveSvnTestServer(self):
        """Returns True if SVN server available for testing"""
        return False

    def haveSftpTestServer(self):
        """Returns True if SFTP server available for testing"""
        return False

    def testNever(self):
        """Always returns False to confirm ability to skip in testing"""
        return False
