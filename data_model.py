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

    def to_dict(self):
        return {
            'product_id': self.product_id,
            'height': self.height,
            'width': self.width,
            'depth': self.depth,
            'weight': self.weight,
            'special_handling_instructions': self.special_handling_instructions,
        }


def create_tables():
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    create_tables()


    print('Tables created successfully.')
