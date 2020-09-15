from requests import *

def send_req(req_data):

    api_key = req_data.api_key
    if api_key == None:
        print("Illegal api_key")

    mode = req_data.mode
    if mode == None:
        print("Illegal mode")

    field = req_data.field
    data = req_data.data
    channel_id = req_data.channel_id

    raw_url = "https://api.thingspeak.com"
    url = {
        "read_field": f"{raw_url}/channels/{channel_id}/fields/{field}.json?api_key={api_key}&results=1",
        "read_feed": f"{raw_url}/channels/{channel_id}/feeds.json?api_key={api_key}&results=1",
        "write": f"{raw_url}/update?api_key={api_key}&field{field}={data}"
    }

    if url[mode] == None:
        print("Illegal url")

    print(url[mode])
    r = get(url[mode])

    parse_methods = {
        "read_field": f"response:{r.json()['feeds'][0][f'field{field}']}"
    }

    if r.status_code == 200:
        print("Connect \033[1;32;40m Success \033[0;37;40m !")
        print(parse_methods[mode])
