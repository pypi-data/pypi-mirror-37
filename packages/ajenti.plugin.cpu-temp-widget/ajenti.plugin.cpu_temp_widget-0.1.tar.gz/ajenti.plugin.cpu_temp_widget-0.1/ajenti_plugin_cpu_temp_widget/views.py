import psutil

from jadi import component
from aj.api.http import url, HttpPlugin
from aj.api.endpoint import endpoint, EndpointError, EndpointReturn


@component(HttpPlugin)
class Handler(HttpPlugin):
    def __init__(self, context):
        self.context = context

    @url(r'/api/cpu/cores')
    @endpoint(api=True)
    def handle_api_cpu_cores(self, http_context):
        return [x.label for x in psutil.sensors_temperatures().get('coretemp')]
