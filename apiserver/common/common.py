import time
import netaddr
from django.conf import settings
from django.http import HttpRequest, HttpResponse
from json import json_dump, json_load
from logger import log_error, log_debug, log_info
from error import Error
import err_code as ErrCode
import err_msg as ErrMSG
from api_request import APIRequest

def ip_in_network(ip, network):
    try:
        if isinstance(network, (list, tuple)) and len(network) == 2:
            is_in = netaddr.IPAddress(ip) in netaddr.IPRange(network[0], network[1])
        else:
            is_in = netaddr.IPAddress(ip) in netaddr.IPNetwork(network)
        if not is_in:
            return False
        return True
    except Exception, e:
        log_error("invalid ip [%s]: %s", ip, e)
        return False

def get_remote_addr(req):
    if 'HTTP_X_REAL_IP' in req.META:
        return req.META['HTTP_X_REAL_IP']
    return req.META['REMOTE_ADDR']

def get_request_headers(req):
    is_secure = is_secure_path(req)
    
    headers = {"method": req.method,
               "path": req.path,
               "remote_addr": get_remote_addr(req),
               "remote_port": req.META["REMOTE_PORT"],
               "server_addr": req.META["SERVER_ADDR"],
               "server_port": req.META["SERVER_PORT"],
               "is_secure": is_secure}
    return headers

def _send(msg):
    return

def send_request(api_request):
    if not isinstance(api_request, APIRequest):
        log_error("illegal api_request [%s]" % api_request)
        return None
        
    start_time = time.time()
    
    try:
        #only send to localhost, but maybe use cluster with zk
        host = '127.0.0.1'
        port = '9512'
        # send request
        req = api_request.build_request()
        log_debug("sending request to vdi_server [%s:%s], [%s]" % (host, port, req))
        ret = _send(json_dump(req))
        rep = json_load(ret)
        if rep == None or rep['ret_code'] == -1:
            log_error("receive reply failed on [%s]" % host)
            return None
    except Exception, e:
        log_error("send request failed, unexpected error [%s]" % e)
        return None
    
    # logging request
    end_time = time.time()
    log_info("handler request [%s], ret_code [%s], exec_time is [%.3f]s" % (api_request, rep['ret_code'], (end_time - start_time)))
    return json_dump(rep)

def return_error(req, error, **kwargs):
    response = {}
    error = error if isinstance(error, Error) else Error(ErrCode.ERR_CODE_INTERNAL_ERROR, ErrMSG.ERR_MSG_INTERNAL_ERROR)
    response["ret_code"] = error.err_code()
    response["message"] = error.err_msg()
    for k in kwargs:
        response[k] = kwargs[k]

    return json_dump(response)

def is_secure_path(request):
    secure_ports = settings.PITRIX_SETTINGS['secure_ports']
    if len(secure_ports) == 0 or (request.META["SERVER_PORT"] in secure_ports):
        return True
    return False
