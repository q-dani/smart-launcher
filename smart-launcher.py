#!/usr/bin/env python3
""" Handles symlinks for reducing storage needs when using various AI programs
that have common, often large files (like models) while providing a seemless 
way to launch specific AI programs.

Written by Dani

v1.2

"""

# Keep these light to avoid the need for venv or installing extra libs
import sys,os
import json
import argparse

# Argparse
appversion = "%(prog)s v1.2"
parser = argparse.ArgumentParser(description=__doc__,
                            formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("--version", action="version", version=appversion)
parser.add_argument("-c", "--config", default='smart-launcher.json', help='JSON config file')
parser.add_argument("-f", "--force", action="store_true", help='Automatically delete existing files/directories when creating symlinks, default behaviour is to print an error and skip that symlink.')
parser.add_argument("-s", "--share", action="store_true", help='If supported for a given peice of software, it will be launched with a flag that generates a public URL for use. Warning, this will disable your ability to install/upgrade/uninstall extensions until restarted without this flag!')
parser.add_argument("-p", "--profile", default='AI', help='gnome-terminal profile to use when launching')
parser.add_argument("-l", "--skip-launch", action="store_true", help='Skip launching software, useful for symlink/config changes')

args = parser.parse_args()

#Global Vars
config_filename = args.config
term_profile = args.profile

# Verify config file exists and exit if it doesnt
if not os.path.isfile(config_filename):
    sys.exit('Error, configuration file ' + config_filename + ' is missing! Exiting!')

# Load config file
with open(os.path.expanduser(config_filename), 'r') as f:
    json_config = json.load(f)

def check_valid_symlink(path):
    if os.path.islink(path):
        if not os.path.exists(path):
            return False
        else:
            return True
    else:
        return False

def check_valid_symlink_and_clean(path):
    if os.path.islink(path):
        if not os.path.exists(path):
            os.unlink(path)
            return False
        else:
            return True
    else:
        return False

# Symlink logic
print('Checking symlinks...')
if json_config['use_vault'] is True:
    for vault_item in json_config['vault']:
        if vault_item['enabled'] != True:
            continue
        print('Checking symlinks for ' + vault_item['name'])
        
        # Single file symlink type
        if vault_item['link_type'] == 'file':
            check_valid_symlink_and_clean(vault_item['program_rel_path'])
            if not os.path.exists(vault_item['program_rel_path']):
                os.symlink(os.path.abspath(os.path.join(os.path.expanduser(json_config['vault_path']), vault_item['vault_rel_path'])),os.path.abspath(vault_item['program_rel_path']))
            else:
                if not os.path.islink(vault_item['program_rel_path']):
                    print(vault_item['program_rel_path'] + ' already exists!')

                    if args.force:
                        print(f'Deleting file {vault_item["program_rel_path}"]} and creating symlink...')
                        os.unlink(vault_item['program_rel_path'])
                        os.symlink(os.path.abspath(os.path.join(os.path.expanduser(json_config['vault_path']), vault_item['vault_rel_path'])),os.path.abspath(vault_item['program_rel_path']))
                    else:
                        print('This will be skipped. To fix this, backup and remove this file or run with the --force flag')
        
        # Single folder symlink type
        elif vault_item['link_type'] == 'folder':
            check_valid_symlink_and_clean(vault_item['program_rel_path'])
            if not os.path.exists(vault_item['program_rel_path']):
                os.symlink(os.path.abspath(os.path.join(os.path.expanduser(json_config['vault_path']), vault_item['vault_rel_path'])),os.path.abspath(vault_item['program_rel_path']))
            else:
                if not os.path.islink(vault_item['program_rel_path']):
                    print(vault_item['program_rel_path'] + ' already exists!')

                    if args.force:
                        print(f'Deleting folder {vault_item["program_rel_path"]}, all contents, and creating symlink...')
                        shutil.rmtree(vault_item["program_rel_path}"])
                        os.symlink(os.path.abspath(os.path.join(os.path.expanduser(json_config['vault_path']), vault_item['vault_rel_path'])),os.path.abspath(vault_item['program_rel_path']))
                    else:
                        print('This will be skipped. To fix this, move any contents to the vault folder and delete this folder or run with the --force flag')
                
        # Folder contents (files only)
        elif vault_item['link_type'] == 'contents':
            for filename in os.listdir(os.path.abspath(os.path.join(os.path.expanduser(json_config['vault_path']), vault_item['vault_rel_path']))):
                check_valid_symlink_and_clean(os.path.join(vault_item['program_rel_path'],filename))
                if not os.path.exists(os.path.join(vault_item['program_rel_path'],filename)):
                    os.symlink(os.path.abspath(os.path.join(os.path.expanduser(json_config['vault_path']), vault_item['vault_rel_path'], filename)),os.path.abspath(os.path.join(vault_item['program_rel_path'],filename)))
                else:
                    if not os.path.islink(os.path.join(vault_item['program_rel_path'],filename)):
                        print(os.path.join(vault_item['program_rel_path'],filename) + ' already exists!')

                        if args.force:
                            print(f'Deleting file {os.path.join(vault_item["program_rel_path"],filename)} and creating symlink...')
                            os.unlink(os.path.join(vault_item['program_rel_path'],filename))
                            os.symlink(os.path.abspath(os.path.join(os.path.expanduser(json_config['vault_path']), vault_item['vault_rel_path'], filename)),os.path.abspath(os.path.join(vault_item['program_rel_path'],filename)))
                        else:
                            print('This will be skipped. To fix this, move any contents to the vault folder and delete this file or run with the --force flag')   
                
## Launch the application
if not args.skip_launch:
    # Build launch command
    gnome_term_title = json_config['software_name']
    working_directory = os.path.abspath(os.getcwd())
    share_flag = ''
    if args.share:
        if not "share_params" in json_config:
            print('WARNING! Share flag cannot be applied because the configuration is missing from the JSON configuration file!')
            print('Please correct this and restart the launcher.')
        else:
            share_flag = json_config["share_params"]
    sh_launch_string = f'sh -c \'{json_config["launch_script"]} {json_config["launch_params"]} {share_flag}\''
    gnome_term_string = f"/usr/bin/gnome-terminal --tab --working-directory=\'{working_directory}\' --profile=\'{term_profile}\' --title \'{gnome_term_title}\' -- {sh_launch_string}"
    
    # Launch
    print('Launching application...')
    print(f'{gnome_term_string}')
    print('------------------------------')
    print(' ')
    
    os.system(gnome_term_string)
