# -*- coding: utf-8 -*-

"""
Copyright (C) 2018, Zato Source s.r.o. https://zato.io

Licensed under LGPLv3, see LICENSE.txt for terms and conditions.
"""

# Originally part of Zato - open-source ESB, SOA, REST, APIs and cloud integrations in Python
# https://zato.io

from __future__ import absolute_import, division, print_function, unicode_literals

from gevent import monkey
monkey.patch_all()

# stdlib
import os

# Behave
from behave.configuration import Configuration
from behave.runner import Runner

# ConfigObj
from configobj import ConfigObj

def handle(path, args=None):
    file_conf = ConfigObj(os.path.join(path, 'features', 'config.ini'))
    try:
        behave_options = file_conf['behave']['options']
    except KeyError:
        raise ValueError("Behave config not found."
            " Are you running with the right path?")
    if args:
        behave_options += ' ' + ' '.join(args)

    tags = os.environ.get('ZATO_APITEST_TAGS')
    if tags:
        behave_options += ' --tags '
        behave_options += ','.join(tags.split())

    conf = Configuration(behave_options)
    conf.paths = [os.path.join(path, 'features')]
    runner = Runner(conf)
    return runner.run()
