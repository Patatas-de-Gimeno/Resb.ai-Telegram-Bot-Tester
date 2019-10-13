import requests
from pprint import pprint


def request_respbai(image_url):
    url = 'https://api-eu.restb.ai/vision/v2/predict'
    # A list of lists of dictionaries that contains the objects.
    detections_jsons = list()
    # A list of strings which are the objects we are looking for
    final_responses = list()

    payload = {
        "client_key": "f59efc7d6b2dc753e9d803d64d4eb30981174252cc6b1d2c1a43fe2a4feedd67",
        'model_id': 're_appliances',
        "image_url": image_url
    }
    re_appliances = requests.get(url, params=payload).json()
    detections_jsons.append(re_appliances['response']['solutions']['re_appliances']['detections'])

    payload['model_id'] = 're_features_v3'
    re_features_v3 = requests.get(url, params=payload).json()
    detections_jsons.append(re_features_v3['response']['solutions']['re_features_v3']['detections'])

    payload['model_id'] = 're_compliance'
    re_compliance = requests.get(url, params=payload).json()
    detections_jsons.append(re_compliance['response']['solutions']['re_compliance']['detections'])

    payload['model_id'] = 're_kitchen_finishes'
    re_kitchen_finishes = requests.get(url, params=payload).json()
    detections_jsons.append(re_kitchen_finishes['response']['solutions']['re_kitchen_finishes']['detections'])

    for detections in detections_jsons:
        for elem in detections:
            for key in elem:
                if key == 'label':
                    final_responses.append(elem[key])

    return final_responses
