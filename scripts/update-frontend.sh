#!/bin/bash

#Colors (use ${COLOR_NAME})
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

echo -e "${LIGHT_YELLOW}#-----------------------------------#"
echo -e "${LIGHT_YELLOW}#- Stopping cowaticook-frontend... -#"
echo -e "${LIGHT_YELLOw}#-----------------------------------#"

sudo systemctl stop cowaticook-frontend

echo -e "${LIGHT_YELLOW}#------------------------------#"
echo -e "${LIGHT_YELLOW}#- Removing the old folder... -#"
echo -e "${LIGHT_YELLOw}#------------------------------#"

rm -rf /home/cowaticook/cowaticook-frontend

echo -e "${LIGHT_CYAN}#-----------------------------#"
echo -e "${LIGHT_CYAN}#- Downloading the update... -#"
echo -e "${LIGHT_CYAN}#-----------------------------#"

git clone git@github.com:COWaticook-Team/cowaticook-frontend.git

echo -e "${LIGHT_CYAN}#--------------------------------#"
echo -e "${LIGHT_CYAN}#- Downloading node packages... -#"
echo -e "${LIGHT_CYAN}#--------------------------------#"

cd /home/cowaticook/cowaticook-frontend/cowaticookapp && npm install

echo -e "${LIGHT_YELLOW}#-------------------------------------#"
echo -e "${LIGHT_YELLOW}#- Restarting cowaticook-frontend... -#"
echo -e "${LIGHT_YELLOw}#-------------------------------------#"

sudo systemctl restart cowaticook-frontend

echo -e "${LIGHT_GREEN}#---------#"
echo -e "${LIGHT_GREEN}#- Done! -#"
echo -e "${LIGHT_GREEN}#---------#"
