#!/bin/bash
cp files/SD-A1111-132.desktop ~/.local/share/applications/
cp files/SD-A1111-132-Share.desktop ~/.local/share/applications/
if [[ ! -e ~/.icons ]]; then
    mkdir ~/.icons
fi
cp files/sd.png ~/.icons/
echo Smart Launcher shortcut for SD-A1111 1.3.2 installed!
