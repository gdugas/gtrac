from trac.ticket.model import Ticket

class Tracker(object):
    
    RESOLUTION_FIXED = 'fixed'
    
    STATUS_OPEN = 'open'
    STATUS_CLOSED = 'closed'
    
    defaults = {'type': 'monitor',
                 'reporter': 'gtrac_plugin'}
    
    def __init__(self, env, component):
        self.env = env
        self.component = component
    
    def component_str(self):
        raise NotImplementedError()
    
    def get_new_ticket(self):
        t = Ticket(self.env)
        for key, value in self.defaults.items():
            t[key] = value
        t['component'] = self.component_str()
        t['status'] = self.STATUS_OPEN
        return t
    
    def last_open_ticket(self):
        tkt_id = self.last_open_ticket_id()
        if tkt_id:
            return Ticket(self.env, tkt_id=tkt_id)
    
    def last_open_ticket_id(self):
        sql  = "SELECT id FROM ticket"
        sql += " WHERE status != '%s'" % self.STATUS_CLOSED
        sql += "  AND component == '%s'" % self.component_str()
        sql += " ORDER BY time desc"
        with self.env.db_transaction as db:
            cursor = db.cursor()
            res = cursor.execute(sql).fetchone()
            if res:
                return res[0]
    
    def last_closed_ticket(self):
        tkt_id = self.last_closed_ticket_id()
        if tkt_id:
            return Ticket(self.env, tkt_id=tkt_id)
    
    def last_closed_ticket_id(self):
        sql  = "SELECT id FROM ticket"
        sql += " WHERE status == '%s'" % self.STATUS_CLOSED
        sql += "  AND component == '%s'" % self.component_str()
        sql += " ORDER BY time desc"
        with self.env.db_transaction as db:
            cursor = db.cursor()
            res = cursor.execute(sql).fetchone()
            if res:
                return res[0]
    
    def update_ticket(self, ticket, comment=None):
        if ticket.exists:
            ticket.save_changes(author='gtrac_plugin', comment=comment)
        else:
            ticket['description'] = comment
            ticket.insert()
    
    def close_ticket(self, ticket, comment=None, resolution=None):
        ticket['status'] = self.STATUS_CLOSED
        ticket['resolution'] = resolution or self.RESOLUTION_FIXED
        ticket.save_changes(author='gtrac_plugin', comment=comment)


class MetricTracker(Tracker):
    def component_str(self):
        host = self.component.host
        cluster = host.cluster
        grid = cluster.grid
        component = '.'.join([grid.name,
                              cluster.name,
                              host.name,
                              self.component.name])
        return component

class HostTracker(Tracker):
    def component_str(self):
        cluster = self.component.cluster
        grid = cluster.grid
        component = '.'.join([grid.name,
                              cluster.name,
                              self.component.name])
        return component



def check_metric(env, metric, triggers):
    tracker = MetricTracker(env, metric)
    ticket = tracker.last_open_ticket()
    # Exit and close ticket if no trigger available
    if len(triggers) == 0:
        if ticket:
            comment = 'Trigger unavailable'
            tracker.close_ticket(ticket, comment=comment)
            return ticket
        return

    triggered = False
    for trigger in triggers:
        if trigger(metric):
            triggered = True
            if ticket:
                if not trigger.priority == ticket['priority']:
                    comment = 'Update priority'
                    ticket['severity'] = str(metric.value)
                    ticket['priority'] = trigger.priority
                    tracker.update_ticket(ticket, comment=comment)
            else:
                ticket = tracker.get_new_ticket()
                comment = 'Triggered Metric'
                ticket['summary'] = '[trigger] %s' % metric.name
                ticket['severity'] = str(metric.value)
                ticket['priority'] = trigger.priority
                tracker.update_ticket(ticket, comment=comment)
            break
    
    if not triggered and ticket:
        comment = 'Not triggered metric'
        ticket['severity'] = str(metric.value)
        ticket['priority'] = None
        tracker.close_ticket(ticket, comment=comment)
    
    return ticket


def host_is_down(env, host):
    timeout = env.config.getint('gtrac', 'host.down.timeout')
    return host.tn - timeout > host.tmax


def check_host(env, host):
    tracker = HostTracker(env, host)
    ticket = tracker.last_open_ticket()
    down = host_is_down(env, host)
    
    if down and not ticket:
        priority = env.config.get('gtrac', 'host.down.priority') \
                    or 'critical'
        ticket = tracker.get_new_ticket()
        comment = 'Triggered Metric'
        ticket['summary'] = '[host_down] %s' % host.name
        ticket['priority'] = priority
        tracker.update_ticket(ticket, comment=comment)
    
    elif not down and ticket:
        priority = env.config.get('gtrac', 'host.up.priority') \
                    or 'low'
        comment = 'Host up !'
        ticket['priority'] = priority
        tracker.close_ticket(ticket, comment=comment)
    
    return ticket
