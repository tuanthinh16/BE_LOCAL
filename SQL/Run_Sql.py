from sqlalchemy import text

class DAO:
    def __init__(self, db_session) -> None:
        self.db_session = db_session

    def get(self,query):
        if query:
            try:
                # Use SQLAlchemy's text() function to handle raw SQL
                result = self.db_session.execute(text(query))
                rows = result.fetchall()
                return rows
            except Exception as e:
                # Handle and log the exception
                return {'error': str(e)}
        else:
            return None
