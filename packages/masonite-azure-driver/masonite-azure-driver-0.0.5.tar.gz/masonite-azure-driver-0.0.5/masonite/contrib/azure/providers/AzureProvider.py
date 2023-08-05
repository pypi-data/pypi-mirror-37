""" An Azure Service Provider """

from config import storage

from masonite.provider import ServiceProvider

from ..drivers import UploadAzureDriver


class AzureProvider(ServiceProvider):

    wsgi = False

    def register(self):
        self.app.bind('UploadAzureDriver', UploadAzureDriver)

    def boot(self):
        pass
