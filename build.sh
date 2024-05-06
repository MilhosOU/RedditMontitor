#!/bin/bash

cd /root/Routines/Valpiccola/RedditMontitor
git pull origin main
. ./set_env_variables.sh
python main.py
