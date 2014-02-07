
from gtrac.triggers import Trigger

class GtracConf(object):
    def __init__(self, env):
        self.env = env
        self.triggers = {}
        self.parse_triggers()
    
    def format_metric_key(self, conf_key):
        splitted = conf_key.split('.')
        if len(splitted) >= 2:
            metric_name = splitted[1]
            options = '.'.join(splitted[2:])
            if not options == '':
                return "%s.%s" % (metric_name, options)
            else:
                return metric_name
    
    def parse_trigger_values(self, strval):
        values = strval.split(',')
        return [Trigger(*value.split(':')) for value in values]
    
    def parse_triggers(self):
        if not 'gtrac' in self.env.config.sections():
            return
        
        for key, value in self.env.config.options('gtrac'):
            if key.startswith('triggers'):
                metric = self.format_metric_key(key)
                triggers = self.parse_trigger_values(value)
                self.triggers[metric] = triggers
    
    def get_triggers(self, metric):
        host = metric.host
        cluster = host.cluster
        grid = cluster.grid
        
        pattern = metric.name
        pattern += '.' + str(grid)
        pattern += '.' + str(cluster)
        pattern += '.' + str(host)
        
        valids = {}
        for key in self.triggers.keys():
            if pattern.startswith(key):
                valids[key] = self.triggers[key]
        
        if len(valids) > 0:
            key = sorted(valids, reverse=True)[0]
            return self.triggers[key]
    
    def get_hostname(self, default=None):
        hostname = self.env.config.get('gtrac', 'host')
        if len(hostname) > 0:
            return hostname
        else:
            return default
    
    def get_port(self, default=8651):
        port = self.env.config.getint('gtrac', 'port')
        if port > 0:
            return port
        else:
            return default
