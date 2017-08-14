import simplejson
from logger import log_error

def json_dump(obj):
    try:
        jstr = simplejson.dumps(obj, separators=(',', ':'))
    except Exception, e:
        jstr = None
        log_error("dump json failed: %s" % e)
    return jstr

def json_load(json):
    if not json:
        return None
    try:
        obj = simplejson.loads(json, encoding='utf-8')
    except Exception, e:
        obj = None
        log_error("load json failed: %s" % e)
    return obj

__all__ = [json_dump, json_load]
