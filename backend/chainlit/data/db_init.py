from sqlalchemy import create_engine, Column, Integer, String, DateTime, UUID, JSON, ForeignKey, ARRAY, Boolean
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime, uuid

Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'
    id = Column(UUID, primary_key=True, default=uuid.uuid4())
    identifier = Column(String, unique=True, nullable=False)
    metadata = Column(JSON, nullable=False)
    createdAt = Column(DateTime, nullable=False, default=datetime.utcnow())
    
    def __repr__(self):
        return f"<User(id={self.id}, identifier={self.identifier})>"
    
    def get_user(self, identifier):
        return self.query.filter_by(identifier=identifier).first()
    
    def create_user(self, identifier):
        user = self.get_user(identifier)
        if user:
            return user
        new_user = Users(identifier=identifier)
        db.session.add(new_user)
        db.session.commit()
        return new_user

class Threads(Base):
    __tablename__ = 'threads'
    id = Column(UUID, primary_key=True)
    userId = Column(UUID, ForeignKey('users.id'), nullable=False)
    name = Column(String, nullable=False)
    userIdentifier = Column(String, nullable=False)
    tags = Column(ARRAY(String), nullable=False)
    metadata = Column(JSON, nullable=False)
    createdAt = Column(DateTime, nullable=False, default=datetime.utcnow())

class Steps(Base):
    __tablename__ = 'steps'
    id = Column(UUID, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    threadId = Column(UUID, ForeignKey('threads.id'), nullable=False)
    parentId = Column(UUID)
    disableFeedback = Column(Boolean, nullable=False)
    streaming = Column(Boolean, nullable=False)
    waitForAnswer = Column(Boolean)
    isError = Column(Boolean)
    metadata = Column(JSON, nullable=False)
    tags = Column(ARRAY(String), nullable=False)
    input = Column(String)
    output = Column(String)
    createdAt = Column(DateTime, nullable=False, default=datetime.utcnow)
    start = Column(DateTime)
    end = Column(DateTime)
    generation = Column(JSON)
    showInput = Column(String)
    language = Column(String)
    indent = Column(Integer)

class Elements(Base):
    __tablename__ = 'elements'
    id = Column(UUID, primary_key=True)
    threadId = Column(UUID, ForeignKey('threads.id'), nullable=False)
    type = Column(String, nullable=False)
    url = Column(String)
    chainlitKey = Column(String)
    name = Column(String, nullable=False)
    display = Column(String)
    objectKey = Column(String)
    size = Column(String)
    page = Column(Integer)
    language = Column(String)
    forId = Column(UUID)
    mime = Column(String)


class Feedbacks(Base):
    __tablename__ = 'feedbacks'
    id = Column(UUID, primary_key=True)
    forId = Column(UUID, nullable=False)
    value = Column(Integer, nullable=False)
    comment = Column(String)


def init_db(db_url):
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()