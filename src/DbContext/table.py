import os

from database import DB_NAME, create_tables

if os.path.exists(DB_NAME):
    os.remove(DB_NAME)
create_tables()
