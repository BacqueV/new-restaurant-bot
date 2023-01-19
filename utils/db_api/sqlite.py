import sqlite3


class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    def create_table_users(self):
        sql = """
        CREATE TABLE Users(
            id INTEGER NOT NULL,
            Name varchar(255) NOT NULL,
            username varchar(255),
            address TEXT,
            number TEXT
            PRIMARY KEY (id)
            );
"""
        self.execute(sql, commit=True)

    def create_table_orders(self):
        sql = """
        CREATE TABLE Orders(
            id INTEGER,
            user_id INTEGER NOT NULL,
            number TEXT,
            lat REAL,
            lon REAL,
            PRIMARY KEY (id)
            );
"""
        self.execute(sql, commit=True)

    def create_categories(self):
        sql = """
        CREATE TABLE Categories(
        id INTEGER PRIMARY KEY,
        name VARCHAR(255) NOT NULL UNIQUE,
        description TEXT
        );"""
        self.execute(sql, commit=True)

    def create_table_meals(self):
        sql = """
        CREATE TABLE Meals(
        id INTEGER NOT NULL,
        name VARCHAR(255) NOT NULL UNIQUE,
        description TEXT NOT NULL,
        price REAL NOT NULL
        );"""
        self.execute(sql, commit=True)

    def create_table_cart(self):
        sql = """
        CREATE TABLE Cart (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL UNIQUE
        );"""
        self.execute(sql, commit=True)

    def create_table_cart_items(self):
        sql = """
        CREATE TABLE CartItems (
            id INTEGER PRIMARY KEY,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            cost REAL NOT NULL,
            cart_id INTEGER NOT NULL
        );"""
        self.execute(sql, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def add_user(self, id: int, name: str, username: str = None):
        # SQL_EXAMPLE = "INSERT INTO Users(id, Name, username) VALUES(1, 'John', '@example_username')"

        sql = """
        INSERT INTO Users(id, Name, username) VALUES(?, ?, ?)
        """
        self.execute(sql, parameters=(id, name, username), commit=True)

    def add_user_cart(self, user_id: int):
        # SQL_EXAMPLE = "INSERT INTO Cart(user_id) VALUES(1)"

        sql = """
        INSERT INTO Cart(user_id) VALUES(?)
        """
        self.execute(sql, parameters=(user_id, ), commit=True)

    def add_cart_item(self, product_id: int, quantity: int, cost: int, cart_id: int):
        # SQL_EXAMPLE = "INSERT INTO CartItems(user_id) VALUES(1)"

        sql = """
        INSERT INTO CartItems(product_id, quantity, cost, cart_id) VALUES(?, ?, ?, ?)
        """
        self.execute(sql, parameters=(product_id, quantity, cost, cart_id), commit=True)

    def select_all_users(self):
        sql = """
        SELECT * FROM Users
        """
        return self.execute(sql, fetchall=True)

    def select_cart(self, **kwargs):
        sql = """
        SELECT * FROM Cart WHERE 
        """
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)

    def select_categories(self):
        sql = """
                SELECT * FROM Categories;
                """
        return self.execute(sql, fetchall=True)

    def check_existence_number(self, id):
        sql = 'SELECT number FROM Orders WHERE user_id=?'
        return self.execute(sql, (id, ), fetchone=True)

    def get_category(self, **kwargs):
        sql = """
        SELECT * FROM Categories WHERE 
        """
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)

    def get_all_items(self, **kwargs):
        sql = """
        SELECT product_id, quantity, cost FROM CartItems WHERE 
        """
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchall=True)

    def select_all_meals(self, **kwargs):
        sql = """
                SELECT * FROM Meals WHERE 
                """
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchall=True)

    def get_data(self, **kwargs):
        sql = """
                SELECT * FROM Meals WHERE 
                """
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)

    def select_user(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)

    def check_existence(self, product_id: int, cart_id: int):
        sql = """SELECT * FROM CartItems WHERE product_id=? AND cart_id=?;"""
        return self.execute(sql, parameters=(product_id, cart_id), fetchone=True)

    def update_cart_data(self, quantity: int, cost: float, product_id: int, cart_id: int):
        sql = """UPDATE CartItems SET quantity=?, cost=? WHERE product_id=? AND cart_id=?;"""
        return self.execute(sql, parameters=(quantity, cost, product_id, cart_id), commit=True)

    def update_order_data(self, number, lat, lon, user_id):
        sql = """UPDATE Orders SET number=?, lat=?, lon=? WHERE user_id=?;"""
        return self.execute(sql, parameters=(number, lat, lon, user_id), commit=True)

    def add_order(self, user_id, number, lat, lon):
        sql = """
        INSERT INTO Orders (user_id, number, lat, lon) VALUES (?, ?, ?, ?)
        """
        self.execute(sql, parameters=(user_id, number, lat, lon), commit=True)

    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM Users;", fetchone=True)

    def update_user_username(self, username, id):
        # SQL_EXAMPLE = "UPDATE Users SET username=example_username WHERE id=12345"

        sql = f"""
        UPDATE Users SET username=? WHERE id=?
        """
        return self.execute(sql, parameters=(username, id), commit=True)

    def delete_users(self):
        self.execute("DELETE FROM Users WHERE TRUE", commit=True)

    def delete_data(self, cart_id: int):
        sql = f"""
        DELETE FROM CartItems WHERE cart_id=?
        """
        return self.execute(sql, parameters=(cart_id, ), commit=True)

    def delete_data_user(self, cart_id):
        sql = f"""
        DELETE FROM CartItems WHERE cart_id=?
        """
        return self.execute(sql, parameters=(cart_id, ), commit=True)


def logger(statement):
    print(f"""
_____________________________________________________
Executing:
{statement}
_____________________________________________________
""")
