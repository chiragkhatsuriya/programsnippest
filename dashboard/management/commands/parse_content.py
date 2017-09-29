import os
import random
import string
import traceback
import urllib2

import StringIO

import re
from bs4 import BeautifulSoup
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.management import BaseCommand
from os.path import isfile, join

from django.template.defaultfilters import slugify

from dashboard.models import Page


class Command(BaseCommand):


     def handle(self, *args, **options):
        path_not_done="/home/abhay/dev/files/not_done/"
        path_done="/home/abhay/dev/files/done/"
        onlyfiles = [f for f in os.listdir(path_not_done) if isfile(join(path_not_done, f))]
        for file in onlyfiles:
            text = open(path_not_done+file, 'rb').read()
            soup = BeautifulSoup(text, "html.parser")
            title = file[:-5]
            title = title.replace("-", " ")
            html = ""
            try:
                for node in soup.find_all(class_=re.compile("mixitup")):
                   html += str(node)
                page = Page()
                page.title = title
                page.description = html
                page.meta_description = title
                page.meta_keywords = title
                page.slug = slugify(title)
                page.save()
                os.rename(path_not_done + file, path_done + file)
            except:
                tb = traceback.format_exc()
                print title+" not done"
                print tb






