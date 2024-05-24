from .postgres import PostgresSingleton


def sessionmanager():
    return PostgresSingleton()


async def initialise_postgres_session():
    async with sessionmanager().session() as session:
        yield session
