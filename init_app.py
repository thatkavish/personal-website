from app import app, db, User, BlogPost, Book
from werkzeug.security import generate_password_hash
from datetime import datetime
import logging
import os

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def init_app():
    with app.app_context():
        try:
            # Drop all tables first
            logger.info("Dropping all existing tables...")
            db.drop_all()
            
            # Create all tables
            logger.info("Creating database tables...")
            db.create_all()

            # Verify tables were created
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            logger.info(f"Created tables: {tables}")

            # Check if admin user exists
            if not User.query.filter_by(username='admin').first():
                logger.info("Creating admin user...")
                admin = User(
                    username='admin',
                    password_hash=generate_password_hash('admin', method='pbkdf2:sha256')
                )
                db.session.add(admin)
                db.session.commit()
                logger.info("Admin user created successfully!")

            # Add sample blog posts if they don't exist
            if not BlogPost.query.first():
                logger.info("Adding sample blog posts...")
                posts = [
                    {
                        'title': 'AI in Economic Policy',
                        'content': 'Exploring how artificial intelligence is reshaping economic policy-making...',
                        'description': 'An analysis of AI\'s impact on economic policy decisions',
                        'date_posted': datetime.utcnow()
                    },
                    {
                        'title': 'Machine Learning in Economics',
                        'content': 'How machine learning algorithms are transforming economic analysis...',
                        'description': 'Overview of ML applications in economic research',
                        'date_posted': datetime.utcnow()
                    }
                ]
                
                for post in posts:
                    blog_post = BlogPost(**post)
                    db.session.add(blog_post)
                logger.info("Sample blog posts added!")

            # Add sample books if they don't exist
            if not Book.query.first():
                logger.info("Adding sample books...")
                books = [
                    {
                        'title': 'Deep Learning',
                        'author': 'Ian Goodfellow, Yoshua Bengio, Aaron Courville',
                        'notes': 'Comprehensive overview of deep learning principles',
                        'date_added': datetime.utcnow()
                    },
                    {
                        'title': 'Economics of AI',
                        'author': 'Various Authors',
                        'notes': 'Collection of papers on AI\'s economic implications',
                        'date_added': datetime.utcnow()
                    }
                ]
                
                for book in books:
                    book_entry = Book(**book)
                    db.session.add(book_entry)
                logger.info("Sample books added!")

            db.session.commit()
            logger.info("Database initialization completed successfully!")
            
            # Verify data was added
            blog_count = BlogPost.query.count()
            book_count = Book.query.count()
            user_count = User.query.count()
            logger.info(f"Database contains: {blog_count} blog posts, {book_count} books, {user_count} users")
            
        except Exception as e:
            logger.error(f"Error during database initialization: {str(e)}")
            db.session.rollback()
            raise

if __name__ == '__main__':
    init_app()
