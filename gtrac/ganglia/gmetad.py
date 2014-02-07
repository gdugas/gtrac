from gtrac.ganglia.models import Grid, Cluster, Host, Metric
from datetime import datetime

NULL = 'unspecified'

def get_xml_metas(xml):
    
    def parse_grid(node):
        ts = float(node.attrib['LOCALTIME'])
        grid = Grid(node.attrib['NAME'],
                    datetime.fromtimestamp(ts),
                    authority=node.attrib['AUTHORITY'])
        return grid
    
    def parse_cluster(node, grid):
        ts = float(node.attrib['LOCALTIME'])
        attrs = {}
        
        if not node.attrib['OWNER'] == NULL:
            attrs['owner'] = node.attrib['OWNER']
        if not node.attrib['URL'] == NULL:
            attrs['url'] = node.attrib['url']
        if not node.attrib['LATLONG'] == NULL:
            attrs['latlong'] = node.attrib['LATLONG']
        
        cluster = Cluster(grid,
                          node.attrib['NAME'],
                          datetime.fromtimestamp(ts),
                          **attrs)
        return cluster
    
    def parse_host(node, cluster):
        attrs = {}
        
        timestamp = float(node.attrib['REPORTED'])
        reported = datetime.fromtimestamp(timestamp)
        
        timestamp = float(node.attrib['GMOND_STARTED'])
        gmon_started = datetime.fromtimestamp(timestamp)
        
        if not node.attrib['LOCATION'] == NULL:
            attrs['location'] = node.attrib['LOCATION']
        
        host = Host(cluster,
                    node.attrib['NAME'],
                    node.attrib['IP'],
                    reported,
                    int(node.attrib['TN']),
                    int(node.attrib['TMAX']),
                    int(node.attrib['DMAX']),
                    gmon_started,
                    **attrs)
        return host
    
    def parse_metric(node, host):
        extras = {}
        for elt in node.find('EXTRA_DATA'):
            extras[elt.attrib['NAME'].lower()] = elt.attrib['VAL']
        
        metric = Metric(host,
                        node.attrib['NAME'],
                        node.attrib['VAL'],
                        node.attrib['TYPE'],
                        node.attrib['UNITS'],
                        int(node.attrib['TN']),
                        int(node.attrib['TMAX']),
                        int(node.attrib['DMAX']),
                        node.attrib['SLOPE'],
                        node.attrib['SOURCE'],
                        extras = extras)
        return metric
    
    
    from xml.etree import ElementTree
    tree = ElementTree.fromstring(xml)
    
    grids = {}
    for gridnode in tree:
        grid = parse_grid(gridnode)
        grids[grid.name] = grid
        
        for clusternode in gridnode:
            cluster = parse_cluster(clusternode, grid)
            grid[cluster.name] = cluster
            
            for hostnode in clusternode:
                host = parse_host(hostnode, cluster)
                cluster[host.name] = host
                
                for metricnode in hostnode:
                    metric = parse_metric(metricnode, host)
                    host[metric.name] = metric
    return grids


def get_daemon_metas(hostname, port=8651):
    import socket
    host = socket.gethostbyname(hostname)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    
    xml = ''
    data = s.recv(4096)
    while len(data) > 0:
        xml += data
        data = s.recv(4096)
    s.close()
    
    return get_xml_metas(xml)
