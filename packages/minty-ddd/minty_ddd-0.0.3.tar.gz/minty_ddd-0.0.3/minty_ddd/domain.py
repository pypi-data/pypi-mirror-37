from abc import ABC, abstractmethod

from minty_ddd.ddd import DDDConfiguration


def register_commands(domain, classname):
    """[summary]

    :param domain: [description]
    :type domain: [type]
    :param classname: [description]
    :type classname: [type]
    :return: [description]
    :rtype: [type]
    """

    return DDDConfiguration().register_commands(domain, classname)


def register_queries(domain, classname):
    return DDDConfiguration().register_queries(domain, classname)


def register_repository(domain, repository):
    return DDDConfiguration().register_repository(domain, repository)


class Entity:
    def __init__(self, **kwargs):
        self._repository = kwargs["repository"]
        super().__init__()


class Repository(ABC):
    aggregate = object

    def __init__(self, infrastructure_factory=None):
        self.infrastructure_factory = infrastructure_factory
        super()

    def create(self):
        return self.aggregate(repository=self)

    @abstractmethod
    def save(self, entity_or_aggregate):
        pass


class Event:
    def __init__(self, params):
        self.params = params


class AggregateEvents(object):
    def _commit_pending_events(self):
        committed_events = []
        for event in self._events_pending:
            ### Will commit pending events to the object, and returns
            ### the successfull events
            event.commit(self, **event.params)
            committed_events.append(event)
            self._events_history.append(event)

        self._events_pending = []

        return committed_events

    def _event(self, event, **kwargs):
        e = event(params=kwargs)
        self._events_pending.append(e)

    def __init__(self, **kwargs):
        self._events_pending = []
        self._events_history = []
        super().__init__(**kwargs)


class AggregateRoot(AggregateEvents, Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
