from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:root1234@127.0.0.1:3306/geeker"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={},
    echo=True,  # echo 设为 True 会打印出实际执行的 sql
    pool_size=5,
    pool_recycle=3600,
)
SessionLocal = sessionmaker(autocommit=False, expire_on_commit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
