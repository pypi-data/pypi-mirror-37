""" Username to UUID
Converts a Minecraft username to it's UUID equivalent.

Uses the official Mojang API to fetch player data.
"""

### Import necessary modules
import http.client
import json


### Main class
class GetPlayerData:
    def __init__(self, username, timestamp=None):
        self.valid = True
        """
            Get the UUID of the player.

            Parameters
            ----------
            username: string
                The known minecraft username
            timestamp : long integer (optional)
                The time at which the player used this name, expressed as a Unix timestamp.
        """

        # Handle the timestamp
        get_args = ""
        if timestamp is not None:
            get_args = "?at=" + str(timestamp)

        # Request the UUID
        http_conn = http.client.HTTPSConnection("api.mojang.com");
        http_conn.request("GET", "/users/profiles/minecraft/" + username + get_args,
            headers={'User-Agent':'https://github.com/clerie/mcuuid', 'Content-Type':'application/json'});
        response = http_conn.getresponse().read().decode("utf-8")

        # In case the answer is empty, the user dont exist
        if not response:
            self.valid = False
        # If there is an answer, fill out the variables
        else:
            # Parse the JSON
            json_data = json.loads(response)
            # The UUID
            self.uuid = json_data['id']
            # The username written correctly
            self.username = json_data['name']
