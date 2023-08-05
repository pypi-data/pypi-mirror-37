#!/usr/bin/python3
"""ScanFetcher

Usage:
    fetcher.py --mangas <mangas_name> --out-dir <out_dir> --chap <chapter> --chapter-range <chap_start> <chap_end>
    fetcher.py --mangas <mangas_name> --chap <chapter>
    fetcher.py --mangas <mangas_name> --chapter-range <chap_start> <chap_end>
    fetcher.py (-h | --help)

Options:
    -h --help   Show this help

"""

import requests
import os
from urllib.parse import urljoin
from docopt import docopt
import re
from hashlib import sha256

# BASE_URL = "https://scantrad.fr/mangas/"
BASE_URL = "https://www.japscan.cc/lecture-en-ligne/"
URL_MIDDLE = ""
URL_SUFFIX = ".html"
CORRECT_EXT = ["png", "jpg", "jpeg"]
HASH_LIST = []


def get_slug(name):
    name = name.replace(" ", "-")

    return name


def download_and_save(link, location, page, hash_list):
    req_hash = None
    try:
        print("Downloading " + str(page))
        response = requests.get(link)
        print("Complete " + str(page))

        mime_type = response.headers["content-type"]
        mime_type_parts = mime_type.split("/")

        file_ext = mime_type_parts[1]

        if file_ext not in CORRECT_EXT:
            print("incorrect file ex found :" + file_ext)

        else:
            # before saving th image, check if their is a file with the same content (md5)

            req_hash = create_hash_content(response.content)

            if req_hash in hash_list:
                print("File already Downloaded maybe on another name")
                req_hash = None
                return

            # save the image
            with open("{location}/{name}.{ext}".format(location=location, name=page, ext=file_ext),
                      "wb") as output_page:

                output_page.write(response.content)
            print("Download successful the page " + str(page))

            # return the req hash to be saved in the hash_list
            return req_hash

    except IndexError as error:
        print("index error" + error.__str__())
    except ConnectionError:
        print("Something went wrong with your internet connection. Retrying ...")
    except Exception as error:
        print("An Error occur : " + error.__str__())
    finally:
        return req_hash


def find_image_link(response):

    img_tags_re = re.compile('<img\s+[^>]*src="([^"]*[0-9]+\.(?:jpg|png|jpeg))"[^>]*>')
    img_tags = img_tags_re.search(response)

    try:
        return img_tags.group(1)

    except IndexError as err:
        print(err)
        return None


def page_exist(dir_name, page):
    for ext in CORRECT_EXT:
        file = "{location}/{name}.{ext}".format(location=dir_name, name=page, ext=ext)
        if os.path.exists(file):
            return True
    return False


def create_hash(file):
    """hash a file with the sha256 algo"""
    hasher = sha256()
    try:
        with open(file, "rb") as f:
            hasher.update(f.read())
            return hasher.hexdigest()

    except Exception:
        return None


def create_hash_content(content):
    """hash a file with the sha256 algo"""
    hasher = sha256()
    try:
        hasher.update(content)
        return hasher.hexdigest()

    except Exception:
        return None


def create_hash_list(target_dir):
    """Hash list of the files
    :param target_dir:
    :return: []

    calculate the digest of all the file which exist in the chap directory
    so before saving a file, check if it's hash already exist
    """
    hash_list = []  # store the hash in this array

    if os.path.exists(target_dir):
        files = os.scandir(target_dir)

        for file in files:
            if file.is_dir():  # ignore the directories
                continue
            digest = create_hash(file.path)  # create the hash of the current file
            if digest is not None:  # if the digest is None
                hash_list.append(digest)  # append the hash to the hash_list

    return hash_list


def download_chapter(mangas_chapter, mangas_url, out_dir):

    # create a dir of the name of the chapter
    dir_name = "{}/chapter_{}".format(out_dir, mangas_chapter)

    scan_urls = []  # will keep the scans url of the current chapter
    hash_list = create_hash_list(dir_name)

    if not os.path.exists(dir_name):
        os.mkdir(dir_name)

    # get the chapter url
    mangas_chapter_url = "{}/{}".format(mangas_url, mangas_chapter)

    page = 0

    while True:

        page = page + 1
        # page_url = urljoin(mangas_chapter_url, page)
        # page_url = "{mangas_chapter_url}?page={page}".format(mangas_chapter_url=mangas_chapter_url, page=page)
        page_url = "{mangas_chapter_url}/{page}{suffix}".format(mangas_chapter_url=mangas_chapter_url, page=page,
                                                                suffix=URL_SUFFIX)
        if page_exist(dir_name, page):
            """ If the file for the scan exist """
            print("The Scan which is at page " + str(page) + " already exist. Skipping ...")
            continue

        # crawl the web page
        try:
            response = requests.get(page_url)
        except ConnectionError as err:
            print(err)
            break
        except Exception as err:
            print(err)
            break

        if response.status_code == 404:
            break

        # find the image link
        image_link = find_image_link(response.content.__str__())
        scan_urls.append(image_link)

        last_hash = download_and_save(image_link, dir_name, page, hash_list)

        if last_hash is not None:
            hash_list.append(last_hash)
        else:
            break


def main(args):

    # get the arguments
    out_dir = args["<out_dir>"]
    mangas_chapter = args["<chapter>"]
    mangas_name = args["<mangas_name>"]
    chapter_range = [args["<chap_start>"], args["<chap_start>"]]

    # get the slug of the mangas
    mangas_name_slug = get_slug(mangas_name)

    if out_dir is not None and not os.path.exists(out_dir):
        os.mkdir(out_dir)

    else:
        if not os.path.exists(mangas_name_slug):
            os.mkdir(mangas_name_slug)
        out_dir = mangas_name_slug

    mangas_url = urljoin(BASE_URL, mangas_name_slug)  # get the mangas url

    if mangas_chapter is not None:  # if the mangas chapter is define
        download_chapter(mangas_chapter, mangas_url, out_dir)

    elif chapter_range is not None:  # if a range of chapter is define
        for mangas_chapter in range(1, 104):
            # Download the scans for this chapter
            download_chapter(mangas_chapter, mangas_url, out_dir)
