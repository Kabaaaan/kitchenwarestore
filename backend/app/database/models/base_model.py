import sqlalchemy as db
import typing
from database.models.db_config import *


class BaseModel:
    def __init__(self, table_name: str):
        self.engine = db.create_engine(CONNECT_MYSQL_STRING)
        self.connection = self.engine.connect()
        self.metaData = db.MetaData()
        self.metaData.reflect(bind=self.engine)
        self.table = db.Table(table_name, self.metaData, autoload_with = self.engine)

    def __del__(self) -> None:
        self.close_connection()

    def close_connection(self) -> None:
        self.connection.close()

    def _execute_query(self, query) -> None:
        try:
            return self.connection.execute(query)
        except Exception as e:
            self.connection = self.engine.connect()
            return self.connection.execute(query)
        
    def _format_result(self, query_result) -> typing.List[dict]:
        result = []
        column_names = list(query_result.keys())
        for row in query_result.fetchall():
            element = dict(zip(column_names, row))
            result.append(element)
        return result

    def _execute_and_commit(self, query) -> dict:
        try:
            self._execute_query(query)
            self.commit()
            return {
                "success": True,
                "message": "Operation completed successfully."
            }
        except Exception as e:
            self.connection.rollback()
            return {
                "success": False,
                "message": f"An error occurred: {str(e)}"
            }
        
    def commit(self) -> None:
        self.connection.commit()

    def select_all(self) -> typing.List[dict]:
        select_all_query = db.select(self.table)
        query_result = self._execute_query(select_all_query)
        return self._format_result(query_result)

    def select_item_by_id(self, item_id: int) -> dict:
        query = self.table.select().where(self.table.c.id == item_id)
        query_result = self._execute_query(query)
        result = self._format_result(query_result)
        if len(result) != 0:
            return result[0]
        else:
            return {'message': 'Not found.'}

    def remove_item_by_id(self, item_id: int) -> None:
        remove_query = self.table.delete().where(self.table.c.id == item_id)
        self._execute_query(remove_query)
        self.commit()

    def insert_item(self, data: dict) -> dict:
        insert_query = self.table.insert().values(**data)
        result = self._execute_and_commit(insert_query)
        return result

    def update_item_by_id(self, item_id: int, data: dict) -> dict:
        update_query = self.table.update().where(self.table.c.id == item_id).values(**data)
        result = self._execute_and_commit(update_query)
        return result
    
    def filter_by_row(self, row, row_value) -> typing.List[dict]:
        column = getattr(self.table.c, row)
        filter_query = self.table.select().where(column == row_value)
        query_result = self._execute_query(filter_query)
        result = self._format_result(query_result)
        return result