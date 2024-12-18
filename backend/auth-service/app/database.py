import oracledb
import logging

logger = logging.getLogger(__name__)


def get_db():
    try:
        connection = oracledb.connect(
            user="system",
            password="your_password",  # Make sure this matches your docker-compose.yml
            dsn="oracle-db:1521/XEPDB1",
        )
        try:
            yield connection
        finally:
            connection.close()
    except Exception as e:
        logger.error(f"Database connection error: {str(e)}")
        raise
