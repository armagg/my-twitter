# from django.core.files import File
from django.core.files.storage import default_storage
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render
from os.path import isfile, join
from mimetypes import MimeTypes
from os import listdir

from django.views.decorators.csrf import csrf_exempt
from wand.image import Image
import wand.image
import hashlib
import json
import time
import hmac
import copy
import sys
import os


@csrf_exempt
def index(request):
    return render(request, 'froala/froala.html')


@csrf_exempt
def file_upload(request):
    if 'file' in request.FILES:
        the_file = request.FILES['file']
        upload_to = getattr(settings, 'FROALA_UPLOAD_PATH', 'uploads/froala_editor/files/')
        path = default_storage.save(os.path.join(upload_to, the_file.name), the_file)
        link = 'http://localhost:8000' + default_storage.url(path)
        return HttpResponse(json.dumps({'link': link}), content_type="application/json")


@csrf_exempt
def upload_image_validation(request):
    print('validation')

    def validation(filePath, mimetype):
        with wand.image.Image(filename=filePath) as img:
            if img.width != img.height:
                return False
            return True

    options = {
        "fieldname": "myImage",
        "validation": validation
    }

    try:
        response = Image.upload(DjangoAdapter(request), "/public/", options)
    except Exception:
        response = {"error": str(sys.exc_info()[1])}
    return HttpResponse(json.dumps(response), content_type="application/json")


class Image(object):
    defaultUploadOptions = {
        "fieldname": "file",
        "validation": {
            "allowedExts": ["gif", "jpeg", "jpg", "png", "svg", "blob"],
            "allowedMimeTypes": ["image/gif", "image/jpeg", "image/pjpeg", "image/x-png", "image/png",
                                 "image/svg+xml"]
        },
        # string resize param from http://docs.wand-py.org/en/0.4.3/guide/resizecrop.html#transform-images
        # Examples: "100x100", "100x100!". Find more on http://www.imagemagick.org/script/command-line-processing.php#geometry
        "resize": None
    }

    @staticmethod
    def upload(req, fileRoute, options=None):
        """
        Image upload to disk.
        Parameters:
            req: framework adapter to http request. See BaseAdapter.
            fileRoute: string
            options: dict optional, see defaultUploadOptions attribute
        Return:
            dict: {link: "linkPath"}
        """

        if options is None:
            options = Image.defaultUploadOptions
        else:
            options = Utils.merge_dicts(Image.defaultUploadOptions, options)

        return File.upload(req, fileRoute, options)

    @staticmethod
    def delete(src):
        """
        Delete image from disk.
        Parameters:
            src: string
        """
        return File.delete(src)

    @staticmethod
    def list(folderPath, thumbPath=None):
        """
        List images from disk.
        Parameters:
            folderPath: string
            thumbPath: string
        Return:
            list: list of images dicts. example: [{url: "url", thumb: "thumb", name: "name"}, ...]
        """

        if thumbPath == None:
            thumbPath = folderPath

        # Array of image objects to return.
        response = []

        absoluteFolderPath = Utils.getServerPath() + folderPath

        # Image types.
        imageTypes = Image.defaultUploadOptions["validation"]["allowedMimeTypes"]

        # Filenames in the uploads folder.
        fnames = [f for f in listdir(absoluteFolderPath) if isfile(join(absoluteFolderPath, f))]

        for fname in fnames:
            mime = MimeTypes()
            mimeType = mime.guess_type(absoluteFolderPath + fname)[0]

            if mimeType in imageTypes:
                response.append({
                    "url": folderPath + fname,
                    "thumb": thumbPath + fname,
                    "name": fname
                })

        return response


class Utils(object):
    """
    Utils static class.
    """

    @staticmethod
    def hmac(key, string, hex=False):
        """
        Calculate hmac.
        Parameters:
            key: string
            string: string
            hex: boolean optional, return in hex, else return in binary
        Return:
            string: hmax in hex or binary
        """

        # python 2-3 compatible:
        try:
            hmac256 = hmac.new(key.encode() if isinstance(key, str) else key,
                               msg=string.encode("utf-8") if isinstance(string, str) else string,
                               digestmod=hashlib.sha256)  # v3
        except Exception:
            hmac256 = hmac.new(key, msg=string, digestmod=hashlib.sha256)  # v2

        return hmac256.hexdigest() if hex else hmac256.digest()

    @staticmethod
    def merge_dicts(a, b, path=None):
        """
        Deep merge two dicts without modifying them. Source: http://stackoverflow.com/questions/7204805/dictionaries-of-dictionaries-merge/7205107#7205107
        Parameters:
            a: dict
            b: dict
            path: list
        Return:
            dict: Deep merged dict.
        """

        aClone = copy.deepcopy(a);
        # Returns deep b into a without affecting the sources.
        if path is None: path = []
        for key in b:
            if key in a:
                if isinstance(a[key], dict) and isinstance(b[key], dict):
                    aClone[key] = Utils.merge_dicts(a[key], b[key], path + [str(key)])
                else:
                    aClone[key] = b[key]
            else:
                aClone[key] = b[key]
        return aClone

    @staticmethod
    def getExtension(filename):
        """
        Get filename extension.
        Parameters:
            filename: string
        Return:
            string: The extension without the dot.
        """
        return os.path.splitext(filename)[1][1:]

    @staticmethod
    def getServerPath():
        """
        Get the path where the server has started.
        Return:
            string: serverPath
        """
        return os.path.abspath(os.path.dirname(sys.argv[0]))

    @staticmethod
    def isFileValid(filename, mimetype, allowedExts, allowedMimeTypes):
        """
        Test if a file is valid based on its extension and mime type.
        Parameters:
            filename string
            mimeType string
            allowedExts list
            allowedMimeTypes list
        Return:
            boolean
        """

        # Skip if the allowed extensions or mime types are missing.
        if not allowedExts or not allowedMimeTypes:
            return False

        extension = Utils.getExtension(filename)
        return extension.lower() in allowedExts and mimetype in allowedMimeTypes

    @staticmethod
    def isValid(validation, filePath, mimetype):
        """
        Generic file validation.
        Parameters:
            validation: dict or function
            filePath: string
            mimetype: string
        """

        # No validation means you dont want to validate, so return affirmative.
        if not validation:
            return True

        # Validation is a function provided by the user.
        if callable(validation):
            return validation(filePath, mimetype)

        if isinstance(validation, dict):
            return Utils.isFileValid(filePath, mimetype, validation["allowedExts"], validation["allowedMimeTypes"])

        # Else: no specific validating behaviour found.
        return False


class BaseAdapter(object):
    """
    Interface. Inherit this class to use the lib in your framework.
    """

    def __init__(self, request):
        """
        Constructor.
        Parameters:
            request: http request object from some framework.
        """
        self.request = request

    def riseError(self):
        """
        Use this when you want to make an abstract method.
        """
        raise NotImplementedError("Should have implemented this method.")

    def getFilename(self, fieldname):
        """
        Get upload filename based on the fieldname.
        Parameters:
            fieldname: string
        Return:
            string: filename
        """
        self.riseError()

    def getMimetype(self, fieldname):
        """
        Get upload file mime type based on the fieldname.
        Parameters:
            fieldname: string
        Return:
            string: mimetype
        """
        self.riseError()

    def saveFile(self, fieldname, fullNamePath):
        """
        Save the upload file based on the fieldname on the fullNamePath location.
        Parameters:
            fieldname: string
            fullNamePath: string
        """
        self.riseError()


class DjangoAdapter(BaseAdapter):
    """
    Django Adapter: Check BaseAdapter to see what methods description.
    """

    def checkFile(self, fieldname):
        if fieldname not in self.request.FILES:
            raise Exception("File does not exist.")

    def getFilename(self, fieldname):
        self.checkFile(fieldname)
        return self.request.FILES[fieldname].name

    def getMimetype(self, fieldname):
        self.checkFile(fieldname)
        return self.request.FILES[fieldname].content_type

    def saveFile(self, fieldname, fullNamePath):
        print("should save now")
        print("the path" + fullNamePath)
        self.checkFile(fieldname)

        with open(fullNamePath, "wb+") as destination:
            for chunk in self.request.FILES[fieldname].chunks():
                destination.write(chunk)
