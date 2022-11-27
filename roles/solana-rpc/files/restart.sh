#!/bin/bash
if [ $# -eq 0 ]
  then
    python3 /mnt/snapcheck.py
fi
sudo systemctl stop sol.service
sudo systemctl start sol.service
