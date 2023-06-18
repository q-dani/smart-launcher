# smart-launcher
Launcher for various AI tools


These instructions are very basic at the moment but will be expanded.

## Environment
* Python 3
* Pop-OS! 20.04 LTS
```
mkdir -p ~/AI/vault/ ~/AI/software
cd ~/AI/vault
mkdir embeddings log misc models outputs run-logs scripts
cd models
mkdir checkpoints Lora LyCORIS VAE
cd ../outputs
mkdir txt2img-images extra-images img2img-images save txt2img-grids
cd ~/AI/vault

git clone https://github.com/q-dani/smart-launcher.git
```
