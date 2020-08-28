from .user import SqliteUserAdapter
from .wake import SqliteWakeAdapter
from .supboard import SqliteSupboardAdapter
from .bathhouse import SqliteBathhouseAdapter

if __name__ == "__main__":
    SqliteUserAdapter, SqliteWakeAdapter, SqliteSupboardAdapter
    SqliteBathhouseAdapter
