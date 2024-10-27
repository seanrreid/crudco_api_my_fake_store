from sqlmodel import create_engine, SQLModel, Session

DATABASE_URL = 'postgresql://postgres.swepwqrdkebfdvzcaezn:DJ7$if9w6jd2@aws-0-us-west-1.pooler.supabase.com:6543/postgres'

engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session
