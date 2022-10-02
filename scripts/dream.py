import base64
import csv
import glob
import itertools
import os
import requests
from tqdm import tqdm

from common import filename_for

topics_file = os.environ.get('TOPICS_FILE', 'inputs/topics.csv')
styles_file = os.environ.get('STYLES_FILE', 'inputs/styles.csv')
output_dir = os.environ.get('OUTPUT_DIR', 'outputs')
sdapi = os.environ.get('SDAPI', 'http://localhost:7860')

IMAGE_COUNT = 4

try:
    os.mkdir(output_dir)
except:
    pass

styles = []
topics = []
with open(styles_file) as f:
    styles = list(csv.DictReader(f))
with open(topics_file) as f:
    topics = list(csv.DictReader(f))

print('Loaded {} styles and {} topics for a total of {} prompts and {} images'.format(
    len(styles),
    len(topics),
    len(styles)*len(topics),
    len(styles)*len(topics)*IMAGE_COUNT))

def save_image(encoded, prompt, number):
    filename = filename_for(prompt, number)
    # Temp file + atomic rename
    tmp_name = os.path.join(output_dir, '_temp-{}.png'.format(filename))
    with open(tmp_name, 'wb') as f:
        payload = encoded[len('data:image/png;base64,'):]
        f.write(base64.b64decode(payload))
    os.rename(tmp_name, os.path.join(output_dir, '{}.png'.format(filename)))

def generate_images(prompt):
    r = requests.post(sdapi + '/api/predict/',
        json = {
            'fn_index': 12,
            'data': [
                prompt,
                '',
                'None',
                'None',
                75, # Sampling steps
                'LMS', # Sampler
                False,
                False,
                1,
                4, # Batch size
                7, # Scale
                42, # Seed (for first image)
                -1, 0, 0, 0,
                False,
                512, 512,
                False, False,
                0.7,
                'None',
                False, False, None, '', 'Seed', '', 'Steps', '', True, False, None,
                '', '',
                ]
        },
    )
    result = r.json()
    # TODO upscale?
    for (i, encoded) in enumerate(result['data'][0][1:]):
        save_image(encoded, prompt, i)

existing_files = set([
    f[len(output_dir)+1:]
    for f in glob.glob(os.path.join(output_dir, '*.png'))
    if '_temp-' not in f])  
print('Found {} existing images which will be skipped'.format(len(existing_files)))

for (style, topic) in tqdm(list(itertools.product(styles, topics))):
    prompt = style['prompt'].replace('$1', topic['topic'])
    
    if all('{}.png'.format(filename_for(prompt, i)) in existing_files
           for i in range(IMAGE_COUNT)):
        tqdm.write(f'SKIP: {prompt}')
        continue
    tqdm.write(f'GENERATING: {prompt}')
    generate_images(prompt)