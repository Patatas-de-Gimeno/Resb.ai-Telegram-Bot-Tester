from datetime import datetime
import os

album = None
image_path = 'image.jpg'


def imgur_upload(client):
    """Uploads and image to imgur
    """
    config = {
        'album': album,
        'name': 'AI image',
        'title': 'Object detect image',
        'description': 'An image we will use to deep learning {0}'.format(datetime.now())
    }

    print('Uploading image...')
    image = client.upload_from_path(os.path.join(os.getcwd(), image_path), config=config, anon=False)
    print("Done")

    return image
