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

# Get the directory where app.py is located
basedir = os.path.abspath(os.path.dirname(__file__))
# Create data directory in the same folder as app.py
data_dir = os.path.join(basedir, 'data')
try:
    os.makedirs(data_dir, exist_ok=True)
    app.logger.info(f"Data directory created at: {data_dir}")
except Exception as e:
    app.logger.error(f"Error creating data directory: {str(e)}")
    raise

app = Flask(__name__)
app.logger.info("Flask app created")

# Enable debug mode
app.config['DEBUG'] = True
app.config['PROPAGATE_EXCEPTIONS'] = True

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')
# Use relative path for SQLite database
db_path = os.path.join(data_dir, "site.db")
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.logger.info(f"Using database at: {db_path}")

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@app.errorhandler(500)
def internal_error(error):
    app.logger.error(f'Server Error: {error}')
    app.logger.error(traceback.format_exc())
    return render_template('error.html', error=error), 500

@app.errorhandler(Exception)
def handle_exception(e):
    app.logger.error(f'Unhandled Exception: {e}')
    app.logger.error(traceback.format_exc())
    return render_template('error.html', error=str(e)), 500

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    description = db.Column(db.String(500))

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(200), nullable=False)
    notes = db.Column(db.Text)
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.get(int(user_id))
    except Exception as e:
        app.logger.error(f'Error loading user: {e}')
        return None

@app.route('/')
def index():
    try:
        blog_posts = BlogPost.query.order_by(BlogPost.date_posted.desc()).all()
        books = Book.query.order_by(Book.date_added.desc()).all()
        return render_template('index.html', blog_posts=blog_posts, books=books)
    except Exception as e:
        app.logger.error(f'Error rendering index page: {e}')
        return render_template('error.html', error=str(e)), 500

@app.route('/blog/<int:id>')
def blog_post(id):
    try:
        post = BlogPost.query.get_or_404(id)
        return render_template('blog_post.html', post=post)
    except Exception as e:
        app.logger.error(f'Error rendering blog post page: {e}')
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
        app.logger.error(f'Error rendering login page: {e}')
        return render_template('error.html', error=str(e)), 500

@app.route('/logout')
@login_required
def logout():
    try:
        logout_user()
        return redirect(url_for('index'))
    except Exception as e:
        app.logger.error(f'Error logging out: {e}')
        return render_template('error.html', error=str(e)), 500

@app.route('/admin')
@login_required
def admin():
    try:
        blog_posts = BlogPost.query.order_by(BlogPost.date_posted.desc()).all()
        books = Book.query.order_by(Book.date_added.desc()).all()
        return render_template('admin.html', blog_posts=blog_posts, books=books)
    except Exception as e:
        app.logger.error(f'Error rendering admin page: {e}')
        return render_template('error.html', error=str(e)), 500

@app.route('/blog/new', methods=['GET', 'POST'])
@login_required
def new_blog():
    try:
        if request.method == 'POST':
            post = BlogPost(
                title=request.form['title'],
                content=request.form['content'],
                description=request.form['description']
            )
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('admin'))
        return render_template('blog_form.html')
    except Exception as e:
        app.logger.error(f'Error creating new blog post: {e}')
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
            db.session.commit()
            return redirect(url_for('admin'))
        return render_template('blog_form.html', post=post)
    except Exception as e:
        app.logger.error(f'Error editing blog post: {e}')
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
        app.logger.error(f'Error deleting blog post: {e}')
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
        app.logger.error(f'Error creating new book: {e}')
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
        app.logger.error(f'Error editing book: {e}')
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
        app.logger.error(f'Error deleting book: {e}')
        return render_template('error.html', error=str(e)), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Create admin user if it doesn't exist
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
    app.run(host='0.0.0.0', port=8000, debug=True)
