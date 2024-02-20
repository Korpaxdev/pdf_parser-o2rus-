from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from modules.database.models import BaseTable
from utils.constants import ResultFiles


class DBService:
    def __init__(self):
        self.db_path = ResultFiles.RESULT_DB
        self._engine = create_engine(f"sqlite:///{ResultFiles.RESULT_DB}")
        self._Session = sessionmaker(bind=self._engine)

    def clear_database(self):
        self._drop_database()
        self._create_database()

    def insert_all(self, data: list[BaseTable]):
        with self._Session() as session:
            session.add_all(data)
            session.commit()

    def _drop_database(self):
        BaseTable.metadata.drop_all(self._engine)

    def _create_database(self):
        BaseTable.metadata.create_all(self._engine)
