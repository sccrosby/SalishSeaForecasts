#!/bin/bash

PATH=/home/crosby/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:

cd /home/crosby/Documents/SalishSeaForecasts

python DownloadGDPS.py

python ProcessGDPS.py

python MakeWaterLevelPredictions.py