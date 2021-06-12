from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, MetaData, ForeignKey, Boolean, Text, Date, create_engine, \
    CheckConstraint
from config import USER, PASSWORD

Base = declarative_base()

engine = create_engine('postgresql://{}:{}@localhost/mtg'.format(USER, PASSWORD),
                       echo=True)

new_engine = 0

class Card(Base):
    __tablename__ = 'Cards'
    __table_args__ = {'schema': 'public'}

    ManaValue = Column(Integer, CheckConstraint('ManaValue >= 0'), nullable=False)
    Set = Column(String, ForeignKey("public.Sets.Name"), nullable=False)
    Name = Column(String, primary_key=True, nullable=False, autoincrement=True)
    Rarity = Column(String(8), nullable=False)
    Color = Column(String(9), nullable=False)
    isLegendary = Column(Boolean, nullable=False, default=False)
    Type = Column(String(12), nullable=False)

    def __init__(self, name, color, mana_value, type, set, rarity, is_legendary_):
        self.Name = name
        self.Color = color
        self.ManaValue = mana_value
        self.Type = type
        self.Set = set
        self.Rarity = rarity
        self.isLegendary = is_legendary_

    def __repr__(self):
        return self.Name


class Set(Base):
    __tablename__ = 'Sets'
    __table_args__ = {'schema': 'public'}

    Name = Column(String, primary_key=True, nullable=False, autoincrement=True)
    Size = Column(Integer, CheckConstraint('Size > 0'), nullable=False)
    Block = Column(String, nullable=False)
    ReleaseDate = Column(Date, nullable=False)
    SetCode = Column(String(3), CheckConstraint('SetCode == upper(SetCode)'), nullable=False, unique=True)
    CountCards = Column(Integer, default=0)

    def __init__(self, name, set_code, release_date, size, block, count_cards):
        self.Name = name
        self.SetCode = set_code
        self.ReleaseDate = release_date
        self.Size = size
        self.Block = block
        self.CountCards = count_cards

    def __repr__(self):
        return self.Name
