import os
import random
import string
from bamboo_lib.connectors.models import Connector


def grab_connector(file_starting_point, cname):
    # try local file first then fall back to global
    par_dir = os.path.abspath(os.path.join(file_starting_point, os.pardir))
    local_conn_path = os.path.join(par_dir, "conns.yaml")
    # source = local_conn_path.get(cname, global_conn_path.get(cname))
    try:
        connector = Connector.fetch(cname, open(local_conn_path))
    except ValueError:
        BAMBOO_FALLBACK_CONNS = os.environ.get("BAMBOO_FALLBACK_CONNS")
        # TODO allow env var to customize default fallback config path
        global_conn_path = os.path.expanduser(os.path.expandvars(BAMBOO_FALLBACK_CONNS))
        connector = Connector.fetch(cname, open(global_conn_path))
    return connector


def random_char(y):
    return ''.join(random.choice(string.ascii_letters) for x in range(y))
