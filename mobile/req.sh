#!/usr/bin/env bash


if [ "$1" == "" ] || [ "$1" == "--help" ]
then
	echo "Please input [API Key] [Field] [Data]"
	exit
fi

if [ "$#" == "3" ] || [ "$#" > "3" ]
then
	#$url = "https://api.thingspeak.com/update?api_key=" + "$1" + "&field" + "$2" + "=" + "$3" 
	#curl $url
	curl https://api.thingspeak.com/update?api_key="$1"\&field"$2"="$3"
	#echo 'https://api.thingspeak.com/update?api_key="$1"&field"$2"="$3"'
	echo 	
	echo  https://api.thingspeak.com/update?api_key="$1"\&field"$2"="$3"
fi


