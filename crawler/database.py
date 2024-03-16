import json
import os

import pandas as pd
from sqlalchemy import URL, create_engine, text
from sqlalchemy.exc import SQLAlchemyError




class DataBase:
    def __init__(self):

        self.url_object = URL.create(
            "postgresql",
            username="develop",
            password="sv32961018",
            host="postgresql",
            database="db_precompra",
        )
        # Tenta conectar ao banco de dados
        try:
            self.db = create_engine(self.url_object)
            self.cursor = self.db.connect()
            print(
                f"The database {
                    os.getenv('DB_DATABASE')} connection has been established!"
            )
        except SQLAlchemyError as err:
            print(f"Failed to try connect to the bank, {err}")

    def execute(self, query):

        try:
            with self.db.connect() as connection:
                if query.lower().startswith("select") or "returning" in query.lower():
                    data = json.loads(
                        pd.read_sql(text(query), connection).to_json(
                            orient="records")
                    )
                    connection.commit()
                    if data == []:
                        return None
                    return data
                elif query.lower().startswith("update") or query.lower().startswith(
                    "insert"
                ):
                    result = connection.execute(text(query))
                    affected_rows = result.rowcount
                    connection.commit()
                    if affected_rows == 0:
                        return f"No rows were affected by the operation."

                    return {
                        "status": "Success",
                        "message": f"Operation completed successfully, {affected_rows} lines were changed",
                    }

        except SQLAlchemyError as err:
            print(f"Failed to execute query: {err}")
            return f"Failed to execute query {err}"


db = DataBase()
