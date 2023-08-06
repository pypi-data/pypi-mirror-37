# -*- coding: UTF-8 -*-
"""
Defines the RESTful API for managing Port Map rules in the NAT firewall
"""
import ujson
from flask import current_app
from flask_classy import request, route, Response
from vlab_api_common import BaseView, describe, get_logger, requires, validate_input

from vlab_ipam_api.lib import const


logger = get_logger(__name__, loglevel=const.VLAB_IPAM_LOG_LEVEL)


class IpamView(TaskView):
    """API end point for managing Port Map rules"""
    route_base = '/api/1/ipam/portmap'
    POST_SCHEMA = { "$schema": "http://json-schema.org/draft-04/schema#",
                    "type": "object",
                    "description": "Create port mapping to connect through a NAT firewall",
                    "properties": {
                        "target ip": {
                            "description": "The IP of the machine in your lab to connect to",
                            "type": "string"
                        },
                        "target port": {
                            "description": "The port number of the machine in your lab to connect to",
                            "type": "integer"
                        },
                        "target name": {
                            "description": "The name of your component",
                            "type": "string"
                        },
                        "component type": {
                            "description": "The kind of component (i.e. OneFS, InsightIQ, etc)",
                            "type": "string"
                        }
                    },
                    "required": ["target ip", "target port", "target name", "component type"]
                  }
    DELETE_SCHEMA = {"$schema": "http://json-schema.org/draft-04/schema#",
                     "description": "Destroy a port mapping",
                     "type": "object",
                     "properties": {
                        "name": {
                            "description": "The name of the Ipam instance to destroy",
                            "type": "string"
                        }
                     },
                     "required": ["name"]
                    }
    GET_SCHEMA = {"$schema": "http://json-schema.org/draft-04/schema#",
                  "description": "Display details about the port map rules configured"
                 }

    @requires(version=2, username=const.VLAB_IPAM_OWNER)
    @describe(post=POST_SCHEMA, delete=DELETE_SCHEMA, get=GET_SCHEMA)
    def get(self, *args, **kwargs):
        """Display the Port Map rules defined on the NAT firewall"""
        username = kwargs['token']['username']
        resp_data = {'user' : username}
        resp = Response(ujson.dumps(resp_data))
        resp.status_code = 200
        return resp

    @requires(version=2, username=const.VLAB_IPAM_OWNER)
    @validate_input(schema=POST_SCHEMA)
    def post(self, *args, **kwargs):
        """Create a Port Map rule in the NAT firewall"""
        username = kwargs['token']['username']
        resp_data = {'user' : username}
        resp = Response(ujson.dumps(resp_data))
        resp.status_code = 200
        return resp

    @requires(version=2, username=const.VLAB_IPAM_OWNER)
    @validate_input(schema=DELETE_SCHEMA)
    def delete(self, *args, **kwargs):
        """Destroy a Port Map rule in the NAT firewall"""
        username = kwargs['token']['username']
        resp_data = {'user' : username}
        resp = Response(ujson.dumps(resp_data))
        resp.status_code = 200
        return resp
