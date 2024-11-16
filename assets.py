#!/usr/bin/env python3
import datetime
import os
from pathlib import Path
from dateutil.parser import parse as parsedate

import requests

ASSETS_URL = os.environ.get('TECHMAN83_ME_ASSETS', '').rstrip('/')
ASSETS = [
    'favicon.ico',
    'leon-vr.png',
    'feed-icon.png',
    'assets/me.jpeg',
]
for file_path in Path('source', 'posts').rglob('**/*.md'):
    with file_path.open('r', encoding='utf-8') as file:
        for line in file:
            if not line.startswith('```{thumbnail}'):
                continue
            ASSETS.append(line[16:].strip())

class CacheFile:
    output_path: Path
    source_url: str

    def __init__(self, output_path: str, source_url: str):
        self.output_path = Path('source', output_path)
        self.source_url = source_url

    def download_if_changed(self):
        # Send a HEAD request to get headers
        response = requests.head(self.source_url)

        # Check if 'Last-Modified' header is present
        if 'Last-Modified' not in response.headers:
            print(f"No 'Last-Modified' header found. Downloading {self.source_url}.")
            self.download_file()
            return

        # Parse the 'Last-Modified' header
        server_last_modified = parsedate(response.headers['Last-Modified']).astimezone()

        # Check if the local file exists
        if self.output_path.exists():
            # Get the local file's last modified time
            local_last_modified = datetime.datetime.fromtimestamp(
                self.output_path.stat().st_mtime
            ).astimezone()

            # Compare the server and local modification times
            if server_last_modified <= local_last_modified:
                print(f"{self.output_path} is up-to-date. No download needed.")
                return

        # Download the file if it's newer
        print(f"Downloading {self.source_url}")
        self.download_file()

        # Update the local file's timestamp
        self.output_path.touch(exist_ok=True)

    def download_file(self):
        self.output_path.parent.mkdir(exist_ok=True,parents=True)
        response = requests.get(self.source_url, stream=True)
        with self.output_path.open('wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

for asset in ASSETS:
    cache = CacheFile(output_path=asset, source_url=f'{ASSETS_URL}/{asset}')
    cache.download_if_changed()

# Hack for contrib-images
images = "sphinxcontrib_images-0.9.4-py3-none-any.whl"
cache = CacheFile(output_path=f"../{images}", source_url=f'{ASSETS_URL}/{images}')
cache.download_if_changed()
