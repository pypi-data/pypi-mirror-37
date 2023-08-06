from minty_infrastructure import InfrastructureFactory


class RepositoryFactory:
    """Create context-specific "repository" instances for domains
    """

    __slots__ = ["infrastructure_factory", "repositories"]

    def __init__(self, infra_factory: InfrastructureFactory):
        """Initialize the repository factory with an infrastructure factory

        :param infra_factory: Infrastructure factory
        :type infra_factory: InfrastructureFactory
        """
        self.infrastructure_factory = infra_factory
        self.repositories = {}

    def register_repository(self, repository):
        """Register a repository class with the repository factory

        :param repository: repository class; will be instantiated when the
            domain code asks for it by __name__.
        :type repository: object
        """
        self.repositories[repository.__name__] = repository

    def get_repository(self, repository: str, context=None):
        """Retrieve a repository, given a name and optionally a context

        :param repository: repository to instantiate, by __name__
        :type repository: str
        :param context: Context for which to retrieve the repository.
        :type context: object, optional
        :return: An instance of the configured repository, for the specified
            context.
        :rtype: object
        """
        repo = self.repositories[repository]
        return repo(context, self.infrastructure_factory)


class CQRS:
    """Keep commands and queries separated

    CQRS: Command Query Responsibility Separation
    """

    __slots__ = ["domains"]

    def __init__(self, domains, infrastructure_factory: InfrastructureFactory):
        """Create a new CQRS instance from a list of domains

        :param domains: iterable returning domains. Domains are classes or
            packages with at least a "REQUIRED_REPOSITORIES" variable defining
            which repositories are necessary to use the domain.
        :type domains: object
        :param infrastructure_factory: Infrastructure factory, created with
            the required configuration, that the repositories can use to
            create infrastructure instances.
        :type infrastructure_factory: InfrastructureFactory
        """
        self.domains = {}

        for domain in domains:
            repo_factory = RepositoryFactory(infrastructure_factory)

            for repo in domain.REQUIRED_REPOSITORIES:
                repo_factory.register_repository(repo)

                for infra in repo.REQUIRED_INFRASTRUCTURE:
                    infrastructure_factory.register_infrastructure(infra)

            self.domains[domain.__name__] = {
                "module": domain,
                "repository_factory": repo_factory,
            }

    def get_query_instance(self, domain: str, context=None):
        """Instantiate and return the "query" part of the specified domain

        :param domain: name of the domain to get the query instance for
        :type domain: str
        :param context: context for this domain, defaults to None
        :param context: object, optional
        """
        # This can be probably be cached (per context = host)
        return self.domains[domain]["module"].get_query_instance(
            self.domains[domain]["repository_factory"], context=context
        )

    # command is unimplemented for now: build when needed
