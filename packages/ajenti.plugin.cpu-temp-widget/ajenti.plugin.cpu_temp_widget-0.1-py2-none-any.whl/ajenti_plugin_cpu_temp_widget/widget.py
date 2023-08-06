import psutil

from jadi import component
from aj.plugins.dashboard.api import Widget


@component(Widget)
class CpuTempWidget(Widget):
    id = 'cpu_temp'

    # display name
    name = 'CPU Temp'

    # template of the widget
    template = '/cpu_temp_widget:resources/partial/widget.html'
    config_template = '/cpu_temp_widget:resources/partial/widget.config.html'

    def __init__(self, context):
        Widget.__init__(self, context)

    def get_value(self, config):
        parts = psutil.sensors_temperatures().get('coretemp')
        usage = dict((x.label, x) for x in parts)

        core = config.get('core', None)
        if core is None:
            return {
                'label':    'CPU Temp',
                'current':  max(x.current for x in usage.values()),
                'high':     max(x.high for x in usage.values()),
                'critical': max(x.critical for x in usage.values()),
            }
        elif core in usage:
            return {
                'label':    usage[core].label,
                'current':  usage[core].current,
                'high':     usage[core].high,
                'critical': usage[core].critical,
            }
        else:
            return {
                'label':    None,
                'current':  None,
                'high':     None,
                'critical': None,
            }