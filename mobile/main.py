
from functions import send_request, setup_window
from classes import data_set, device


new_device = device("on")

setup_window(new_device)


try:
    api_key = input("Input API Key : ")
    channel = input("Input the Channel : ")
    #result = input("Input the result : ")
except:
    print("\nStopped by User")
    exit()

#req_data = data_set("XXX", "read_field", 1)

req_data = data_set(api_key, "write", 1, 123)
req_data.channel_id = int(channel)
send_request(req_data)
