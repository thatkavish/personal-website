from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

# Get the directory where app.py is located
basedir = os.path.abspath(os.path.dirname(__file__))
# Create data directory in the same folder as app.py
data_dir = os.path.join(basedir, 'data')
os.makedirs(data_dir, exist_ok=True)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')
# Use relative path for SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', f'sqlite:///{os.path.join(data_dir, "site.db")}')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

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
    return User.query.get(int(user_id))

@app.route('/')
def index():
    blog_posts = BlogPost.query.order_by(BlogPost.date_posted.desc()).all()
    books = Book.query.order_by(Book.date_added.desc()).all()
    return render_template('index.html', blog_posts=blog_posts, books=books)

@app.route('/blog/<int:id>')
def blog_post(id):
    post = BlogPost.query.get_or_404(id)
    return render_template('blog_post.html', post=post)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.check_password(request.form['password']):
            login_user(user)
            return redirect(url_for('admin'))
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/admin')
@login_required
def admin():
    blog_posts = BlogPost.query.order_by(BlogPost.date_posted.desc()).all()
    books = Book.query.order_by(Book.date_added.desc()).all()
    return render_template('admin.html', blog_posts=blog_posts, books=books)

@app.route('/blog/new', methods=['GET', 'POST'])
@login_required
def new_blog():
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

@app.route('/blog/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_blog(id):
    post = BlogPost.query.get_or_404(id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        post.description = request.form['description']
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template('blog_form.html', post=post)

@app.route('/blog/delete/<int:id>')
@login_required
def delete_blog(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/book/new', methods=['GET', 'POST'])
@login_required
def new_book():
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

@app.route('/book/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_book(id):
    book = Book.query.get_or_404(id)
    if request.method == 'POST':
        book.title = request.form['title']
        book.author = request.form['author']
        book.notes = request.form['notes']
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template('book_form.html', book=book)

@app.route('/book/delete/<int:id>')
@login_required
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('admin'))

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
