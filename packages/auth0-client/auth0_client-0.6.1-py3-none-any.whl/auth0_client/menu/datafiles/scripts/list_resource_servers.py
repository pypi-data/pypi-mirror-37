#!/usr/bin/env python

import json
from auth0_client.Auth0Client import Auth0Client
from auth0_client.menu.menu_helper.common import *
from auth0_client.menu.menu_helper.pretty import *


try:

    client = Auth0Client(auth_config())
    results = client.get_all_resource_servers()

    if type(results) == type(str()):
        results = json.loads(results)

    print(pretty(results))


except (KeyboardInterrupt, SystemExit):
    sys.exit()
