from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators
from wtforms.validators import DataRequired, Length, ValidationError, EqualTo
from urllib.parse import urlparse, urljoin


app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Конфигурация MySQL (остаётся как в предыдущей части)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/flask_db7'
db = SQLAlchemy(app)

# Инициализация Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'


# Модель пользователя с наследованием UserMixin
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)


# Загрузчик пользователя (обязателен для Flask-Login)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Форма регистрации
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=4, max=20)
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=6)
    ])
    confirm_password = PasswordField('Confirm Password', validators=[  # Фикс здесь
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])  # Закрывающая скобка была пропущена
    submit = SubmitField('Sign Up')


# Форма авторизации
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        validators.EqualTo('password', message='Passwords must match')
    ])

# Проверки
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    db.session.rollback()
    return render_template('500.html'), 500

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


# Маршруты
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Account created!', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            if not is_safe_url(next_page):
                next_page = None
            return redirect(next_page) if next_page else redirect(url_for('profile'))
        else:
            flash('Login failed. Check username and password', 'danger')

    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)


# Остальные маршруты остаются без изменений
# Создаём таблицы при первом запросе
# Вместо этого используйте явное создание таблиц в контексте приложения:
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)