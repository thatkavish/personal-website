from app import app, db, BlogPost, Book
from datetime import datetime

def add_sample_data():
    with app.app_context():
        # Add sample blog posts if they don't exist
        if not BlogPost.query.first():
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
            
            print("Added sample blog posts!")

        # Add sample books if they don't exist
        if not Book.query.first():
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
            
            print("Added sample books!")

        db.session.commit()
        print("Sample data added successfully!")

if __name__ == '__main__':
    add_sample_data()
