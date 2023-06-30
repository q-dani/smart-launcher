#!/bin/bash
cp files/SD-A1111-140.desktop ~/.local/share/applications/
cp files/SD-A1111-140-Share.desktop ~/.local/share/applications/
if [[ ! -e ~/.icons ]]; then
    mkdir ~/.icons
fi
cp files/sd.png ~/.icons/
echo Smart Launcher shortcut for SD-A1111 1.4.0 installed!
