#!/usr/bin/python
# Copyright (c) 2013, 2014-2019 Oracle and/or its affiliates. All rights reserved.


"""Provide Module Description
"""

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
__author__ = ["Stefan Hinker (Oracle Cloud Solutions A-Team)"]
__copyright__ = "Copyright (c) 2013, 2014-2019  Oracle and/or its affiliates. All rights reserved."
__ekitversion__ = "@VERSION@"
__ekitrelease__ = "@RELEASE@"
__version__ = "1.0.0.0"
__date__ = "@BUILDDATE@"
__status__ = "@RELEASE@"
__module__ = "ociNetwork"
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


import oci
import re
import sys

from facades.ociConnection import OCIComputeConnection
from common.ociLogging import getLogger

# Configure logging
logger = getLogger()

class OCIInstanceVnicAttachments(OCIComputeConnection):
    def __init__(self, config=None, configfile=None, compartment_id=None, instance_id=None, **kwargs):
        self.compartment_id = compartment_id
        self.instance_id = instance_id
        self.vnic_attachments_json = []
        self.vnic_attachments_obj = []
        super(OCIInstanceVnicAttachments, self).__init__(config=config, configfile=configfile)

    def list(self, compartment_id=None, instance_id=None):
        if compartment_id is None:
            compartment_id = self.compartment_id
        if instance_id is None:
            instance_id = self.instance_id

        vnic_attachments = oci.pagination.list_call_get_all_results(self.client.list_vnic_attachments, compartment_id=compartment_id, instance_id=instance_id).data
        # Convert to Json object
        vnic_attachments_json = self.toJson(vnic_attachments)
        logger.debug(str(vnic_attachments_json))
  
        self.vnic_attachments_json=vnic_attachments_json
        logger.debug(str(self.vnic_attachments_json))

        for vnic_attachment in self.vnic_attachments_json:
            self.vnic_attachments_obj.append(OCIInstanceVnicAttachment(self.config, self.configfile, vnic_attachment))

        return self.vnic_attachments_json

class OCIInstanceVnicAttachment(object):
    def __init__(self, config=None, configfile=None, data=None, **kwargs):
        self.config = config
        self.configfile = configfile
        self.data = data

class OCIInstances(OCIComputeConnection):
    def __init__(self, config=None, configfile=None, compartment_id=None, **kwargs):
        self.compartment_id = compartment_id
        self.instances_json = []
        self.instances_obj = []
        super(OCIInstances, self).__init__(config=config, configfile=configfile)

    def list(self, compartment_id=None, filter=None):
        if compartment_id is None:
            compartment_id = self.compartment_id

        instances = oci.pagination.list_call_get_all_results(self.client.list_instances, compartment_id=compartment_id).data
        # Convert to Json object
        instances_json = self.toJson(instances)
        logger.debug(str(instances_json))

        # Check if the results should be filtered
        # Stefan: No filtering here so far...
        #if filter is None:
            #self.instances_json = instances_json
        #else:
            #filtered = instances_json[:]
            #for key, val in filter.items():
                #filtered = [instance for instance in filtered if re.compile(val).search(instance[key])]
            #self.instances_json = filtered
 
        self.instances_json=instances_json
        logger.debug(str(self.instances_json))

        for instance in self.instances_json:
            self.instances_obj.append(OCIInstance(self.config, self.configfile, instance))

        return self.instances_json


class OCIInstance(object):
    def __init__(self, config=None, configfile=None, data=None, id=None):
        self.config = config
        self.configfile = configfile
        self.data = data
        
    def getInstanceVnicAttachmentClients(self):
        return OCIInstanceVnicAttachments(self.config, self.configfile, self.data['compartment_id'], self.data['id'])
        

# Main processing function
def main(argv):

    return


# Main function to kick off processing
if __name__ == "__main__":
    main(sys.argv[1:])
