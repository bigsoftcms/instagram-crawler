# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys, os, json
from io import open
from datetime import datetime
import urllib.request
from urllib.parse import urlparse
import pandas as pd

from inscrawler import InsCrawler
from inscrawler.settings import override_settings
from inscrawler.settings import prepare_override_settings

username = 'taeyeon_ss'
number = 999

target_path = 'result_username'
debug = False

current_timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

target_img_path = os.path.join(target_path, '%s_%s' % (username, current_timestamp))
output_filename = '%s_%s.csv' % (username, current_timestamp)
output_path = os.path.join(target_path, output_filename)

os.makedirs(target_path, exist_ok=True)
os.makedirs(target_img_path, exist_ok=True)

ins_crawler = InsCrawler(has_screen=debug)

results = ins_crawler.get_user_posts(username, number, detail=False)

print('[*] %d results' % len(results))

df = pd.DataFrame(columns=['key', 'caption', 'img_url'])

for result in results:
  # key, caption, img_url
  if '1 person' in result['caption'] and 'closeup' in result['caption']:
    parsed = urlparse(result['img_url'])
    filename = parsed.path.split('/')[-1]
    result['filename'] = filename

    urllib.request.urlretrieve(result['img_url'], os.path.join(target_img_path, filename))

    df = df.append(result, ignore_index=True)

df.to_csv(output_path, index=False)
