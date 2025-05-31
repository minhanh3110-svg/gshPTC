from flask import Flask, request, g, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging
from logging.handlers import RotatingFileHandler
import os
import sys
from config import Config
from flask_babel import Babel

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
mail = Mail()
limiter = Limiter(key_func=get_remote_address)
babel = Babel()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)
    limiter.init_app(app)
    babel.init_app(app)

    # Setup login manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Vui lòng đăng nhập để truy cập trang này.'
    login_manager.login_message_category = 'info'

    # Setup logging
    if not os.path.exists('logs'):
        os.mkdir('logs')
    
    # Configure logging to use UTF-8
    logging.basicConfig(encoding='utf-8')
    file_handler = RotatingFileHandler('logs/gshptc.log', maxBytes=10240, backupCount=10, encoding='utf-8')
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    
    # Add console handler for development
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    console_handler.setLevel(logging.INFO)
    
    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('GSHPTC startup')

    # Register blueprints
    from .routes.main import bp as main_bp
    app.register_blueprint(main_bp)

    from .routes.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    # User loader
    from .models import User
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    # Babel locale selector
    @babel.localeselector
    def get_locale():
        # Try to get language from URL parameters
        lang = request.args.get('lang')
        if lang in app.config['LANGUAGES']:
            session['lang'] = lang
            return lang
        
        # Try to get language from session
        if 'lang' in session:
            return session['lang']
        
        # Try to get language from user preferences
        if hasattr(g, 'lang'):
            return g.lang
        
        # Get best matching language from headers
        return request.accept_languages.best_match(app.config['LANGUAGES'])

    if not app.debug and not app.testing:
        if app.config['MAIL_SERVER']:
            import logging
            from logging.handlers import SMTPHandler
            credentials = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                credentials = (app.config['MAIL_USERNAME'], 
                             app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], subject='GSHPTC Failure',
                credentials=credentials, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

    return app
