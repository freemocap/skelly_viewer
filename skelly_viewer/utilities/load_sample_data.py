import io
import logging
import zipfile
from pathlib import Path

import requests

from skelly_viewer.config.default_paths import get_base_folder_path
from skelly_viewer.config.folder_and_file_names import SAMPLE_DATA_FILE_NAME

SAMPLE_DATA_URL = zip_file_url = 'https://figshare.com/ndownloader/files/39369101'

logger = logging.getLogger(__name__)
def load_sample_data():
    sample_recording_path = get_base_folder_path() / SAMPLE_DATA_FILE_NAME.split('.')[0]
    if not Path.exists(sample_recording_path):
        logger.info(f"Downloading sample data from: {SAMPLE_DATA_URL}")
        r = requests.get(SAMPLE_DATA_URL)
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall(sample_recording_path.parent)
    logger.info(f"Returning sample data path: {sample_recording_path}")
    return sample_recording_path

