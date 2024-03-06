from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base


from connect_connector import engine


Base = declarative_base()


class Package(Base):
    __tablename__ = 'packages'


    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, nullable=False)
    height = Column(Float, nullable=False)
    width = Column(Float, nullable=False)
    depth = Column(Float, nullable=False)
    weight = Column(Float, nullable=False)
    special_handling_instructions = Column(String, nullable=True)


def create_tables():
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    create_tables()


    print('Tables created successfully.')
