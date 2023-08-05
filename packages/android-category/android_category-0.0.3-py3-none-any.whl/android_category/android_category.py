"""Module with main logic to retrieve an apps category."""

import logging
import os
import xml.etree.ElementTree as ET
import requests
import tempfile

import click
from google_play_reader.models import AppEntry
from git import Repo

from android_category.cache import Cache

MANIFEST_FILENAME = 'AndroidManifest.xml'
APP_CATEGORY_CACHE = Cache('app_category_cache.json')

def get_app_category_from_repo_git(repo_url):
    """Collect app category given its git url."""
    category = APP_CATEGORY_CACHE.get_value(repo_url)
    if category:
        return category
    with tempfile.TemporaryDirectory() as tmpdirname:
        Repo.clone_from(repo_url, tmpdirname)
        category = get_app_category_from_local(tmpdirname)
    APP_CATEGORY_CACHE.set_value(repo_url, category)
    return category

def get_app_category_from_local(repo_path):
    """Collect category from a local app source code."""
    package = _get_package_of_local_app(repo_path)
    return get_category(package)

def _get_package_of_local_app(repo_path):
    for root, _, files in os.walk(repo_path):
        if MANIFEST_FILENAME in files:
            manifest_path = os.path.join(root, MANIFEST_FILENAME)
            return _extract_package_from_manifest(manifest_path)
    logging.info(f'No manifest was found in f{repo_path}.')
    return None

def _extract_package_from_manifest(manifest_path):
    manifest_node = ET.parse(manifest_path).getroot()
    return manifest_node.get('package')

def get_category(package):
    """Retrieve category of a given Android app."""
    category = APP_CATEGORY_CACHE.get_value(package)
    if category:
        return category
    category = _get_category_from_gplay(package) or _get_category_from_fdroid(package)
    APP_CATEGORY_CACHE.set_value(package, category)
    return category

def _get_category_from_gplay(package):
    app_entry = AppEntry(package)
    return app_entry.get_category()

def _get_category_from_fdroid(package):
    file_in = "./fdroid.xml"
    if not os.path.isfile(file_in):
        url = "https://f-droid.org/repo/index.xml"
        response = requests.get(url, stream=True)
        with open(file_in, "wb") as handle:
            with click.progressbar(
                response.iter_content(),
                label='Downloading F-Droid metadata'
            ) as bar:
                for data in bar:
                    handle.write(data)
    for _, element in ET.iterparse(file_in):
        if element.tag == "application":
            for source_node in element.iter('source'):
                app_id = element.find("id").text
                if app_id == package:
                    return element.find("category").text
    
    