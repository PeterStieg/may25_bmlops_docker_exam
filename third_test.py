import requests
import json
import time
import os

# ### USER DATA
# Get usernames and passwords from JSON file
try:
    with open("users.json", "r", encoding="utf-8") as user_file:
        users = json.load(user_file)
except FileNotFoundError:
    print("File with registered users not found. Please check the file path.")
    users = {}

# ### CONTENT DATA
# Get sentences to check
try:
    with open("content.txt", "r", encoding="utf-8") as content_file:
        lines = content_file.readlines()
        # Remove newline characters
        sentences = [line.strip() for line in lines]
except FileNotFoundError:
    print("File with content not found. Please check the file path.")
    sentences = ""


# ### TIME CONFIGURATION
# Get current time
current_time = time.localtime()

# Format time string: Day. Month Year: Hours:Minutes:Seconds
formatted_time = time.strftime("%d. %B %Y: %H:%M:%S", current_time)


# ### API CONFIGURATION
# API address
api_address = os.environ.get("API_HOST", "http://172.17.0.1")

# API port
api_port = 8000

# API URL for permissions
api_url = f"{api_address}:{api_port}/permissions"

for username, password in users.items():

    # Request to the API
    r = requests.get(url=api_url, params={"username": username, "password": password})

    # Get status code
    status_code = r.status_code

    # Display test status
    if status_code == 200:
        test_status = "SUCCESS"
    else:
        test_status = "FAILURE"

    permissions = r.json().get("permissions", "No permissions found")

    if test_status == "SUCCESS":

        for permission in permissions:

            content_url = f"{api_address}:{api_port}/{permission}/sentiment"

            for sentence in sentences:

                content_r = requests.get(
                    url=content_url,
                    params={
                        "username": username,
                        "password": password,
                        "sentence": sentence,
                    },
                )

                score = content_r.json().get("score", "No score found")

                output = f"""
                ================================================
                Content test // {formatted_time}
                ================================================
                request done at "{content_url}"
                | username = "{username}"
                | password = "{password}"
                | sentence = "{sentence}"
                | score = "{score}"
                {'expected result = 200' if username != 'clementine' else 'expected result = 403'}
                actual result = {status_code}
                ==>  {test_status}
                """

                print(output)

                # Print output in log file
                if os.environ.get("LOG", "").lower() in ["1", "true", "yes"]:
                    with open("/app/logs/api_test.log", "a") as file:
                        file.write(output)

    else:
        output = f"""
        ================================================
         Content test // {formatted_time}
        ================================================
        request done at "{content_url}"
        | username = "{username}"
        | password = "{password}"
        {'expected result = 200' if username != 'clementine' else 'expected result = 403'}
        actual result = {status_code}
        ==>  {test_status}
        """

        print(output)

    # Print output in log file
    if os.environ.get("LOG", "").lower() in ["1", "true", "yes"]:
        # Create logs directory if it doesn't exist
        os.makedirs("/app/logs", exist_ok=True)
        with open("/app/logs/api_test.log", "a") as file:
            file.write(output)