import os
import json
from datetime import datetime
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Text, LargeBinary
from sqlalchemy.types import TypeDecorator

# Custom type for handling JSON (for image list)
class JSONEncodedDict(TypeDecorator):
    impl = Text

    def process_bind_param(self, value, dialect):
        if value is not None:
            return json.dumps(value)
        return None

    def process_result_value(self, value, dialect):
        if value is not None:
            return json.loads(value)
        return None

# Setup DB Path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
DB_PATH = os.path.join(DATA_DIR, 'app.db')

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

DATABASE_URL = f"sqlite:///{DB_PATH}"

Base = declarative_base()
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}) 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --- Models ---

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    project_code = Column(String, unique=True, nullable=False)
    project_name = Column(String, nullable=False)
    title = Column(String, default="Weekly Project Update")
    project_progress = Column(Integer, default=0)
    pending_rfi = Column(Integer, default=0)
    days_spent = Column(Integer, default=0)
    model_review_link = Column(String, nullable=True)
    rfi_sheet_link = Column(String, nullable=True)
    alert_note = Column(Text, nullable=True) # Text data type, consistent with current_progress
    current_progress = Column(Text, nullable=True)
    next_week_plan = Column(Text, nullable=True)
    
    # New Fields for Logos and Carousel
    client_logo_base64 = Column(Text, nullable=True) # Base64 string for client logo
    kshitij_logo_base64 = Column(Text, nullable=True) # Base64 string for kshitij logo
    carousel_images_json = Column(JSONEncodedDict, default=lambda: []) # List of image Base64 strings
    
    updated_at = Column(String, default=datetime.utcnow().isoformat)

class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    project_code = Column(String, nullable=False)
    client_name = Column(String, nullable=False)
    comment = Column(Text, nullable=False)
    created_at = Column(String, default=datetime.utcnow().isoformat)

# --- DB Functions ---

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_project_by_code(project_code: str):
    session = SessionLocal()
    try:
        # Use session.execute and mapping for better column handling if schema evolves
        project_data = session.query(Project).filter(Project.project_code == project_code).first()
        if project_data:
             # Convert to dict to handle JSON field correctly
            data = project_data.__dict__.copy()
            data.pop('_sa_instance_state', None)
            return data
        return None
    finally:
        session.close()

def list_project_codes():
    session = SessionLocal()
    try:
        projects = session.query(Project.project_code).all()
        return [p[0] for p in projects]
    finally:
        session.close()

def upsert_project(data: dict):
    session = SessionLocal()
    try:
        project_code = data['project_code']
        project = session.query(Project).filter(Project.project_code == project_code).first()
        
        if not project:
            # New Project
            project = Project(**data)
            session.add(project)
        else:
            # Update Existing Project
            for key, value in data.items():
                if key != 'id': # Don't update the primary key
                    setattr(project, key, value)
            project.updated_at = datetime.utcnow().isoformat()
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def add_comment(project_code, client_name, comment_text):
    session = SessionLocal()
    try:
        new_comment = Comment(
            project_code=project_code,
            client_name=client_name,
            comment=comment_text,
            created_at=datetime.utcnow().isoformat()
        )
        session.add(new_comment)
        session.commit()
    finally:
        session.close()

def list_comments(project_code, limit=500):
    session = SessionLocal()
    try:
        comments = session.query(Comment)\
            .filter(Comment.project_code == project_code)\
            .order_by(Comment.id.desc())\
            .limit(limit).all()
        # Return as list of dicts for pandas
        return [{
            "Client": c.client_name,
            "Comment": c.comment,
            "Timestamp (UTC)": c.created_at
        } for c in comments]
    finally:
        session.close()
