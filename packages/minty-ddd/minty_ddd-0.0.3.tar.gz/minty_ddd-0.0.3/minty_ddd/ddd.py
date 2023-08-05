"""Command and Query module

Module for managing command and query actions for a given domain.
"""

import importlib
import re

from minty_ddd.util import Singleton


class DomainNotFoundError(Exception):
    pass


class CommandQueryNotFoundError(Exception):
    pass


class InvalidDomainGiven(Exception):
    pass


class NoReturnValueAllowedInCommand(Exception):
    pass


class DDDConfiguration(metaclass=Singleton):
    """Configuration of the command and query system."""

    _domains = {}  # List of loaded domain classes
    _domainprefix = "minty.domain"

    _loaded_components = {}

    ### Attributes

    @property
    def domainprefix(self) -> str:
        """Returns the module prefix to search for a domain

        :return: The prefix of a domain
        :rtype: str
        """

        return self._domainprefix

    @domainprefix.setter
    def domainprefix(self, value: str) -> str:
        """Set a new domain prefix in our config

        :param value: The new domain prefix, e.g.: "mintlab.domain"
        :type value: str
        :return: The setted domain prefix
        :rtype: str
        """

        self._domainprefix = value
        return self._domainprefix

    ### Public methods

    def add_domain(self, domain: str = None) -> bool:
        """Add a new domain to search on, e.g.: "brewing"

        :param domain: Add a new domain, e.g. "brewing"
        :param domain: str
        :raises InvalidDomainGiven: Raises exception when domain does not exist
        :return: True on success, exception on failure
        :rtype: bool
        """

        module = domain
        if type(domain) == str:
            module_name = self._get_module_name_from_domain(domain=domain)

            module = self._import_module(module_name)
        else:
            raise InvalidDomainGiven

        self._domains[domain] = module
        return True

    def get_domain(self, domain: str) -> object:
        """Get a domain to work on, mostly used internally to initiate
        a new command

        :param domain: The domain to retrieve, e.g. "brewing"
        :type domain: str
        :return: Returns an instance of the domain module
        :rtype: object
        """

        return self._domains[domain]

    ### Private methods

    def _get_module_name_from_domain(self, domain="") -> str:
        ### Retrieves the proper module_name for the given domain and name
        module = domain
        if re.search(r"\.", domain):
            raise InvalidDomainGiven
        else:
            module = "%s.%s" % (self.domainprefix, domain)

        return module

    def _import_module(self, module_name: str) -> object:
        ### Imports module from system by given module_name
        module = None
        try:
            module = importlib.import_module(module_name)
        except ModuleNotFoundError as e:
            raise DomainNotFoundError(e)

        return module

    def register_commands(self, domain: str, classname: object) -> bool:
        """Register a command class to a domain

        :param domain: Domain to add these commands to, e.g. "brewing"
        :type domain: str
        :param classname: Class containing the command, e.g. "Commands"
        :type classname: object
        :return: True or error on failure
        :rtype: bool
        """

        if domain not in self._loaded_components:
            self._loaded_components[domain] = {}

        self._loaded_components[domain]["commands"] = classname()
        return True

    def register_queries(self, domain: str, classname: object) -> bool:
        """Register a query class to a domain

        :param domain: Domain to add these commands to, e.g. "brewing"
        :type domain: str
        :param classname: Class containing the queries, e.g. "Queries"
        :type classname: object
        :return: True or error on failure
        :rtype: bool
        """

        if domain not in self._loaded_components:
            self._loaded_components[domain] = {}

        self._loaded_components[domain]["queries"] = classname()

        return True

    def register_repository(self, domain: str, repository: object) -> bool:
        """Register a repository to this domain

        :param domain: Domain to add these commands to, e.g. "brewing"
        :type domain: str
        :param repository: Repository class
        :type repository: object
        :return: True or error on failure
        :rtype: bool
        """

        if domain not in self._loaded_components:
            self._loaded_components[domain] = {}

        if "repositories" not in self._loaded_components[domain]:
            self._loaded_components[domain]["repositories"] = {}

        self._loaded_components[domain]["repositories"][
            repository.__name__
        ] = repository

        return True

    def get_repository_class(self, domain: str, name: str) -> object:
        """Return a non-instantiated repository by name

        :param domain: Domain to retrieve this repository from, e.g. "brewing"
        :type domain: str
        :param name: Name pointing to repository, e.g. "BeerRepository"
        :type name: str
        :return: Repository object
        :rtype: object
        """
        return self._loaded_components[domain]["repositories"][name]


class CommandAndQuery:
    """Executes commands and queries to a given domain."""

    def command(
        self, domain: str, command: str, params: dict = None
    ) -> object:
        """Retrieves a command object from the given domain.

        :param domain: The domain to search in, e.g. "brewing"
        :type domain: str
        :param command: The command to run, e.g. "BrewBeer"
        :type command: str
        :param params: List of parameters to prepare this command for
        :param params: dict, optional
        :return: Returns an instance of the command
        :rtype: object
        """

        command_instance = self._get_classname_from_domain(
            domain=domain, classname=command, type="commands"
        )

        return command_instance(
            params=params,
            infrastructure_factory=self._infrastructure_factory,
            domain=domain,
            event_system=self._event_system,
        )

    def query(self, domain: str, query: str, params: dict = None) -> object:
        """Prepare a query on the given domain.

        :param domain: The domain to search in, e.g. "brewing"
        :type domain: str
        :param query: The query to run, e.g. "ListBeers"
        :type query: str
        :param params: List of parameters to prepare this command for
        :param params: dict, optional
        :return: Returns an instance of the query
        :rtype: object
        """

        query_instance = self._get_classname_from_domain(
            domain=domain, classname=query, type="queries"
        )

        return query_instance(
            params=params,
            infrastructure_factory=self._infrastructure_factory,
            domain=domain,
            event_system=self._event_system,
        )

    def __init__(
        self,
        domain: str = None,
        params: dict = None,
        infrastructure_factory: object = None,
        event_system: object = None,
    ):
        self._dddconfig = DDDConfiguration()
        self._domain = domain
        self._event_system = event_system

        self._execute_params = params
        self._infrastructure_factory = infrastructure_factory

    def _get_classname_from_domain(
        self, domain: str, classname: str, type: str
    ) -> object:
        loaded_class = self._dddconfig._loaded_components[domain][type]
        try:
            cq_class = getattr(loaded_class, classname)
        except AttributeError:
            raise CommandQueryNotFoundError(
                "Command or Query '%s' not found in domain: %s"
                % (classname, domain)
            )

        return cq_class

    @property
    def infrastructure_factory(self) -> object:
        return self._infrastructure_factory

    @infrastructure_factory.setter
    def infrastructure_factory(self, infrastructure_factory: object) -> object:
        self._infrastructure_factory = infrastructure_factory
        return self._infrastructure_factory


class BaseQueryCommand(CommandAndQuery):
    def execute(self, **kwargs):
        """Execute a command in the domain

        :raises Exception: when command returns a value, only void or true
                           allowed
        :return: Result of the command or query
        :rtype: Result of the domain command
        """

        ### Do some magic, like registering this command in a database
        if self._execute_params and isinstance(self._execute_params, dict):
            kwargs = {**kwargs, **self._execute_params}

        result = self.action(**kwargs)

        ### Do something with result, e.g.: always return an object containing
        ### the events to run, and the return value.
        ### TODO Probably move this to DomainCommand
        if hasattr(self, "_is_command"):
            if result and not isinstance(result, (int, float)):
                raise NoReturnValueAllowedInCommand(
                    "Commands should not return anything"
                )

        return result

    def action(self, **kwargs):
        raise NotImplementedError(
            "Method '%s' is not implemented in query or command: %s"
            % ("action", str(type(self)))
        )

    def get_repository(self, name: str) -> object:
        """Return a repository instance by name registered for this domain.

        :param name: Name of the repository, e.g. "BeerRepository"
        :type name: str
        :return: Repository object with infrastructure_factory loaded
        :rtype: object
        """

        Repository = self._dddconfig.get_repository_class(self._domain, name)
        return Repository(infrastructure_factory=self.infrastructure_factory)

    def save(self, aggregate: object) -> bool:
        """Save an aggregate to the system by comitting it to its corresponding
        repository

        :param events: List of Event's
        :type events: list
        :return: True or error on failure
        :rtype: bool
        """
        events = aggregate._commit_pending_events()

        # First ask system to save all changes to the Entity
        for event in events:
            self._event_system.publish(event)

        # Now save the entity to the repository
        aggregate._repository.save(aggregate)

        return True


class BaseCommand(BaseQueryCommand):
    _is_command = 1


class BaseQuery(BaseQueryCommand):
    _is_query = 1
