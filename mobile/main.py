#!/usr/bin/python3
from req import *

class data_set:
    def __init__(self, api_key, mode, field=1, data=None, channel_id=None):
        self.api_key = api_key
        self.field = field
        self.data = data
        self.channel_id = channel_id
        self.mode = mode


try:
    api_key = input("Input API Key : ")
    channel = input("Input the Channel : ")
    #result = input("Input the result : ")
except:
    print("\nStopped by User")
    exit()

#req_data = data_set("XXX", "read_field", 1)

req_data = data_set(api_key , "write", 1 , 123 , )
req_data.channel_id = int(channel)
send_req(req_data)
