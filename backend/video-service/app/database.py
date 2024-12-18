import oracledb


def get_db():
    connection = oracledb.connect(
        user="system",
        password="your_password",  # Use the password from docker-compose
        dsn="oracle-db:1521/XEPDB1",
    )
    try:
        yield connection
    finally:
        connection.close()
