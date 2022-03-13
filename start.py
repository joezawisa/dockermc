import argparse
import requests
import os
import sys

# Function to load version manifest
def get_manifest(url):
    r = requests.get(url)
    if r.ok:
        return r.json()
    else:
        print('Error: failed to load manifest', file=sys.stderr)
        sys.exit(1)

# Parse command line arguments
parser = argparse.ArgumentParser(description='Start a minecraft server in Docker.')
parser.add_argument('-v', '--version', metavar='version', type=str, help='minecraft version', required=False, default='latest')
parser.add_argument('-m', '--manifest', metavar='manifest', type=str, help='version manifest', required=False, default='https://launchermeta.mojang.com/mc/game/version_manifest_v2.json')
arguments = vars(parser.parse_args())

# Create required directories if they don't already exist
for directory in ['versions', 'data']:
    if not os.path.exists(directory):
        os.mkdir(directory)

version = arguments['version']
manifest = None

# If the user chose to run the latest version, find out what version that is
if version == 'latest':
    # Get version manifest
    manifest = get_manifest(arguments['manifest'])
    # Get the version number of the latest release from the manifest
    try:
        version = manifest['latest']['release']
    except KeyError:
        print('Error: failed to find latest release in manifest', file=sys.stderr)
        sys.exit(1)

# Check whether we already have the requested version
if not os.path.exists(f'versions/{version}.jar'):
    if manifest is None:
        manifest = get_manifest(arguments['manifest'])

    # If it's missing, find it in the version manifest
    server = None
    try:
        for v in manifest['versions']:
            if v['id'] == version:
                # Get version info
                r = requests.get(v['url'])
                if r.ok:
                    metadata = r.json()
                    server = metadata['downloads']['server']['url']
                else:
                    print('Error: failed to load version info', file=sys.stderr)
                    sys.exit(1)
                break
    except KeyError:
        print('Error: failed to find server URL', file=sys.stderr)
        sys.exit(1)
    
    # Download the server (we do this in chunks since it might be big)
    if server is None:
        print('Error: Requested version not found', file=sys.stderr)
        sys.exit(1)
    else:
        with requests.get(server, stream=True) as r:
            if r.ok:
                with open(f'versions/{version}.jar', 'wb') as jar:
                    for chunk in r.iter_content(chunk_size=1024):
                        if chunk:
                            jar.write(chunk)
            else:
                print('Error: failed to download server', file=sys.stderr)
                sys.exit(1)

# Start the server
os.chdir('./data')
os.execvp(file='java', args=['java', '-Xmx1024M', '-Xms1024M', '-jar', f'../versions/{version}.jar', 'nogui'])