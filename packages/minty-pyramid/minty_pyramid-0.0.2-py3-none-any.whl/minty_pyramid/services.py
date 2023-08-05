from minty_ddd import DDDConfiguration
from minty_infrastructure import InfrastructureFactory

from minty_pyramid.util import INIParser

# from minty_config import Configuration as MintyConfiguration
# from minty_config.parser import ApacheConfigParser
# from minty_config.store import FileStore


class MintyDDDNoConfiguration(Exception):
    pass


class MintyConfigNoApplicationConfigSetup(Exception):
    pass


class MintyConfigNoRequestConfigSetup(Exception):
    pass


class MintyAppServiceDDD:
    def load(self, config: object) -> bool:
        """Load and configures the Command and Query service for Pyramid

        :param config: Pyramid Configurator object
        :type config: object
        :raises ValueError: When 'minty_service.ddd.domains' is missing
        :raises ValueError: When 'minty_service.ddd.domainprefix' is missing
        :return: True on success
        :rtype: bool
        """

        # Add a directive to Configuratorobject with our DDD Configuration
        config.add_directive(
            "get_ddd_configuration", self._directive_get_ddd_configuration
        )

        settings = config.get_settings()

        if "minty_service.ddd.domains" not in settings:
            raise MintyDDDNoConfiguration(
                "Required configuration 'minty_service.ddd.domains'"
                + " is missing in ini file"
            )

        if "minty_service.ddd.domainprefix" not in settings:
            raise MintyDDDNoConfiguration(
                "Required configuration 'minty_service.ddd.domainprefix'"
                + " is missing in ini file"
            )

        # Get domains from ini file
        domains = INIParser().parse_array(
            settings["minty_service.ddd.domains"]
        )
        domainprefix = settings["minty_service.ddd.domainprefix"]

        # Load configuration in Configurator
        ddd_config = DDDConfiguration()
        ddd_config.domainprefix = domainprefix

        for domain in domains:
            ddd_config.add_domain(domain=domain)

        config.__ddd_configuration = ddd_config

    @staticmethod
    def _directive_get_ddd_configuration(config):
        return config.__ddd_configuration


class MintyAppInfrastructureConfig:
    def load(self, config):
        """Load configuration in pyramid.

        :param config: Configuration object
        :type config: object
        """
        settings = config.get_settings()
        self.load_infrastructure_factory(config, settings)

    def load_infrastructure_factory(self, config, settings):
        if "minty_service.infrastructure.config_file" not in settings:
            raise MintyConfigNoApplicationConfigSetup(
                "Could not load application config, setting '%s' not found"
                % ("minty_service.infrastructure.config_file")
            )

        infra_config = INIParser().parse_from_prefix(
            settings, "minty_service.infrastructure"
        )

        config.__infrastructure_factory = InfrastructureFactory(
            config_file=infra_config["config_file"]
        )

        config.add_directive(
            "get_infrastructure_configuration",
            self._directive_get_infrastructure_config,
        )

        return True

    @staticmethod
    def _directive_get_infrastructure_config(config):
        return config.__infrastructure_factory


class MintyAppService:
    """Application Service for loading extra Minty services into Pyramid."""

    _services = []
    _service_map = {
        "ddd": MintyAppServiceDDD,
        "infrastructure": MintyAppInfrastructureConfig,
    }

    def load_services(self, config: object) -> bool:
        """Load services from ini directive 'minty_service.enable'.

        :param config: Pyramid Configurator object
        :type config: object
        :return: True on success
        :rtype: bool
        """

        settings = config.get_settings()
        if "minty_service.enable" not in settings.keys():
            return False

        # Make sure we skip empty services
        services = INIParser().parse_array(settings["minty_service.enable"])

        # In the future, we could use importlib here. Keep it simple for now
        self._services = services
        for service in services:
            service_class = self._service_map[service]()
            service_class.load(config)

        return True
