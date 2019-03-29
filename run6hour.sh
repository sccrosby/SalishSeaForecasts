#!/bin/bash

PATH=/home/crosby/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:

cd /home/crosby/Documents/SalishSeaForecasts

python DownloadHRDPS.py

python ProcessHRDPS.py

python CreateLUTForecasts.py

python PlotWindWave.py

python MakeWindValidation.py

python DownloadWW3.py

python MakeSwellForecast.py

python UploadToWWU.py

