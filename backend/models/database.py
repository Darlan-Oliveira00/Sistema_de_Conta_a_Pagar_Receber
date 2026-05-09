def init_db():
    from sqlalchemy_utils import create_database, database_exists
    from dotenv import load_dotenv
    import os

    load_dotenv()

    db_url = os.getenv("URL_DB")
    if not database_exists(db_url):
        create_database(db_url)
