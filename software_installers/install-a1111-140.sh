#!/bin/bash
cd ..
git clone -b v1.4.0 --depth 1 https://github.com/AUTOMATIC1111/stable-diffusion-webui.git ../../software/a1111-140
echo Launching Smart Launcher installer...
cd installers
./install-launcher-a1111-140.sh
echo Launching Smart Launcher Shortcut installer...
cd ../shortcuts
./install-shortcut-a1111-140.sh
