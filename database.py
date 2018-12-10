import pickledb


class Database(object):
    def __init__(self, name):
        self.db = pickledb.load(name, False)

    def set(self, key, value):
        self.db.set(key, value)

    def get(self, key):
        return self.db.get(key)

    def dump(self):
        return self.db.dump()

    def snapshot(self):
        db_snapshot = dict()
        keys = self.db.getall()

        for key in keys:
            db_snapshot[key] = self.get(key)
        return db_snapshot

    def deldb(self):
        self.db.deldb()



    