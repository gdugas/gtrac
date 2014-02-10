from trac.core import Component, implements
from trac.admin import IAdminCommandProvider
from gtrac.triggers import TriggerParser
from gtrac.ganglia.gmetad import get_daemon_metas
from gtrac.tracker import check_metric, check_host

class Console(Component):
    implements(IAdminCommandProvider)
    
    def get_admin_commands(self):
        '''
        gtrac check [hostname[:port]]
        '''
        yield ('gtrac monitor', '',
               'Check currents gmetad metrics',
               None, self.run_monitoring)
    
    
    def run_monitoring(self):
        
        parser = TriggerParser(self.env)
        
        hostname = self.env.config.get('gtrac', 'host')
        port = self.env.config.getint('gtrac', 'port') or 8651
        
        grids = get_daemon_metas(hostname, port)
        
        for grid_name in grids:
            grid = grids[grid_name]
            
            for cluster_name in grid:
                cluster = grid[cluster_name]
                
                for host_name in cluster:
                    host = cluster[host_name]
                    
                    # Submit ticket on host down
                    check_host(self.env, host)
                    for metric_name in host:
                        metric = host[metric_name]
                        triggers = parser.get_triggers(metric) \
                                    or []
                        # Check metric an submit ticket if needed
                        check_metric(self.env, metric, triggers)
