class Api:
    def __init__(self, db):
        self.db = db
        self.error = None
        self.erred = False

    def set_error(self, message):
        self.error = message
        self.erred = True
    
    def clear_error(self):
        self.error = None
        self.erred = False

    def list(self, table, assume_exists=False):
        self.clear_error()
        
        try:
            items = table.query.filter((table.status == 0)).all()
            if not items and assume_exists:
                self.set_error("list {} failed; none found".format(table))
            return items
        except Exception as e:
            self.set_error("list {} failed; {}".format(table, str(e)))
            return None
    
    def get(self, table, id, assume_exists=True):
        self.clear_error()

        try:
            item = table.query.filter_by(id=id).first()
            if not item and assume_exists:
                self.set_error("get {} failed; not found".format(table))
            return item
        except Exception as e:
            self.set_error("get {} failed; {}".format(table, str(e)))

    def create(self, table, instance):
        self.clear_error()

        try:
           self.db.session.add(instance)
           self.db.session.commit()
           return instance
        except Exception as e:
            self.set_error("create {} failed; {}".format(table, str(e)))
            return None
    
    def update(self, table, instance):
        self.clear_error()

        try:
            self.db.session.add(instance)
            self.db.session.commit()
            return instance
        except Exception as e:
            self.set_error("update {} failed; {}".format(table, str(e)))
            return None
    
    def delete(self, table, instance):
        self.clear_error()

        instance.status = 1

        try:
            self.db.session.add(instance)
            self.db.session.commit()
            return instance
        except Exception as e:
            self.set_error("delete {} failed; {}".format(table, str(e)))
            return None

    def restore(self, table, instance):
        self.clear_error()

        instance.status = 0

        try:
            self.db.session.add(instance)
            self.db.session.commit()
            return instance
        except Exception as e:
            self.set_error("restore {} failed; {}".format(table, str(e)))
            return None

    