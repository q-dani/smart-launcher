#!/bin/bash
cp files/SD-A1111.desktop ~/.local/share/applications/
if [[ ! -e ~/.icons ]]; then
    mkdir ~/.icons
fi
cp files/sd.png ~/.icons/
echo Smart Launcher shortcut for SD-A1111 installed!
