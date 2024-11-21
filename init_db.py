from app import app, db, User
from werkzeug.security import generate_password_hash
import os

def init_db():
    try:
        with app.app_context():
            # Drop all tables first to ensure clean state
            db.drop_all()
            print("Dropped existing tables.")
            
            # Create all tables
            db.create_all()
            print("Created new tables.")

            # Check if admin user exists
            admin = User.query.filter_by(username='admin').first()
            if not admin:
                # Create admin user
                admin = User(
                    username='admin',
                    password_hash=generate_password_hash('admin', method='pbkdf2:sha256')
                )
                db.session.add(admin)
                db.session.commit()
                print("Admin user created successfully!")
            else:
                print("Admin user already exists!")
                
    except Exception as e:
        print(f"Error initializing database: {str(e)}")
        raise

if __name__ == '__main__':
    init_db()
