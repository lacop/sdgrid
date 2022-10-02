from BunnyCDN.Storage import Storage
import glob
import os
import tqdm

api_key = os.environ.get('API_KEY')
local_image_dir = os.environ.get('LOCAL_IMAGE_DIR')
local_html_dir = os.environ.get('LOCAL_HTML_DIR')
bucket = os.environ.get('CDN_BUCKET', 'sdgrid')

obj_storage = Storage(api_key, bucket)

def sync_prefix(local_prefix, cdn_prefix, pattern):
    print('Sycning {prefix}')

    local_files = set([
        f[len(local_prefix)+1:]
        for f in glob.glob(os.path.join(local_prefix, pattern))])  
    print('Found {} files locally'.format(len(local_files)))

    remote_files = set()
    # API is broken...
    if cdn_prefix != '/':
        remote_files = set([
            f['File_Name']
            for f in obj_storage.GetStoragedObjectsList(cdn_prefix)])
        print('Found {} files on CDN'.format(len(remote_files)))

    missing_files = list(local_files - remote_files)
    for file in tqdm.tqdm(missing_files):
        obj_storage.PutFile(file, os.path.join(cdn_prefix, file), local_prefix)

if local_image_dir:
    for prefix in ['256', '512']:
        local_prefix = os.path.join(local_image_dir, prefix)
        cdn_prefix = os.path.join('/images', prefix)
        sync_prefix(local_prefix, cdn_prefix, '*.jpg')

if local_html_dir:
    sync_prefix(local_html_dir, '/', '*.html')