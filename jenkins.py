#!/usr/bin/python

import json
import sys
import urllib3
import jenkinsapi
from jenkinsapi.jenkins import Jenkins

jenkinsUrl = "https://build.georchestra.org/ci/"
J = Jenkins(jenkinsUrl)


def updateLastFailedBuilds():
    pass


print (J.keys())

for k,v in J.iteritems():
    print v.get_build_dict()



sys.exit(0)
