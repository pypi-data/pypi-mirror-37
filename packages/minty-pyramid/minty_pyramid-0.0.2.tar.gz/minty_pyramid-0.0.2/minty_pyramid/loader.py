# import minty_service
from pyramid.config import Configurator

from minty_pyramid.request import MintyRequest
from minty_pyramid.services import MintyAppService


class Engine:
    config = None

    def setup(self, global_config: dict, **settings) -> object:
        """Setup the application by loading the Configurator

        :param global_config: Global configuration
        :type global_config: dict
        :return: Returns the Configurator from Pyramid
        :rtype: object
        """

        config = Configurator(settings=settings, request_factory=MintyRequest)
        minty_service = MintyAppService()
        minty_service.load_services(config)

        config.scan()
        self.config = config
        return config

    def main(self) -> object:
        """Run the application by calling the wsgi_app function of Pyramid

        :raises ValueError: When setup is forgotten
        :return: wsgi app
        :rtype: object
        """

        if not self.config:
            raise ValueError("Make sure you run setup before 'main'")

        return self.config.make_wsgi_app()
