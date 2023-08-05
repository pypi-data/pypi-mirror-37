#!/usr/bin/env python
import getpass
from browndog.bd import *
from utils import *


# Generate key and token for an existing Brown Dog user
def get_key_token(bds, auth_file_path):

    bdcli_str = "bdcli: "

    # Check if a key already exists
    key_exists, api_key = check_key_token("key", bds, auth_file_path)

    # Check if a token already exists
    token_exists, access_token = check_key_token("token", bds, auth_file_path)

    if not key_exists or not token_exists:
        protocol, server = bds.split("://")

        if not key_exists:
            print bdcli_str + "API Key not available. Getting new API Key."
            bd_url = generate_url_with_credentials(protocol, server)
            # Obtain an access key from the Brown Dog API Gateway service
            api_key, status_code, status_text = get_key(bd_url)

            # Everything is OK
            if status_code == httplib.OK:
                print bdcli_str + MSG_GET_KEY_SUCCESS
                print bdcli_str + 'API Key: ' + str(api_key)
                key_exists = True
            else:
                process_common_http_status_codes(status_code, OP_GET_KEY)

        # Generate a new token if either currently a token doesn't exist or it has expired
        if not token_exists and key_exists:
            print bdcli_str + "Access Token expired or not available. Getting new token."
            # Obtain a token from the Brown Dog API Gateway service
            access_token, status_code, status_text = get_token(bds, api_key)

            # Everything is OK
            if status_code == httplib.OK:
                print bdcli_str + MSG_GET_TOKEN_SUCCESS
                print bdcli_str + 'Access Token: ' + str(access_token)
                token_exists = True
            else:
                process_common_http_status_codes(status_code, OP_GET_TOKEN)

            # If token is None, it could mean that the key was deleted from the database, hence get a new key and token.
            if access_token is None:

                # Reset flags
                key_exists = token_exists = False

                print bdcli_str + "Your API Key was possibly deleted from the server. Getting new API Key and Access " \
                                  "Token."
                bd_url = generate_url_with_credentials(protocol, server)

                api_key, status_code, status_text = get_key(bd_url)
                # Everything is OK
                if status_code == httplib.OK:
                    print bdcli_str + MSG_GET_KEY_SUCCESS
                    key_exists = True
                else:
                    process_common_http_status_codes(status_code, OP_GET_KEY)

                if key_exists:
                    access_token, status_code, status_text = get_token(bds, api_key)
                    # Everything is OK
                    if status_code == httplib.OK:
                        print bdcli_str + MSG_GET_TOKEN_SUCCESS
                        token_exists = True
                    else:
                        process_common_http_status_codes(status_code, OP_GET_TOKEN)

                if key_exists and token_exists:
                    print bdcli_str + 'API Key: ' + str(api_key)
                    print bdcli_str + 'Access Token: ' + str(access_token)

        # Save the key and token in auth file (.bdcli) in home directory
        # If creating auth file for the first time, create and empty dict
        if not os.path.isfile(auth_file_path):
            with open(auth_file_path, 'w') as f:
                f.write('{}')

        if key_exists and token_exists:
            with open(auth_file_path, 'r') as f:
                auth_dict = json.load(f)
                auth_dict[server] = {"key": str(api_key), "token": str(access_token)}  # Replace key and token for server

                with open(auth_file_path, 'w') as f:
                    json.dump(auth_dict, f, indent=4, sort_keys=True)  # Write dict to auth file


# Check if the existing key or token is valid or not
def check_key_token(string_type, bds, auth_file_path):
    """

    :param string_type: String indicating whether to check for a token or key. Accepted values are "key" and "token".
    :return: True and value of key or token, it it's valid. False in other cases.
    """
    try:

        # Get current server name
        server = bds.split("://")[1]

        # Check if auth file exists
        if os.path.isfile(auth_file_path):

            # Read file contents
            with open(auth_file_path, "r") as f:
                auth_dict = json.load(f)

                # Check if server name matches
                if server in auth_dict:

                    # Get key or token value based on string_type
                    value = auth_dict[server][string_type]

                    if string_type == 'key':
                        # Make sure that some key value exists
                        if value is not None and value != "":
                            return True, value
                        # If key value if empty, return false
                        else:
                            return False, None

                    elif string_type == 'token':
                        # Make sure that some token value exists
                        if value is not None and value != "":
                            # Check validity of token
                            token_validity, status_code, status_text = check_token_validity(bds, value)

                            if token_validity is not None and token_validity["found"] == "true":

                                if "ttl" in token_validity and token_validity["ttl"] > 0:
                                    # Token is present and unexpired
                                    return True, value
                            else:
                                # Token doesn't exist or received an error status when trying to check validity
                                return False, None
                        # If token value if empty, return false
                        else:
                            return False, None
                else:
                    return False, None

        # If auth file doesn't exist, return false
        else:
            return False, None
    except ValueError:
        return False, None


def generate_url_with_credentials(protocol, server):
    """
    This method prompts for username and password to generate the fully qualified BD URL

    :param protocol: http or https
    :param server: BD server hostname
    :return: BD URL in the format <protocol>://<username>:<password>@<hostname>
    """

    username = raw_input('Username: ')
    password = getpass.getpass()

    bd_url = protocol + "://" + username + ":" + password + "@" + server

    return bd_url
