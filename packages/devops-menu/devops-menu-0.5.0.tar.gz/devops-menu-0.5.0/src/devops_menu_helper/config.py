
import boto3.session
import re
from .pretty import *
import os
import sys
from os.path import expanduser
import ConfigParser
from .s3 import *


DEBUG=1

def create_devops_menu_config_file():


    home = expanduser("~")

    PATH = home+'/devops-menu/config.ini'

    if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
        if (DEBUG):
            print "devops-menu config file exists and is readable"

    else:
        print "Either file is missing or is not readable.  Let us create a file"

        open(PATH, 'w').close()




