# Brown Dog Support Email ID
bd_support_email = "browndog-support@ncsa.illinois.edu"

# Get Key
MSG_GET_KEY_SUCCESS = "Successfully obtained new API Key."
MSG_GET_KEY_INVALID_CREDENTIALS = "Invalid credentials. Please check your username and password and try again."

# Get Token
MSG_GET_TOKEN_SUCCESS = "Successfully obtained new Access Token."
MSG_GET_TOKEN_INVALID_CREDENTIALS = "Invalid credentials. Please check your username and password and try again."


# General
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
MSG_GEN_FORBIDDEN = ""  # 404
