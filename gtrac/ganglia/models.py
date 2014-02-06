
class GMetricValue(object):
    TYPES = {
        'string': str,
        'int8' : int,
        'int16' : int,
        'int32' : int,
        'uint8' : int,
        'uint16' : int,
        'uint32' : int,
        'float' : float,
        'double' : float
    }
    
    class TypeException(Exception):
        pass
    
    def __init__(self, value, type, units):
        if not type in self.TYPES:
            raise GMetricValue.TypeException(type)
        self.value = self.TYPES[type.lower()](value)
        self.type = type
        self.units = units
    
    def __str__(self):
        return "%s %s" % (str(self.value), self.units)
    
    def __unicode__(self):
        return "%s %s" % (str(self.value), self.units)


class Metric(object):
    def __init__(self, name, value, type, units,
                 tn, tmax, dmax, slope, source,
                 extras={}):
        self.name = name
        self.value = GMetricValue(value, type, units)
        self.tn = tn
        self.tmax = tmax
        self.dmax = dmax
        self.slope = slope
        self.source = source
        
        self.extras = {}
    
    def __unicode__(self):
        return self.name
    
    def __str__(self):
        return self.name


class Host(object):
    
    def __init__(self, name, ip, reported, tn, tmax, dmax, gmond_started,
                 location=None):
        self.name = name
        self.ip = ip
        self.tn = tn
        self.tmax = tmax
        self.dmax = dmax
        self.location = location
        
        self.reported = reported
        self.gmond_started = gmond_started
        
        self._metrics = {}
    
    def __contains__(self, metric):
        return metric in self._metrics
    
    def __iter__(self):
        return iter(self._metrics)
    
    def __getitem__(self, metricname):
        return self._metrics[metricname]

    def __setitem__(self, metricname, metric):
        self._metrics[metricname] = metric
    
    def __unicode__(self):
        return self.name
    
    def __str__(self):
        return self.name


class Cluster(object):
    def __init__(self, name, localtime,
                 owner=None,
                 url=None,
                 latlong=None):
        self.name = name
        self.localtime = localtime
        self.owner = owner
        self.url = url
        self.latlong = latlong
        
        self._hosts = {}
    
    def __contains__(self, host):
        return host in self._hosts
    
    def __iter__(self):
        return iter(self._hosts)
    
    def __getitem__(self, hostname):
        return self._hosts[hostname]
    
    def __setitem__(self, hostname, host):
        self._hosts[hostname] = host
    
    def __unicode__(self):
        return self.name
    
    def __str__(self):
        return self.name


class Grid(object):
    def __init__(self, name, localtime, authority=None):
        self.name = name
        self.authority = authority
        self.localtime = localtime
        self._clusters = {}
    
    def __contains__(self, cluster):
        return cluster in self._clusters
    
    def __iter__(self):
        return iter(self._clusters)
    
    def __getitem__(self, clustername):
        return self._clusters[clustername]
    
    def __setitem__(self, clustername, cluster):
        self._clusters[clustername] = cluster
    
    def __unicode__(self):
        return self.name
    
    def __str__(self):
        return self.name


