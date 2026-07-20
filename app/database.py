from sqlmodel import SQLModel, Session, create_engine, select

from app.models import Task

DATABASE_URL = "sqlite:///tasks.db"

engine = create_engine(
    DATABASE_URL,
    echo=True,
    connect_args={"check_same_thread": False}
)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        statement = select(Task)
        tasks = session.exec(statement).all()

        if len(tasks) == 0:
            session.add(Task(title="Learn FastAPI"))
            session.add(Task(title="Build CRUD API"))
            session.add(Task(title="Connect SQLite"))
            session.commit()


def get_session():
    with Session(engine) as session:
        yield session