from trac.ticket.model import Ticket

class Alert(object):
    def __init__(self, env,
                 id=None,
                 ticket=None,
                 metric=None,
                 value=None,
                 date=None):
        self.env = env
        self.id = id
        self.ticket = ticket
        self.metric = metric
        self.value = value
        self.date = date
        self.load()
    
    def load(self):
        clause = []
        if self.id:
            clause.append('id')
            clause.append(str(self.id))
        elif isinstance(self.ticket, Ticket):
            clause.append('ticket_id')
            clause.append(str(self.ticket.id))
        else:
            return
        
        with self.env.db_query as db:
            sql = "SELECT * FROM gtrac_alert WHERE "
            sql += "=".join(clause)
            for fields in db(sql):
                self.id = fields[0]
                self.ticket = Ticket(self.env, tkt_id=fields[1])
                self.metric = fields[2]
                self.value = fields[3]
                self.date = fields[4]
                return
    
    def save(self):
        pass
    
    def delete(self):
        pass
            