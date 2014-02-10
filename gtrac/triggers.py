from gtrac.ganglia.models import Metric
from gtrac.utils import cmp

class Trigger(object):
    
    class ComparisonException(Exception):
        pass
    
    @staticmethod
    def get_builtin_cmp(cmp_name):
        cmp_function = 'do_%s' % cmp_name
        if not getattr(cmp, cmp_function, None):
            raise Trigger.ComparisonException(cmp_name)
        return getattr(cmp, cmp_function)
    
    def get_cmp_function(self):
        splitted = self.comparison.split('.')
        if len(splitted) > 1:
            try:
                mod_name = '.'.join(splitted[:-1])
                module = __import__(mod_name, globals(), locals(),
                                    [splitted[-1]], 0)
                return getattr(module, splitted[-1])
            except:
                raise Trigger.ComparisonException(self.comparison)
        
        else:
            return Trigger.get_builtin_cmp(self.comparison)
    
    def __init__(self, comparison, treshold, priority):
        self.comparison = comparison
        self.treshold = treshold
        self.priority = priority
    
    def __call__(self, metric):
        treshold = self.treshold
        if isinstance(metric, Metric):
            treshold = metric.to_python(treshold)
        
        return self.get_cmp_function()(metric, treshold)
    
    def __unicode__(self):
        return "%s:%s:%s" % (self.comparison,
                             self.treshold,
                             self.priority)
    
    def __str__(self):
        return self.__unicode__()
