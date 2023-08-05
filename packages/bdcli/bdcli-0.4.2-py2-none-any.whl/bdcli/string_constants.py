# Brown Dog Support Email ID
bd_support_email = "browndog-support@ncsa.illinois.edu"

# Operations
OP_GET_KEY = "GET_KEY"
OP_GET_TOKEN = "GET_TOKEN"
OP_GET_OUTPUTS = "GET_OUTPUTS"
OP_GET_EXTRACTORS = "GET_EXTRACTORS"
OP_FIND_SIMILAR = "FIND_SIMILAR"
OP_FILE_DOWNLOAD = "FILE_DOWNLOAD"
OP_FILE_CONVERSION = "FILE_CONVERSION"
OP_FILE_CONVERSION_LOCAL = "FILE_CONVERSION_LOCAL"
OP_FILE_EXTRACTION = "FILE_EXTRACTION"
OP_FILE_EXTRACTION_LOCAL = "FILE_EXTRACTION_LOCAL"
OP_FILE_INDEXING = "FILE_INDEXING"

# Error messages
# Get Key
MSG_GET_KEY_SUCCESS = "Successfully obtained new API Key."
MSG_GET_KEY_INVALID_CREDENTIALS = "Invalid credentials. Please check your username and password and try again."

# Get Token
MSG_GET_TOKEN_SUCCESS = "Successfully obtained new Access Token."
MSG_GET_TOKEN_INVALID_CREDENTIALS = "Invalid credentials. Please check your API Key and try again."
MSG_GET_TOKEN_KEY_NOT_FOUND = "API Key not found on server."

# Get supported output formats
MSG_GET_OUTPUTS_NO_CONTENT = "There are no supported output file formats within Brown Dog for the given input format." \
                             " Please check the provided input format name."

# Get available extractors
MSG_GET_EXTRACTORS_NO_CONTENT = "There are no supported extractors within Brown Dog that can process files in the " \
                                "given input format. If the input format is incorrect, please correct and try again. " \
                                "You can also send an email to " + bd_support_email + " to report this."

# File download
MSG_FILE_DOWNLOAD_NOT_FOUND = "No file was found at the given input URL. Please check the URL and try again."

# General
MSG_GEN_204_NO_CONTENT = "The Brown Dog API Gateway (Fence) successfully fulfilled your request but there is no " \
                         "additional content in the response."  # 204
MSG_GEN_400_BAD_REQUEST = "User authentication failed. Please make sure that you are providing your correct user " \
                       "and password and try again."  # 400
MSG_GEN_401_UNAUTHORIZED = "User authentication failed. Please make sure that you are providing your correct user " \
                       "and password and try again."  # 401
MSG_GEN_403_FORBIDDEN = "User not authorized. You do not seem to have enough permissions to perform this operation. " \
                        "If you think this is a mistake, please send an email to " + bd_support_email + "."  # 403
MSG_GEN_404_NOT_FOUND = "The requested resource was not found on Brown Dog servers. If you have any questions, " \
                        "please feel send an email to " + bd_support_email + "."  # 404
MSG_GEN_500_INTERNAL_SERVER_ERROR = "An internal server error has occurred. Please try again after some time."  # 500
MSG_GEN_502_BAD_GATEWAY = "The Brown Dog API Gateway (Fence) did not receive a valid response from one of the " \
                          "internal services of Brown Dog. Please try again after some time."  # 502
MSG_GEN_503_SERVICE_UNAVAILABLE = "Brown Dog is currently unavailable. This happens when the system is overloaded or " \
                                  "is under maintenance. Please try again after some time."  # 503
MSG_GEN_504_GATEWAY_TIMEOUT = "The Brown Dog API Gateway (Fence) did not receive a valid response from one of the " \
                          "internal services of Brown Dog. Please try again after some time."  # 504
MSG_GEN_UNKNOWN_ERROR_OCCURRED = "An unknown error occurred while processing your request. " \
                             "Please try again after some time."

