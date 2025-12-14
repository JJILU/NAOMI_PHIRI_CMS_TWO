from extensions import db



def create_tables():
    """Create all database tables"""
    try:
        db.create_all()
        print("Tables created successfully!")
    except Exception as e:
        print(f"Error occurred while creating tables: {e}")    