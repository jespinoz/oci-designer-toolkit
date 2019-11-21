#!/usr/bin/python
# Copyright (c) 2013, 2014-2019 Oracle and/or its affiliates. All rights reserved.


"""Provide Module Description
"""

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
__author__ = ["Andrew Hopkinson (Oracle Cloud Solutions A-Team)"]
__copyright__ = "Copyright (c) 2013, 2014-2019  Oracle and/or its affiliates. All rights reserved."
__ekitversion__ = "@VERSION@"
__ekitrelease__ = "@RELEASE@"
__version__ = "1.0.0.0"
__date__ = "@BUILDDATE@"
__status__ = "@RELEASE@"
__module__ = "ociRouteTable"
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


import oci

from common.ociLogging import getLogger
from facades.ociConnection import OCIVirtualNetworkConnection

# Configure logging
logger = getLogger()


class OCIRouteTables(OCIVirtualNetworkConnection):
    def __init__(self, config=None, configfile=None, compartment_id=None, vcn_id=None):
        self.compartment_id = compartment_id
        self.vcn_id = vcn_id
        self.route_tables_json = []
        self.route_tables_obj = []
        super(OCIRouteTables, self).__init__(config=config, configfile=configfile)

    def list(self, compartment_id=None, filter=None):
        if compartment_id is None:
            compartment_id = self.compartment_id

        if self.vcn_id is not None:
            route_tables = oci.pagination.list_call_get_all_results(self.client.list_route_tables, compartment_id=compartment_id, vcn_id=self.vcn_id).data
            # Convert to Json object
            route_tables_json = self.toJson(route_tables)
            logger.debug(str(route_tables_json))

            # Filter results
            self.route_tables_json = self.filterJsonObjectList(route_tables_json, filter)
            logger.debug(str(self.route_tables_json))

            # Build List of RouteTable Objects
            self.route_tables_obj = []
            for route_table in self.route_tables_json:
                self.route_tables_obj.append(OCIRouteTable(self.config, self.configfile, route_table))
        else:
            logger.warn('Virtual Cloud Network Id has not been specified.')

        return self.route_tables_json


class OCIRouteTable(object):
    def __init__(self, config=None, configfile=None, data=None):
        self.config = config
        self.configfile = configfile
        self.data = data

