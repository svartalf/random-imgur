# -*- coding: utf-8 -*-

import os.path

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

REDIS_DATABASE = 1

# Check image status in seconds
CHECKER_INTERVAL = 3

TEMPLATE_PATH = os.path.join(PROJECT_ROOT, 'templates')