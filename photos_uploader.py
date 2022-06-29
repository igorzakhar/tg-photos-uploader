import pathlib

from urllib.parse import unquote
from urllib.parse import urlsplit

import requests


def download_image(url, path):
    url_path = unquote(urlsplit(url).path)
    filename = pathlib.PurePath(url_path).name.replace(' ', '_')
    file_path = pathlib.PurePath(path).joinpath(filename)

    response = requests.get(url)
    response.raise_for_status()

    with open(file_path, 'wb') as file:
        file.write(response.content)


def main():
    images_path = pathlib.Path.cwd() / 'images'
    url = "https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg"

    pathlib.Path.mkdir(images_path, exist_ok=True)
    download_image(url, images_path)


if __name__ == '__main__':
    main()
