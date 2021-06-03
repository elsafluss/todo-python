import sqlite3


class Schema:
    def __init__(self):
        self.conn = sqlite3.connect('todo.db')
        self.create_user_table()
        self.create_to_do_table()

    def __del__(self):
        self.conn.commit()
        self.conn.close()

    def create_to_do_table(self):

        query = """
        CREATE TABLE IF NOT EXISTS "Todo" (
          id INTEGER PRIMARY KEY,
          Title TEXT,
          Description TEXT,
          _is_done boolean DEFAULT 0,
          _is_deleted boolean DEFAULT 0,
          CreatedOn Date DEFAULT CURRENT_DATE,
          DueDate Date,
          UserId INTEGER FOREIGNKEY REFERENCES User(_id)
        );
        """

        self.conn.execute(query)

    def create_user_table(self):

        query = """
        CREATE TABLE IF NOT EXISTS "User" (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          Name TEXT NOT NULL,
          Email TEXT,
          CreatedOn Date DEFAULT CURRENT_DATE
        );
        """

        self.conn.execute(query)


class ToDoModel:
    TABLE = "TODO"

    def __init__(self):
        self.conn = sqlite3.connect('todo.db')
        self.conn.row_factory = sqlite3.Row

    def __del__(self):
        self.conn.commit()
        self.conn.close()

    def get_by_id(self, _id):
        where_clause = f"AND id={_id}"
        return self.list_items(where_clause)

    def create(self, params):
        print(params)
        query = f'insert into {self.TABLE}' \
                f'(Title, Description, DueDate, UserId' \
                f'values ("{params.get("Title")}","{params.get("Description")}")' \
                f'values ("{params.get("DueDate")}","{params.get("UserId")}")'

        result = self.conn.execute(query)
        return self.get_by_id(result.lastrowid)

    def __delete__(self, item_id):
        query = f"UPDATE {self.TABLE} " \
                f"SET _is_deleted = {1}" \
                f"WHERE id = {item_id}"
        print(query)
        self.conn.execute(query)
        return self.list_items()

    def update(self, item_id, update_dict):
        """
        column: value
        Title: new title
        """
        set_query = ", ".join([f'{column} = {value}'
                              for column, value in update_dict.items()])

        query = f"UPDATE {self.TABLE} " \
                f"SET {set_query}" \
                f"WHERE id = {item_id}"
        self.conn.execute(query)
        return self.get_by_id(item_id)

    def list_items(self, where_clause=""):
        query = f"SELECT id, Title, Description, DueDate, _is_done " \
                f"from {self.TABLE} WHERE _is_deleted != {1} " + where_clause
        print(query)
        result_set = self.conn.execute(query).fetchall()
        result = [{column: row[i]
                  for i, column in enumerate(result_set[0].keys())}
                  for row in result_set]
        return result


class User:
    TABLE = "User"

    def create(self, name, email):
        query = f'insert into {self.TABLE} ' \
                f'(Name, Email) ' \
                f'values ({name},{email})'
        result = self.conn.execute(query)
        return result
