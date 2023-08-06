##
#
# File:    test_setup.py
# Author:  E. Peisach
# Date:    5-Oct-2018
# Version: 0.001
##
"""
Setups up configuration file and environment for use in test cases

Must be invoked before import ConfigInfo as cache must exist
"""

__docformat__ = "restructuredtext en"
__author__ = "Ezra Peisach"
__email__ = "peisach@rcsb.rutgers.edu"
__license__ = "Creative Commons Attribution 3.0 Unported"
__version__ = "V0.01"

import traceback
import os
import sys
import platform
from subprocess import call, check_output


# Empty class for import
class SiteConfigSetup(object):
    def __init__(self):
        pass

    def setupEnvironment(self, TestOutputPath, MockDirPath):
        if not os.path.exists(TestOutputPath):
            os.makedirs(TestOutputPath)

        testSiteConfig= os.path.join(TestOutputPath, 'site-config')
        fSiteConfig = os.path.join(testSiteConfig, 'rcsb-east', 'test')
        if not os.path.exists(fSiteConfig):
            os.makedirs(fSiteConfig)


        # Extend python search path
        sys.path.insert(0, fSiteConfig)
        os.environ['TOP_WWPDB_SITE_CONFIG_DIR'] = testSiteConfig
        os.environ['WWPDB_SITE_ID'] = 'TEST'
        os.environ['WWPDB_SITE_LOC'] = 'rcsb-east'

        call('ConfigInfoFileExec --writecache --locid=rcsb-east --siteid=TEST --sourcedir ' +
             os.path.join(MockDirPath, 'site-config') +
             ' --mockdir ' + MockDirPath, shell=True)

    
