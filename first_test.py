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

    output = f"""
    ================================================
     Authentication test // {formatted_time}
    ================================================
    request done at "/permissions"
    | username = "{username}"
    | password = "{password}"
    expected result = 200
    actual restult = {status_code}
    ==>  {test_status}
    """

    print(output)

    # Print output in log file
    if os.environ.get("LOG", "").lower() in ["1", "true", "yes"]:
        with open("logs/api_test.log", "a") as file:
            file.write(output)
