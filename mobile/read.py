#!/usr/bin/python3
from requests import *

# https://api.thingspeak.com/channels/1144451/feeds.json?api_key=5GZE4PVFW5OST0G7&results=2

try:
    api_key = input("Input API Key : ")
    channel = input("Input the Channel : ")
    result = input("Input the result : ")
except:
    print("\nStopped by User")
    exit()

url = f"https://api.thingspeak.com/channels/{channel}/feeds.json?api_key={api_key}&results={result}"

print(url)

r = get(url)

if r.status_code == 200 :
    print("Connect \033[1;32;40m Success \033[0;37;40m !")
else:
    print(f"Connect \033[1;31;40m Failed \033[0m 1;31;40m with Status Code : \033[0;34;47m {r.status_code} \033[0m")


