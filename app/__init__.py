from flask import Flask, current_app, request
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_babel import Babel
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
from flask_babel import lazy_gettext as _l

# Flask-SQLALCHEMY and Flask-Migrate
db = SQLAlchemy()
migrate = Migrate()
# Login
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = _l('请登录后再访问该页面。')
mail = Mail()  # Email support
bootstrap = Bootstrap()  # Bootstrap
moment = Moment()  # Date and Time
babel = Babel()  # I18n and L10n


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    babel.init_app(app)

    # error blueprint
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    # auth blueprint
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # main blueprint
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    # api blueprint
    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    if not app.debug and not app.testing:
        # Sending errors by Email
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'],
                        app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                # fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                fromaddr='youzj@163.com',
                toaddrs=app.config['ADMINS'], subject='MINI Failure',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

        # Logging to file
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/mini.log',
                                           maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('<MINI>开始运行...')

    return app


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(
        current_app.config['LANGUAGES']) or 'zh_cn'


from app import models
