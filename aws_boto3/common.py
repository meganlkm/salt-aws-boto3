import json
from collections import Mapping

import jmespath


def object_search(client, paginator, query, return_single=False):
    pager = client.get_paginator(paginator).paginate()
    for page in pager:
        result = jmespath.search(query, page)
        if result:
            if return_single:
                result = result.pop()
            return result
    return False


def dict_to_str(thing):
    rtnstr = thing
    if isinstance(thing, Mapping):
        try:
            rtnstr = json.dumps(thing)
        except Exception:
            rtnstr = str(thing)
    return rtnstr
