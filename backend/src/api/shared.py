from ..dinnerme.mongo import MongoManager
from ..dinnerme.manager import Manager

db = MongoManager()
manager = Manager(db)
