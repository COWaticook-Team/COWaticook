#!/bin/bash

#Colors (use ${COLOR})
CLEAR='\033[0m'
WHITE='\033[1;37m'
BLACK='\033[1;30m'
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
LIGHT_GRAY='\033[1;30m'
LIGHT_RED='\033[1;31m'
LIGHT_GREEN='\033[1;32m'
LIGHT_YELLOW='\033[1;33m'
LIGHT_BLUE='\033[1;34m'
LIGHT_PURPLE='\033[1;35m'
LIGHT_CYAN='\033[0;36m'

echo -ne "${LIGHT_PURPLE}\n############################\n${PURPLE}"
echo -ne "${LIGHT_PURPLE}#### InfluxDB installer ####\n${PURPLE}"
echo -ne "${LIGHT_PURPLE}############################\n${PURPLE}"

echo -e "${PURPLE}# ${LIGHT_YELLOW}Getting the latest InfluxDB image ${CLEAR}"
docker pull influxdb

echo -e "${PURPLE}# ${LIGHT_YELLOW}Starting InfluxDB ${CLEAR}"
docker run \
	--detach \
	-p 8086:8086 \
	-v myInfluxVolume:/var/lib/influxdb2 \
	--name cowdb \
	--restart=always \
	influxdb:latest

echo -e "${PURPLE}# ${LIGHT_GREEN}Go to http://localhost:8086 to configure InfluxDB\n${CLEAR}"
read -n 1 -s -r -p "Press any key to leave the installer..."

echo -e "\n${PURPLE}# Bye bye :)\n${CLEAR}"

