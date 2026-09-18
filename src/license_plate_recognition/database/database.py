from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from ..config import Config


class Base(DeclarativeBase):
    pass


class Database:

    def __init__(self):
        # =========================
        # Connection Url
        # =========================

        connection_url = URL.create(
            "mysql+pymysql",
            username=Config.DB_USER,
            password=Config.DB_PASSWORD,
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            database=Config.DB_NAME,
        )

        # =========================
        # Engine
        # =========================

        self.engine = create_engine(
            connection_url,
            pool_pre_ping=True,
        )

        # =========================
        # Session
        # =========================

        self.SessionLocal = sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
        )

    def get_session(self):
        """
        取得 Session
        """

        return self.SessionLocal()

    def dispose(self):
        """
        關閉 Engine
        """

        self.engine.dispose()

    def create_tables(self):
        """
        建立 Table
        """

        Base.metadata.create_all(self.engine)
