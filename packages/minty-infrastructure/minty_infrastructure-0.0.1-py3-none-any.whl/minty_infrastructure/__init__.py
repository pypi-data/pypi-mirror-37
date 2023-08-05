__version__ = "0.0.1"

from minty_config import Configuration
from minty_config.parser import ApacheConfigParser
from minty_config.store import FileStore, RedisStore

CONFIG_STORE_MAP = {"file": FileStore, "redis": RedisStore}

__all__ = ["InfrastructureFactory"]


def _parse_global_config(filename):
    config_parser = ApacheConfigParser()

    with open(filename, "r", encoding="utf-8") as config_file:
        content = config_file.read()

    return config_parser.parse(content)


class InfrastructureFactory:
    """Infrastructure factory class

    The infrastructure factory will create instances of registered
    "infrastructure" classes, with configuration for a specific hostname.
    """

    slots = ["global_config", "instance_config", "registered_infrastructure"]

    def __init__(self, config_file: str):
        """Initialize an application service factory

        :param config_file: Global configuration file to read
        :type config_file: str
        :param hostname: Hostname to retrieve host-specific configuration for
        :type hostname: str
        """

        self.global_config = _parse_global_config(filename=config_file)

        config_store_type = self.global_config["InstanceConfig"]["type"]
        config_store_args = self.global_config["InstanceConfig"]["arguments"]

        config_store = CONFIG_STORE_MAP[config_store_type](**config_store_args)

        self.instance_config = Configuration(
            parser=ApacheConfigParser(), store=config_store
        )

        self.registered_infrastructure = {}

    def register_infrastructure(self, name: str, cls: type):
        """Register an infrastructure class with the factory

        :param name: Name to register the infrastructure class under
        :type name: str
        :param cls: Class to register in the infrastructure factory
        :type cls: class
        """

        self.registered_infrastructure[name] = cls

    def get_infrastructure(self, hostname: str, infrastructure_name: str):
        """Retrieve an infrastructure instance for the selected instance

        :param infrastructure_name: Name of the infrastructure class to
                                    instantiate
        :type infrastructure_name: str
        :return: [description]
        :rtype: object
        """
        return self.registered_infrastructure[infrastructure_name](
            config={**self.global_config, **self.instance_config.get(hostname)}
        )
