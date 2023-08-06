from pathlib import Path
import errno
import os
from collections import namedtuple

from .authsession import AuthSession
from .helpers import asset_safe_name, get_b64_image

class App(AuthSession):
    def __init__(self, id, name, token):
        super().__init__(token)
        self.id = id
        self.name = name
        self.link = f'https://discordapp.com/api/oauth2/applications/{id}/assets'

    def upload_image(self, image_path):
        """ Uploads an image.

            :param str image_path:
                Path to the image to upload.
            :rtype:
                str
            :returns:
                ID of the uploaded image so it can be deleted later.
        """

        safe_path = Path(image_path)

        params = {
            'image': get_b64_image(safe_path),
            'name': asset_safe_name(safe_path.stem),
            'type': 1
        }

        r = self.authreq(
                'POST',
                self.link,
                json=params
        )
        return r.json()['id']

    def delete_image(self, image_id):
        """ Deletes an uploaded image.

            :param str image_id:
                ID of the image to delete.
        """

        link = f'{self.link}/{image_id}'
        self.authreq('POST', link)
