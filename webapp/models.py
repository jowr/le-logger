
#class MeasurementCampaign(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    name = db.Column(db.String(50))

class MeasurementCampaign(object):
    id = 0
    name = "The name"

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category %r>' % self.name

class MeasurementSet(object):
    id = 0
    campaign = "The category"

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category %r>' % self.name