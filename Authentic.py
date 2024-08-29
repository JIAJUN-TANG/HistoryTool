import os
import json
import requests

def get_api_key(file_path):
    if not os.path.isfile(file_path):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)
        with open(file_path, "r", encoding="utf-8") as file:
            API_Key_dict = json.load(file)
            return API_Key_dict
    else:
        with open(file_path, "r", encoding="utf-8") as file:
            API_Key_dict = json.load(file)
            return API_Key_dict

def get_authentication(model, api_key):
    if model == "Kimi":
        header = {"Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"}
        balance_url = "https://api.moonshot.cn/v1/users/me/balance"
        response = requests.get(balance_url, headers=header)
        if response.status_code == 200:
            balance_data = response.json()
            balance_data = balance_data["data"]["available_balance"]
            return balance_data
        else:
            return False
    elif model == "文心一言":
        client_id = api_key.get("client_id")
        client_secret = api_key.get("secret_id")
        balance_url = f"https://aip.baidubce.com/oauth/2.0/token?client_id={client_id}&client_secret={client_secret}&grant_type=client_credentials"
        payload = json.dumps("")
        headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
        response = requests.request("POST", balance_url, headers=headers, data=payload)
        if response.status_code == 200:
            return response.status_code
        else:
            return False
    elif model == "ChatGPT":
        api_key = api_key
        balance_url = "https://api.chatanywhere.tech/v1/query/usage_details"

        payload = json.dumps({
   "model": "gpt-4o-mini%",
   "hours": 24
})
        headers = {
   "Authorization": api_key,
   "Content-Type": "application/json"
}
        response = requests.request("POST", balance_url, headers=headers, data=payload)
        if response.status_code == 200:
            balance_data = response.json()
            balance_data = dict(balance_data[0]).get("cost") + 30
            return balance_data
        else:
            return False
    
    else:
        return False
    
        