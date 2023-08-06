##
#
# File:    CreateRWTree.py
# Author:  E. Peisach
# Date:    22-Oct-2018
# Version: 0.001
##
"""
Copies selected mock-data to a r/w tree for test cases.

"""

__docformat__ = "restructuredtext en"
__author__ = "Ezra Peisach"
__email__ = "peisach@rcsb.rutgers.edu"
__license__ = "Creative Commons Attribution 3.0 Unported"
__version__ = "V0.01"

import logging
import shutil
import os

logger = logging.getLogger(__name__)


class CreateRWTree(object):
    def __init__(self, source=None, destination=None):
        self.__srcDir = source
        self.__dstDir = destination
        self.__reqOpts = {
            'site-config': '_copysiteconfig',
            'actiondata': '_copyactiondata',
            'archive': '_copyarchive',
        }

    def createtree(self, objlist=None):
        for obj in objlist:
            if type(obj) is str:
                req = obj
                opt_arg = None
            else:
                req = obj[0]
                if len(obj) > 1:
                    opt_arg = obj[1]
                else:
                    opt_arg = None

            if req in self.__reqOpts:
                mth = getattr(self, self.__reqOpts[req], None)
                if opt_arg:
                    mth(opt_arg)
                else:
                    mth()
            else:
                logger.error("%s not known" % req)

    def _copysiteconfig(self):
        """Copies the site config tree down so that MockTopDir will be the top of the r/w tree"""
        logging.info("Creating %s" % self.__dstDir)
        src = os.path.join(self.__srcDir, 'site-config')
        dst = os.path.join(self.__dstDir, 'site-config')
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(src, dst)

    def _copyactiondata(self):
        """Copies the actondata definitions"""
        src = os.path.join(self.__srcDir, 'da_top', 'resources_ro', 'actionData.xml')
        dst = os.path.join(self.__dstDir, 'da_top', 'resources_ro', 'actionData.xml')
        logging.info("Copying %s to %s" %(src, dst))
        dst_base = os.path.dirname(dst)
        if os.path.exists(dst):
            os.unlink(dst)
        if not os.path.exists(dst_base):
            os.makedirs(dst_base)
        shutil.copyfile(src, dst)

    def _copyarchive(self, idlist):
        """Copies the archive directory down so that MockTopDir will be the top of the r/w tree"""
        if type(idlist) is str:
            idlist = [idlist]

        for did in idlist:
            src = os.path.join(self.__srcDir, 'da_top', 'data', 'archive', did)
            dst = os.path.join(self.__dstDir, 'da_top', 'data', 'archive', did)
            logger.info("Copying %s to %s" % (src, dst))
            if os.path.exists(dst):
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
