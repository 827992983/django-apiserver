# Create your views here.
import copy
from django.conf import settings
from django.http import HttpResponse
from common.api_request import APIRequest
from common.common import return_error, send_request, get_request_headers
from common.constants import API_REQUEST_TYPE
import common.err_code as ErrCode
import common.err_msg as ErrMsg
from common.error import Error
from common.logger import log_info, log_error

def api(request):
    ''' Handle http request '''
    log_info('request:%s' % request)
    if request.method not in ["GET", "POST"]:
        log_error("unsupported method [%s]" % (request.method))
        content = return_error(request, Error(ErrCode.ERR_CODE_INVALID_REQUEST, ErrMsg.ERR_MSG_INVALID_REQUEST))
    else:
        content = handle_request(request)
    response = HttpResponse(content, content_type = "application/json")
    return response

def handle_request(req):
    ''' handle incoming request '''
    # build api request
    if req.method == "GET":
        params = copy.deepcopy(req.GET)
    elif req.method == "POST":
        params = copy.deepcopy(req.POST)
    api_request = APIRequest(API_REQUEST_TYPE, 
                             get_request_headers(req), 
                             params)

    # POST method
    if req.method == "POST":
        return return_error(req, Error(ErrCode.ERR_CODE_INVALID_REQUEST, ErrMsg.ERR_MSG_INVALID_REQUEST))

    # send request
    rep = send_request(api_request) 
    if rep is None:
        if settings.SERVER_UPDATING:
            return return_error(req, Error(ErrCode.ERR_CODE_SERVER_UPDAT, ErrMsg.ERR_MSG_SERVER_UPDAT))
        else:
            return return_error(req, Error(ErrCode.ERR_CODE_INTERNAL_ERROR, ErrMsg.ERR_MSG_INTERNAL_ERROR))

    return rep
