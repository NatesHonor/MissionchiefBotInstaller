import shutil
import requests
import zipfile
import io
import os
import time
import configparser


def installation_check():
    print("Are you installing or updating the bot?")
    print("Type 'install' for installation, 'update' for updating, or 'exit' to quit.")
    return input().lower()


def dashboard_check():
    print("Would you like to install the bot management dashboard?")
    print("Type 'yes' to install, 'no' to skip.")
    return input().lower()


def password_check():
    while True:
        s = input("Server: ").lower()
        if s not in ['na', 'eu']:
            print("Invalid server. Please enter either 'na' or 'eu'.")
            continue
        e = input("Email: ")
        p = input("Password: ")
        print("You have entered the following details:")
        print("Server:", s)
        print("Email:", e)
        print("Password:", '*' * len(p))
        return s, e, p


print("Welcome to the MissionChiefBot Installer!")
print("Note: bot could be against TOS so use at your own risk!")

installation = installation_check()

if installation == 'exit':
    print("Exiting the installer.")
    exit()

dashboard = dashboard_check()

if dashboard == 'no' and installation == 'install':
    print("Skipping dashboard installation.")
    exit()

server, email, password = password_check()

print("If this is correct please type 'yes' otherwise, type 'no'")

confirmation = input().lower()

if confirmation == 'yes':
    print("Installing...")
    if server == 'na':
        api_url = "https://api.github.com/repos/NatesHonor/MissionchiefBot/releases/latest"
    elif server == 'eu':
        api_url = "https://api.github.com/repos/NatesHonor/MissionchiefBotEU/releases/latest"
    else:
        print("Invalid server. Restarting the installer.")
        password_check()

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
    }
    config['transport'] = {
        'should_handle_transport_requests': 'true',
        'should_handle_transport_requests_time': '60',
        'prisoner_van_handling': 'false',
        'minimum_prisoners': '3'
    }
    config['dispatches'] = {'dispatch_type': 'alliance'}
    config['other'] = {
        'daily_login': 'true',
        'claim_tasks': 'true',
        'claim_tasks_time': '5',
        'event_calender': 'true',
    }

    with open('config.ini', 'w') as configfile:
        config.write(configfile)

    with open(os.path.join('Bot', 'config.ini'), 'w') as configfile:
        config.write(configfile)

else:
    print("Restarting Installation Process")
    time.sleep(2)
    password_check()
