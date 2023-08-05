from string_constants import *
import httplib


def process_common_http_status_codes(status_code, operation=None, custom_message=None):

    # Important: This string has to be prepended to all informational messages printed by this program.
    # If not, piping and redirection will not work properly.
    bdcli_str = "bdcli: "

    # Forbidden
    # TODO: Check if Fence needs to send UNAUTHORIZED instead of FORBIDDEN
    if status_code == httplib.FORBIDDEN:
        if operation is OP_GET_KEY:
            print bdcli_str + MSG_GET_KEY_INVALID_CREDENTIALS
            exit(1)
        elif operation is OP_GET_TOKEN:
            print bdcli_str + MSG_GET_TOKEN_INVALID_CREDENTIALS
        else:
            print bdcli_str + MSG_GEN_403_FORBIDDEN
    # Not Found
    elif status_code == httplib.NOT_FOUND:
        if operation is OP_GET_TOKEN:
            print bdcli_str + MSG_GET_TOKEN_KEY_NOT_FOUND
        elif operation is OP_FILE_DOWNLOAD:
            print bdcli_str + MSG_FILE_DOWNLOAD_NOT_FOUND
            exit(1)
        else:
            print bdcli_str + MSG_GEN_404_NOT_FOUND
    # No Content
    elif status_code == httplib.NO_CONTENT:
        if operation is OP_GET_OUTPUTS:
            print bdcli_str + MSG_GET_OUTPUTS_NO_CONTENT
        elif operation is OP_GET_EXTRACTORS:
            print bdcli_str + MSG_GET_EXTRACTORS_NO_CONTENT
        else:
            print bdcli_str + MSG_GEN_204_NO_CONTENT
    # Bad Gateway
    elif status_code == httplib.BAD_GATEWAY:
        print bdcli_str + MSG_GEN_502_BAD_GATEWAY
    # An unknown or unhandled error occurred.
    else:
        print bdcli_str + MSG_GEN_UNKNOWN_ERROR_OCCURRED
