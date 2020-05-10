import requests as re
from PIL import Image
import io
from datetime import datetime
import asyncio
import aiohttp
import aiofiles
import time


def get_image_list(url):
    """Return list of images"""
    response = re.get(url)
    return str.split(response.content.decode('UTF-8'), '\n')


def get_image(url, filename):
    """Download image by url and filename"""
    response = re.get(url)
    f = open('images/' + filename, 'wb')
    f.write(response.content)
    f.close()


def get_images(url):
    """Download images by url"""
    for l in get_image_list(url):
        get_image(url + l, l)


def get_mirror(filename):
    """save mirror image about a vertical axis"""
    im = Image.open('images/' + filename)
    im = im.transpose(Image.FLIP_LEFT_RIGHT)
    return im
    # im.save('mirror/' + filename)


def get_mirrors(url):
    """save mirror images"""
    for l in get_image_list(url):
        get_mirror(l)


def post_mirors(url):
    for l in get_image_list(url):
        mirror = get_mirror(l)
        imgByteArr = io.BytesIO()
        mirror.save(imgByteArr, format='jpeg')
        imgByteArr = imgByteArr.getvalue()
        response = re.post(url, files={l: imgByteArr})
        print(response)

async def download_image(session, url, image):
    async with session.get(url + image) as response:
        f = await aiofiles.open('images/' + image, 'wb')
        await f.write(await response.read())
        await f.close()
        print("Read {0} from {1}".format(response.content_length, url))


async def download_all_images(image_list, url):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for image in image_list:
            task = asyncio.ensure_future(download_image(session, url, image))
            tasks.append(task)
        await asyncio.gather(*tasks, return_exceptions=True)

if __name__ == '__main__':
    # start_time = datetime.now()
    # post_mirors('http://142.93.138.114/images/')
    # print(datetime.now() - start_time)
    start_time = datetime.now()
    image_list = get_image_list('http://142.93.138.114/images/')
    asyncio.get_event_loop().run_until_complete(download_all_images(image_list, 'http://142.93.138.114/images/'))
    print(datetime.now() - start_time)
    # print(get_image_list('http://142.93.138.114/images/'))
    # get_images('http://142.93.138.114/images/')
    # get_mirrors('http://142.93.138.114/images/')
