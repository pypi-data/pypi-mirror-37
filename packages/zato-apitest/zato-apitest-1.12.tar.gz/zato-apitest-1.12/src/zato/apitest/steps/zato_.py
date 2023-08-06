# -*- coding: utf-8 -*-

"""
Copyright (C) 2018, Zato Source s.r.o. https://zato.io

Licensed under LGPLv3, see LICENSE.txt for terms and conditions.
"""

# Originally part of Zato - open-source ESB, SOA, REST, APIs and cloud integrations in Python
# https://zato.io

from __future__ import absolute_import, division, print_function, unicode_literals

# stdlib
from datetime import datetime
from httplib import OK
import json
from os.path import split

# requests
import requests

# Behave
from behave import given, then, when

# Zato
from .. import util
from .. import CHANNEL_TYPE
from zato.websocket.client import Client as WSXClient, Config as WSXConfig

# ################################################################################################################################

@given('I store "{cluster_id}" "{url_path}" "{username}" "{password}" under Zato "{conn_name}"')
@util.obtain_values
def given_i_store_zato_info_under_conn_name(ctx, cluster_id, url_path, username, password, conn_name):
    ctx.zato.user_ctx[conn_name] = {
        'cluster_id': cluster_id,
        'url_path': url_path,
        'username': username,
        'password': password
    }

# ################################################################################################################################

@when('I upload a Zato service from "{module_path}" to "{conn_name}"')
@util.obtain_values
def when_i_upload_a_zato_service_from_path_to_conn_details(ctx, module_path, conn_name):
    with open(module_path, 'r') as module:
        service_code = module.read().encode('base64', 'strict')
        payload = json.dumps({
            'cluster_id': conn_name['cluster_id'],'payload': service_code,
            'payload_name': split(module_path)[-1]
            }, ensure_ascii=False)

        response = requests.get(conn_name['url_path'], auth=(conn_name['username'], conn_name['password']), data=payload)
        assert response.status_code == OK

# #################################################################################################################################

@given('I use Zato WSX')
def given_i_use_zato_wsx(ctx):
    ctx.zato.zato_channel_type = CHANNEL_TYPE.WEB_SOCKETS

# #################################################################################################################################

@given('I connect to a Zato WSX channel without credentials')
def given_i_connect_to_zato_wsx_without_credentials(ctx):

    ctx.zato.zato_wsx_username = ''
    ctx.zato.zato_wsx_secret = ''

    def on_request_from_zato(msg):
        pass

    config = WSXConfig()
    config.client_name = 'zato-apitest'
    config.client_id = '{}.{}'.format(config.client_name, datetime.utcnow().isoformat())
    config.address = '{}{}'.format(ctx.zato.request.address, ctx.zato.request.url_path)
    config.username = ctx.zato.zato_wsx_username
    config.secret = ctx.zato.zato_wsx_secret
    config.on_request_callback = on_request_from_zato

    client = WSXClient(config)
    client.run()

    if not client.is_authenticated:
        raise Exception('Client `{}` could not authenticate with {} (Incorrect credentials? Server not running?)'.format(
            config.username, config.address))

    ctx.zato.wsx_client = client

# #################################################################################################################################

@given('I close WSX connection')
def given_i_close_wsx_connection(ctx):
    ctx.zato.wsx_client.stop()

# #################################################################################################################################

@then('WSX client is authenticated')
def then_wsx_client_is_authenticated(ctx):
    assert ctx.zato.wsx_client.is_authenticated is True

# #################################################################################################################################

@then('WSX client is disconnected')
def then_wsx_client_is_disconnected(ctx):
    assert ctx.zato.wsx_client.conn.client_terminated is True

# ################################################################################################################################

@given('Zato WebSockets service "{service}"')
@util.obtain_values
def given_zato_websockets_service(ctx, service):
    ctx.zato.zato_ws_service = service

# ################################################################################################################################
