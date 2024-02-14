#!/usr/bin/env python

import os

# Connection and authentication details
SERVER_URL  =   'https://api.clarivate.com/'
API_KEY     =   os.environ.get("AI_API_KEY", None)
CONTENT_SET_NAMES = ["dealspa"]
