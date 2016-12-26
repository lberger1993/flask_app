import datetime

class User(db.DynamicDocument):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)

    facebook_id = db.IntField(required=True, unique=True)
    name = db.StringField(max_length=255, required=True)

    def __unicode__(self):
        return self.name

    meta = {
        'indexes' : ['-created_at', 'facebook_id'],
        'ordering' : ['-created_at']
    }