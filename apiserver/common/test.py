from error import Error
import err_code as  ErrCode
import err_msg as ErrMsg
from logger import log_info,log_debug,log_error

if __name__ == "__main__":
    err = Error(ErrCode.ERR_CODE_INTERNAL_ERROR, ErrMsg.ERR_MSG_INTERNAL_ERROR)
    log_info(type(err))
    log_debug(type(err.to_dict()))
    log_error(err)
