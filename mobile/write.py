#!/usr/bin/python3
from requests import *

try:
    api_key = input("Input API Key : ")
    field = input("Input the field : ")
    data = input("Input the data : ")
except:
    print("\nStopped by User")
    exit()

url = f"https://api.thingspeak.com/update?api_key={api_key}&field{field}={data}"

print(url)

r = get(url)

if r.status_code == 200 :
    print("Connect \033[1;32;40m Success \033[0;37;40m !")
else:
    print(f"Connect \033[1;31;40m Failed \033[0m 1;31;40m with Status Code : \033[0;34;47m {r.status_code} \033[0m")


