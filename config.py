import os

class ProductionConfig:
    SQLALCHEMY_DATABASE_URI = os.environ.get("postgresql://dbname_5up9_user:P6VLdUfz2uRYXT8rtJ22YrIHbTcfaYea@dpg-d611s94hg0os73d007d0-a.virginia-postgres.render.com/dbname_5up9")
    CACHE_TYPE = "SimpleCache"

