import os


class General:
    collecting: bool = True


class MongoDB:
    conn_string: str = (
        f"mongodb+srv://{os.environ['MONGO_USERNAME']}:{os.environ['MONGO_PASSWORD']}@cluster0.0gz5h.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    )


class Schedule:
    fetch: int = 60 * 60 * 24
    n_weeks: int = 80
