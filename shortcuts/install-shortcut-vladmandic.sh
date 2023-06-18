#!/bin/bash
cp files/SD-Vladmandic.desktop ~/.local/share/applications/
if [[ ! -e ~/.icons ]]; then
    mkdir ~/.icons
fi
cp files/vladmandic.png ~/.icons/
echo Smart Launcher shortcut for SD-Vladmandic installed!
