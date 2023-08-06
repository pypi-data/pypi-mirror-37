import os
import json


def get_model_data():

    file_path = os.path.join(os.getcwd(), 'artifacts', 'KerasVGG16', 'vgg16.tar.gz')
    if not os.path.exists(file_path):
        raise FileNotFoundError("vgg16.tar.gz not found. Please use download_model.sh script to download model.")

    return {
        'path': file_path
    }


def get_scoring_payload():
    file_path = os.path.join(os.getcwd(), 'datasets', 'KerasVGG16', 'scoring_payload.json')
    with open(file_path) as f:
        return json.load(f)
