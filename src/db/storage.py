from db.mongodb import MongoStorage


mongo: MongoStorage | None = None


def get_mongo() -> MongoStorage:
    return mongo
