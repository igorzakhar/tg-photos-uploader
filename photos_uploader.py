import pathlib
import random

from urllib.parse import unquote
from urllib.parse import urlsplit

import requests


def get_spacex_photos(latest=True):
    spacex_api_url = 'https://api.spacexdata.com/v5/launches'
    response = requests.get(spacex_api_url)
    response.raise_for_status()

    launches = response.json()

    launch_with_photos = [
        launch
        for launch in launches
        if launch["links"]["flickr"]["original"]
    ]

    max_date = max([launch.get('date_unix') for launch in launch_with_photos])

    if not latest:
        return random.choice(launch_with_photos)["links"]["flickr"]["original"]

    latest_launch = [
        launch
        for launch in launch_with_photos
        if launch.get('date_unix') == max_date
    ][0]

    return latest_launch["links"]["flickr"]["original"]


def fetch_spacex_last_launch(urls, images_dir):
    for url in urls:
        url_path = unquote(urlsplit(url).path)
        filename = pathlib.PurePath(url_path).name
        file_path = pathlib.PurePath(images_dir).joinpath(filename)

        response = requests.get(url)
        response.raise_for_status()

        with open(file_path, 'wb') as file:
            file.write(response.content)


def main():
    images_path = pathlib.Path.cwd() / 'images'

    pathlib.Path.mkdir(images_path, exist_ok=True)

    spacex_photos = get_spacex_photos()
    fetch_spacex_last_launch(spacex_photos, images_path)


if __name__ == '__main__':
    main()
