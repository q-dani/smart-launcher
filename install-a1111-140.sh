#!/bin/bash
git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui.git ~/AI/software/a1111-140
rm -rf ~/AI/software/a1111-140/embeddings
rm -rf ~/AI/software/a1111-140/models/Stable-diffusion
rm -rf ~/AI/software/a1111-140/models/VAE
echo Launching Smart Launcher installer...
cd ~/AI/vault/smart-launcher/
./install-launcher-a1111-140.sh
echo Launching Smart Launcher Shortcut installer...
cd shortcuts
./install-shortcut-a1111-140.sh
