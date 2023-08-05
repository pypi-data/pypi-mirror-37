from minty_ddd import CommandAndQuery
from pyramid.request import Request


class CommandAndQueryRequest:
    def __init__(self, req):
        self._request = req

    def command(self, **kwargs):
        # Do something with logged in user
        # TODO:
        # * Load infrastructure factory
        # * Load event_system
        cqs = CommandAndQuery()  # infrastructure_factory=req.)

        # Do something with hostname
        # if "params" not in kwargs.keys():
        #     kwargs["params"] = {}

        # kwargs["params"]["auth"] = {"type": "subject", "id": 1}
        # kwargs["params"]["instance_hostname"] = self.host

        return cqs.command(**kwargs)

    def query(self, **kwargs):
        # Do something with logged in user
        # TODO:
        # * Load infrastructure factory
        # * Load event_system
        cqs = CommandAndQuery()

        # Do something with hostname
        # if "params" not in kwargs.keys():
        #     kwargs["params"] = {}

        # kwargs["params"]["auth"] = {"type": "subject", "id": 1}
        # kwargs["params"]["instance_hostname"] = self.host

        return cqs.query(**kwargs)


# Extends the request object of pyramid, to supply instance configuration, etc
class MintyRequest(Request):
    cqs = None

    def __init__(self, *args, **kwargs):
        super(MintyRequest, self).__init__(*args, **kwargs)

        self.cqs = CommandAndQueryRequest(self)
