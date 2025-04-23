from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

db_type = "mysql"
db_user = "kishor"
db_pass = "kishor"
db_host = "localhost"
db_port = "3306"
db_name = "fastpizza"

# engine = create_engine(
#     "mysql://kishor:kishor@localhost/fastpizza",
#     echo=True
# )

engine = create_engine(
        url="mysql://{0}:{1}@{2}:{3}/{4}".format(
            db_user, db_pass, db_host, db_port, db_name
        )
    )

Base = declarative_base()

Session = sessionmaker()