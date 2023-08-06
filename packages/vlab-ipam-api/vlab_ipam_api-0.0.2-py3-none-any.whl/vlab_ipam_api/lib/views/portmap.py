# -*- coding: UTF-8 -*-
"""
Defines the RESTful API for managing Port Map rules in the NAT firewall
"""
import random

import ujson
from flask import current_app
from flask_classy import request, Response
from vlab_api_common import BaseView, describe, get_logger, requires, validate_input

from vlab_ipam_api.lib import const, Database, DatabaseError


logger = get_logger(__name__, loglevel=const.VLAB_IPAM_LOG_LEVEL)


class PortMapView(BaseView):
    """API end point for managing Port Map rules"""
    route_base = '/api/1/ipam/portmap'
    POST_SCHEMA = { "$schema": "http://json-schema.org/draft-04/schema#",
                    "type": "object",
                    "description": "Create port mapping to connect through a NAT firewall",
                    "properties": {
                        "target_addr": {
                            "description": "The IP of the machine in your lab to connect to",
                            "type": "string"
                        },
                        "target_port": {
                            "description": "The port number of the machine in your lab to connect to",
                            "type": "integer"
                        },
                        "target_name": {
                            "description": "The name of your component",
                            "type": "string"
                        },
                        "target_component": {
                            "description": "The kind of component (i.e. OneFS, InsightIQ, etc)",
                            "type": "string"
                        }
                    },
                    "required": ["target_ip", "target_port", "target_name", "component"]
                  }
    DELETE_SCHEMA = {"$schema": "http://json-schema.org/draft-04/schema#",
                     "description": "Destroy a port mapping",
                     "type": "object",
                     "properties": {
                        "conn_port": {
                            "description": "The local port that forwards into the user's lab",
                            "type": "string"
                        }
                     },
                     "required": ["conn_port"]
                    }
    GET_SCHEMA = {"$schema": "http://json-schema.org/draft-04/schema#",
                  "description": "Display details about the port map rules configured"
                 }

    @requires(version=2, username=const.VLAB_IPAM_OWNER)
    @describe(post=POST_SCHEMA, delete=DELETE_SCHEMA, get=GET_SCHEMA)
    def get(self, *args, **kwargs):
        """Display the Port Map rules defined on the NAT firewall"""
        username = kwargs['token']['username']
        resp_data = {'user' : username, 'content' : {}}
        resp_data['content']['port_map'] = current_app.firewall.show(table='nat', format='json')
        resp = Response(ujson.dumps(resp_data))
        resp.status_code = 200
        return resp

    @requires(version=2, username=const.VLAB_IPAM_OWNER)
    @validate_input(schema=POST_SCHEMA)
    def post(self, *args, **kwargs):
        """Create a Port Map rule in the NAT firewall"""
        username = kwargs['token']['username']
        resp_data = {'user' : username, 'content' : {}}
        target_addr = kwargs['body']['target_addr']
        target_port = kwargs['body']['target_port']
        target_name = kwargs['body']['target_name']
        target_component = kwargs['body']['target_component']
        status_code = 200
        try:
            with Database() as db:
                conn_port = db.add_port(target_addr, target_port, target_name, target_component)
                try:
                    current_app.firewall.map_port(conn_port, target_port, target_addr)
                except (CliError, OSError, RuntimeError) as doh:
                    # OSError b/c map_port auto-saves the rule
                    db.delete_port(conn_port)
                    resp_data['error'] = '%s' % doh
                    logger.exception(doh)
        except Exception as doh:
            status_code = 500
            resp_data['error'] = '%s' % doh
        else:
            resp_data['content']['conn_port'] = conn_port

        resp = Response(ujson.dumps(resp_data))
        resp.status_code = status_code
        return resp

    @requires(version=2, username=const.VLAB_IPAM_OWNER)
    @validate_input(schema=DELETE_SCHEMA)
    def delete(self, *args, **kwargs):
        """Destroy a Port Map rule in the NAT firewall"""
        username = kwargs['token']['username']
        resp_data = {'user' : username, 'content' : {}}
        conn_port = kwargs['body']['conn_port']
        status_code = 200
        with Database() as db:
            target_port, target_addr = db.port_info(conn_port)
            # The ``with`` statement locks the firewall object
            # Only locking here because deleting requires multiple updates
            with current_app.firewall:
                nat_id = current_app.firewall.find_rule(target_port, target_addr, table='nat', conn_port=conn_port)
                filter_id = current_app.firewall.find_rule(target_port, target_addr, table='nat')
                record_error, status_code = records_valid(nat_id, filter_id, target_port, target_addr):
                if not record_error:
                    error, status_code = remove_map_rule(nat_id, filter_id, target_port, target_addr, db)
        resp_data['error'] = error
        resp = Response(ujson.dumps(resp_data))
        resp.status_code = status_code
        return resp


def records_valid(nat_id, filter_id, target_port, target_addr):
    """TODO"""
    if not (nat_id and filter_id) and (target_port and target_addr):
        # crap! iptables and DB are out of sync
        return False

def remove_map_rule(nat_id, filter_id, target_port, target_addr, db):
    """TODO"""
    current_app.firewall.delete_rule(nat_id, table='nat')
    try:
        # If we fail to delete the 2nd rule, undo the 1st delete
        current_app.firewall.delete_rule(filter_id, table='filter')
    except Exception as doh:
        status_code = 500
        logger.exception(doh)
        current_app.firewall.forward(target_port, target_addr)
        current_app.firewall.save_rules()
    else:
        # iptables updated; let's update the DB
        try:
            db.delete_port(conn_port)
        except Exception as doh:
            # If (for whatever reason) the DB update fails, we must
            # restore the state of iptables
            current_app.firewall.map_port(conn_port, target_port, target_addr)
            status_code = 500
            logger.exception(doh)
