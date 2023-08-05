""":mod:`ugoira.lib` --- Ugoira Download Library
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Ugoira Download Library

"""

import json
import pathlib
import re
import tempfile
import zipfile

from requests import Session
from wand.image import Image

__all__ = (
    'PixivError',
    'download_zip',
    'is_ugoira',
    'make_gif',
    'pixiv',
    'pixiv_url',
    'save_zip',
    'ugoira_data_regex',
    'user_agent',
)

#: (:class:`str`) User-Agent for fake
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:34.0)' + \
             ' Gecko/20100101 Firefox/34.0'

#: (:class:`dict`) URLs needed by API
pixiv_url = {
    'image-main': ('http://www.pixiv.net/member_illust.php'
                   '?mode=medium&illust_id={}'),
}

#: (:class:`requests.Session`) requests Session for keep headers
pixiv = Session()
pixiv.headers['User-Agent'] = user_agent


#: (:class:`re.regex`) regular expression for grep login field data
login_field_regex = re.compile(
    '<input type="hidden" id="init-config" class="json-data" value=\'(.+)\'>'
)

#: (:class:`re.regex`) regular expression for grep ugoira data
ugoira_data_regex = re.compile(
    r'pixiv\.context\.ugokuIllustData\s*=\s*'
    '(\{"src":".+?","mime_type":".+?","frames":\[.+?\]\})'
)


class PixivError(Exception):
    """Error with Pixiv"""


def is_ugoira(illust_id: int):
    """Check this image type.

    :param illust_id: Pixiv illust_id
    :type illust_id: :class:`int`
    :return: Which is ugoira or not.
    :rtype: :class:`bool`

    """

    res = pixiv.get(pixiv_url['image-main'].format(illust_id))
    return '_ugoku-illust-player-container' in res.text


def download_zip(illust_id: int):
    """Download ugoira zip archive.

    :param illust_id: Pixiv illust_id
    :type illust_id: :class:`int`
    :return: zip file bytes(:class:`bytes`) and frame data(:class:`dict`)
    :rtype: :class:`tuple`
    :raise PixivError: If fail to access to image file.

    """

    image_main_url = pixiv_url['image-main'].format(illust_id)
    res = pixiv.get(image_main_url)
    data = json.loads(ugoira_data_regex.search(res.text).group(1))
    pixiv.headers['Referer'] = image_main_url
    res = pixiv.head(data['src'])
    if res.status_code != 200:
        raise PixivError('Wrong image src. Please report it with illust-id')
    res = pixiv.get(data['src'])
    if res.status_code != 200:
        raise PixivError('Can not download image zip')
    frames = {f['file']: f['delay'] for f in data['frames']}
    return res.content, frames


def make_gif(filename: str, file_data: bytes, frames: dict, acceleration=1.0):
    """Make GIF file from given file data and frame data.

    :param filename: filename of dest
    :type filename: :class:`str`
    :param file_data: zip file bytes from :func:`ugoira.lib.download_zip`
    :type file_data: :class:`bytes`
    :param frames: dict of each frames delay by frame filename
    :type frames: :class:`dict`
    :param acceleration: speed acceleration control
    :type acceleration: :class:`float`

    """

    with tempfile.TemporaryDirectory() as tmpdirname:
        file = pathlib.Path(tmpdirname) / 'temp.zip'
        with file.open('wb') as f:
            f.write(file_data)
        with zipfile.ZipFile(str(file)) as zipf:
            files = zipf.namelist()
            first_image = zipf.read(files[0])

            with Image(blob=first_image) as img:
                width = img.width
                height = img.height

            with Image(width=width,
                       height=height) as container:
                with container.convert('gif') as gif:
                    gif.sequence.clear()  # remove first empty frame
                    for file in files:
                        with Image(blob=zipf.read(file)) as part_image:
                            with part_image.convert('gif') as part_gif:
                                part = part_gif.sequence[0]
                                gif.sequence.append(part)
                                with gif.sequence[-1]:
                                    gif.sequence[-1].delay = \
                                        int(frames[file]//10//acceleration)

                    gif.save(filename=filename)


def save_zip(filename: str, blob: bytes):
    """Make ZIP file from given file data.

    :param filename: filename of dest
    :type filename: :class:`str`
    :param file_data: zip file bytes from :func:`ugoira.lib.download_zip`
    :type file_data: :class:`bytes`

    """

    with open(filename, 'wb') as f:
        f.write(blob)
