import shutil
import requests
import zipfile
import io
import os
import time
import configparser
print("Welcome to the MissionChiefBot Installer!")
print("Note: bot could be against TOS so use at your own risk!")


def password_check():
    s = input("Server: ").lower()
    e = input("Email: ")
    p = input("Password: ")
    print("You have entered the following details:")
    print("Server:", s)
    print("Email:", e)
    print("Password:", '*' * len(p))
    return s, e, p


server, email, password = password_check()

print("If this is correct please type 'yes' otherwise, type 'no'")

confirmation = input().lower()

if confirmation == 'yes':
    print("Installing...")
    if server == 'na':
        api_url = "https://api.github.com/repos/NatesHonor/MissionchiefBot/releases/latest"
    elif server == 'eu':
        api_url = "https://api.github.com/repos/NatesHonor/MissionchiefBotEU/releases/latest"
    headers = {"Accept": "application/vnd.github.v3+json"}

    response = requests.get(api_url, headers=headers)
    data = response.json()

    zip_url = data['zipball_url']

    response = requests.get(zip_url)
    zip_file = zipfile.ZipFile(io.BytesIO(response.content))

    os.makedirs('Bot', exist_ok=True)

    zip_file.extractall('Bot')

    extracted_folder = [name for name in os.listdir('Bot') if os.path.isdir(os.path.join('Bot', name))][0]

    extracted_path = os.path.join('Bot', extracted_folder)
    target_path = 'Bot'

    for filename in os.listdir(extracted_path):
        shutil.move(os.path.join(extracted_path, filename), target_path)

    os.rmdir(extracted_path)
    config = configparser.ConfigParser()
    config['credentials'] = {'username': email, 'password': password}
    config['client'] = {'headless': 'true'}
    config['missions'] = {
        'should_wait_before_missions': 'true',
        'should_wait_before_missions_time': '5',
        'should_handle_transport_requests': 'true',
        'should_handle_transport_requests_time': '60'
    }
    config['transport'] = {'prisoner_van': 'false', 'minimum_prisoners': '3'}
    config['dispatches'] = {'dispatch_type': 'alliance'}
    config['other'] = {
        'daily_login': 'true',
        'event_calender': 'true',
        'claim_tasks': 'true',
        'solve_tasks': 'true'
    }

    # Write the configuration to the 'config.ini' file in the 'Bot' directory
    with open(os.path.join('Bot', 'config.ini'), 'w') as configfile:
        config.write(configfile)
else:
    print("Restarting Installation Process")
    time.sleep(2)
    password_check()
