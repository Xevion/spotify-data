import os
import sys
import time
import json
import auth
import pull
import process
import logging

cache = json.load(open(os.path.join(sys.path[0], f'.cache-{auth.username}')))
if time.time() > cache['expires_at']:
    pull.main()