# -*- coding: utf-8 -*-
import os
from pixivpy3 import *

class Pixiv(object):
    api = AppPixivAPI()

    def login(self, user, pwd):
        self.api.login(user, pwd)

    def getFilename(self,url, illust):
        basename = os.path.basename(url)
        filename = os.path.splitext(basename)[0]
        extension = os.path.splitext(basename)[1]
        name = "%s - %s - %s(%d)%s" % (filename, illust.title, illust.user.name, illust.user.id, extension)
        return name

    def artworkDetail(self, id):
        try:
            illust = self.api.illust_detail(id).illust
        except AttributeError:
            raise PixivError("Artwork not found")
        imgs = list()
        if illust.meta_pages: # Contains more than one image
            pages = illust.meta_pages
            for page in pages:
                url = page.image_urls.original
                name = self.getFilename(url, illust)
                imgs.append({'url': url, 'name': name})
        else:
            url = illust.meta_single_page.original_image_url
            name = self.getFilename(url, illust)
            imgs.append({'url': url, 'name': name})
        return imgs

    def downloadArtwork(self, id=None, imgs=None):
        directory = './downloads/'
        if not imgs:
            imgs = self.artworkDetail(id)
        if not os.path.exists(directory):
            os.makedirs(directory)
        for img in imgs:
            self.api.download(img['url'], path=directory, name=img['name'])
        return imgs
