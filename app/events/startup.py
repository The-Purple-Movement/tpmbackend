from app.db.session import engine, Base

def init_db():
    print("Initializing database tables...")
    Base.metadata.create_all(bind=engine) # creates new tables only if it doesnot exists, but cant do migrations
    print("Tables created successfully!")