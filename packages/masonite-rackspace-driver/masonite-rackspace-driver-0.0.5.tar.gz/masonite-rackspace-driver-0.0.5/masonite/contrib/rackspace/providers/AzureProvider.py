""" An Rackspace Service Provider """

from config import storage

from masonite.provider import ServiceProvider

from ..drivers import UploadRackspaceDriver


class RackspaceProvider(ServiceProvider):

    wsgi = False

    def register(self):
        self.app.bind('UploadRackspaceDriver', UploadRackspaceDriver)

    def boot(self):
        pass
