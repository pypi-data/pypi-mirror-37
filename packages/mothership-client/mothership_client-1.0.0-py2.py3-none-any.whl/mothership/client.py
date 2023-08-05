import os, requests
from .exceptions import ConfigError

config = None

def init(obj):
    global config
    config = None
    
    base_url = os.getenv('MOTHERSHIP_BASE_URL', 'https://app.mothership.cloud')
    
    url = '{base_url}/api/configs/retrieve'.format(base_url=base_url)
    headers = {'X-Config-Key': obj['key']}
    r = requests.get(url, headers=headers)
    
    if (r.status_code is not 200):
        raise ConfigError('Failed to fetch the config from the server.')
    
    config = r.json()
    
    return config
    
def get():
    global config
    return config