from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
import logging
import sys
import traceback

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
)
logger = logging.getLogger(__name__)

# Create Flask app first
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['PROPAGATE_EXCEPTIONS'] = True

# Get the directory where app.py is located
basedir = os.path.abspath(os.path.dirname(__file__))
# Create data directory in the same folder as app.py
data_dir = os.path.join(basedir, 'data')
try:
    os.makedirs(data_dir, exist_ok=True)
    logger.info(f"Data directory created at: {data_dir}")
except Exception as e:
    logger.error(f"Error creating data directory: {str(e)}")
    raise

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')
# Use relative path for SQLite database
db_path = os.path.join(data_dir, "site.db")
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

logger.info(f"Using database at: {db_path}")

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Define models first
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class BlogPost(db.Model):
    __tablename__ = 'blog_posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    description = db.Column(db.String(200))
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    notes = db.Column(db.Text)
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.get(int(user_id))
    except Exception as e:
        logger.error(f'Error loading user: {e}')
        return None

# Then define initialization function
def init_db():
    """Initialize the database and add sample data."""
    with app.app_context():
        try:
            logger.info("Creating database tables...")
            db.create_all()
            logger.info("Database tables created successfully")

            # Check if tables exist and log their names
            inspector = db.inspect(db.engine)
            table_names = inspector.get_table_names()
            logger.info(f"Existing tables in database: {table_names}")

            # Check if admin user exists
            if not User.query.filter_by(username='admin').first():
                logger.info("Creating admin user...")
                admin_user = User(
                    username='admin',
                    password_hash=generate_password_hash('admin', method='pbkdf2:sha256')
                )
                db.session.add(admin_user)
                db.session.commit()
                logger.info("Admin user created successfully")

            # Add sample blog posts if none exist
            if not BlogPost.query.first():
                logger.info("Adding sample blog posts...")
                sample_posts = [
                    BlogPost(
                        title='Welcome to My Blog',
                        content='This is my first blog post...',
                        description='An introduction to my blog'
                    ),
                    BlogPost(
                        title='The Future of Economic Policy in an AI-Driven World',
                        content='As artificial intelligence continues to reshape our economy...',
                        description='Exploring how AI will influence economic policy making'
                    ),
                    BlogPost(
                        title='Game Theory and Machine Learning',
                        content='The intersection of game theory and machine learning...',
                        description='Understanding strategic decision making in AI systems'
                    ),
                    BlogPost(
                        title='Behavioral Economics in the Age of AI',
                        content='How do cognitive biases affect our interactions with AI...',
                        description='Examining human behavior in AI-integrated markets'
                    ),
                    BlogPost(
                        title='The Economics of Large Language Models',
                        content='Analyzing the economic implications of LLMs...',
                        description='Cost-benefit analysis of developing and deploying LLMs'
                    ),
                    BlogPost(
                        title='Market Design for AI Systems',
                        content='Principles for designing efficient AI marketplaces...',
                        description='Creating sustainable markets for AI resources'
                    ),
                    BlogPost(
                        title='AI and Labor Market Transformation',
                        content='Understanding how AI is reshaping employment...',
                        description='Analysis of AI\'s impact on workforce dynamics'
                    )
                ]
                db.session.add_all(sample_posts)
                db.session.commit()
                logger.info("Sample blog posts added successfully")

            # Add sample books if none exist
            if not Book.query.first():
                logger.info("Adding sample books...")
                sample_books = [
                    Book(
                        title='The Economics of AI',
                        author='Sample Author',
                        notes='A fascinating exploration of AI economics'
                    ),
                    Book(
                        title='Superintelligence: Paths, Dangers, Strategies',
                        author='Nick Bostrom',
                        notes='A comprehensive analysis of potential AI development trajectories and their implications'
                    ),
                    Book(
                        title='The Economics of Artificial Intelligence',
                        author='Ajay Agrawal, Joshua Gans, Avi Goldfarb',
                        notes='Exploring the economic principles governing AI adoption and impact'
                    ),
                    Book(
                        title='Human Compatible: AI and the Problem of Control',
                        author='Stuart Russell',
                        notes='Insights into designing AI systems that are aligned with human values'
                    ),
                    Book(
                        title='Prediction Machines: The Simple Economics of Artificial Intelligence',
                        author='Ajay Agrawal, Joshua Gans, Avi Goldfarb',
                        notes='Understanding AI through the lens of economic decision-making'
                    ),
                    Book(
                        title='The Alignment Problem',
                        author='Brian Christian',
                        notes='Examining the challenges of aligning AI systems with human values and objectives'
                    ),
                    Book(
                        title='Life 3.0: Being Human in the Age of Artificial Intelligence',
                        author='Max Tegmark',
                        notes='Exploring the future of life in a world transformed by AI'
                    )
                ]
                db.session.add_all(sample_books)
                db.session.commit()
                logger.info("Sample books added successfully")

        except Exception as e:
            logger.error(f"Error initializing database: {str(e)}")
            logger.error(traceback.format_exc())
            raise

# Initialize database when the application starts
with app.app_context():
    init_db()

# Then define routes
@app.route('/')
def index():
    try:
        logger.info("Fetching blog posts and books for index page...")
        blog_posts = BlogPost.query.order_by(BlogPost.date_posted.desc()).all()
        books = Book.query.order_by(Book.date_added.desc()).all()
        return render_template('index.html', blog_posts=blog_posts, books=books)
    except Exception as e:
        logger.error(f'Error rendering index page: {str(e)}')
        logger.error(traceback.format_exc())
        return render_template('error.html', error=str(e)), 500

@app.route('/blog')
def blog():
    """Route for the full blog page."""
    posts = BlogPost.query.order_by(BlogPost.date_posted.desc()).all()
    return render_template('blog.html', posts=posts)

@app.route('/blog/<int:id>')
def blog_post(id):
    try:
        post = BlogPost.query.get_or_404(id)
        return render_template('blog_post.html', post=post)
    except Exception as e:
        logger.error(f'Error rendering blog post page: {e}')
        return render_template('error.html', error=str(e)), 500

@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        if request.method == 'POST':
            user = User.query.filter_by(username=request.form['username']).first()
            if user and user.check_password(request.form['password']):
                login_user(user)
                return redirect(url_for('admin'))
            flash('Invalid username or password')
        return render_template('login.html')
    except Exception as e:
        logger.error(f'Error rendering login page: {e}')
        return render_template('error.html', error=str(e)), 500

@app.route('/logout')
@login_required
def logout():
    try:
        logout_user()
        return redirect(url_for('index'))
    except Exception as e:
        logger.error(f'Error logging out: {e}')
        return render_template('error.html', error=str(e)), 500

@app.route('/admin')
@login_required
def admin():
    try:
        blog_posts = BlogPost.query.order_by(BlogPost.date_posted.desc()).all()
        books = Book.query.order_by(Book.date_added.desc()).all()
        return render_template('admin.html', blog_posts=blog_posts, books=books)
    except Exception as e:
        logger.error(f'Error rendering admin page: {e}')
        return render_template('error.html', error=str(e)), 500

@app.route('/blog/new', methods=['GET', 'POST'])
@login_required
def new_blog():
    try:
        if request.method == 'POST':
            date_posted = datetime.strptime(request.form['date_posted'], '%Y-%m-%dT%H:%M') if request.form['date_posted'] else datetime.utcnow()
            post = BlogPost(
                title=request.form['title'],
                content=request.form['content'],
                description=request.form['description'],
                date_posted=date_posted
            )
            db.session.add(post)
            db.session.commit()
            logger.info(f"Created new blog post: {post.title} with date {date_posted}")
            return redirect(url_for('admin'))
        return render_template('blog_form.html')
    except Exception as e:
        logger.error(f'Error creating new blog post: {e}')
        logger.error(traceback.format_exc())
        return render_template('error.html', error=str(e)), 500

@app.route('/blog/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_blog(id):
    try:
        post = BlogPost.query.get_or_404(id)
        if request.method == 'POST':
            post.title = request.form['title']
            post.content = request.form['content']
            post.description = request.form['description']
            if request.form['date_posted']:
                post.date_posted = datetime.strptime(request.form['date_posted'], '%Y-%m-%dT%H:%M')
            db.session.commit()
            logger.info(f"Updated blog post: {post.title} with date {post.date_posted}")
            return redirect(url_for('admin'))
        return render_template('blog_form.html', post=post)
    except Exception as e:
        logger.error(f'Error editing blog post: {e}')
        logger.error(traceback.format_exc())
        return render_template('error.html', error=str(e)), 500

@app.route('/blog/delete/<int:id>')
@login_required
def delete_blog(id):
    try:
        post = BlogPost.query.get_or_404(id)
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for('admin'))
    except Exception as e:
        logger.error(f'Error deleting blog post: {e}')
        return render_template('error.html', error=str(e)), 500

@app.route('/book/new', methods=['GET', 'POST'])
@login_required
def new_book():
    try:
        if request.method == 'POST':
            book = Book(
                title=request.form['title'],
                author=request.form['author'],
                notes=request.form['notes']
            )
            db.session.add(book)
            db.session.commit()
            return redirect(url_for('admin'))
        return render_template('book_form.html')
    except Exception as e:
        logger.error(f'Error creating new book: {e}')
        return render_template('error.html', error=str(e)), 500

@app.route('/book/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_book(id):
    try:
        book = Book.query.get_or_404(id)
        if request.method == 'POST':
            book.title = request.form['title']
            book.author = request.form['author']
            book.notes = request.form['notes']
            db.session.commit()
            return redirect(url_for('admin'))
        return render_template('book_form.html', book=book)
    except Exception as e:
        logger.error(f'Error editing book: {e}')
        return render_template('error.html', error=str(e)), 500

@app.route('/book/delete/<int:id>')
@login_required
def delete_book(id):
    try:
        book = Book.query.get_or_404(id)
        db.session.delete(book)
        db.session.commit()
        return redirect(url_for('admin'))
    except Exception as e:
        logger.error(f'Error deleting book: {e}')
        return render_template('error.html', error=str(e)), 500

@app.route('/books')
def books():
    """Route for the full bookshelf page."""
    try:
        logger.info("Fetching all books from database...")
        books = Book.query.order_by(Book.date_added.desc()).all()
        logger.info(f"Successfully fetched {len(books)} books")
        return render_template('books.html', books=books)
    except Exception as e:
        logger.error(f"Error in books route: {str(e)}")
        logger.error(traceback.format_exc())  # Add full traceback
        return render_template('error.html', error="Could not load books at this time.")

@app.errorhandler(500)
def internal_error(error):
    logger.error(f'Server Error: {error}')
    logger.error(traceback.format_exc())
    return render_template('error.html', error=error), 500

@app.errorhandler(Exception)
def handle_exception(e):
    logger.error(f'Unhandled Exception: {e}')
    logger.error(traceback.format_exc())
    return render_template('error.html', error=str(e)), 500

if __name__ == '__main__':
    app.run(debug=True)
