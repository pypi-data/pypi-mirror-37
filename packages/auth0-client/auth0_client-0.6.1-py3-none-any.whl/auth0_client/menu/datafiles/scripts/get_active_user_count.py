#!/usr/bin/env python

import json
from auth0_client.Auth0Client import Auth0Client
from auth0_client.menu.menu_helper.common import *
from auth0_client.menu.menu_helper.pretty import *


try:
    users = {}

    client = Auth0Client(auth_config())
    results = client.active_users()

    print(pretty(results))

except (KeyboardInterrupt, SystemExit):
    sys.exit()
