import os
from flask import Flask,render_template,request
from myblog.blueprints.admin import admin_bp
from myblog.blueprints.blog import blog_bp
from myblog.blueprints.auth import auth_bp
from myblog.settings import config
from myblog.extensions import db,mail,bootstrap,moment,ckeditor,login_manager,csrf,migrate,dropzone
from myblog.models import Admin,Category,Post,Link
from flask_wtf.csrf import CSRFError
from flask_login import current_user
from flask_sqlalchemy import get_debug_queries
from logging.handlers import SMTPHandler, RotatingFileHandler
from myblog.commands import register_commands,register_shell_context

import logging

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

def creat_app(config_name=None):
    if config_name==None:
        config_name = os.getenv('FLASK_ENV', 'development')
    app = Flask('myblog')
    app.config.from_object(config[config_name])


    register_extensions(app)
    register_blueprint(app)
    register_commands(app)
    register_errors(app)
    register_shell_context(app)
    register_template_context(app)
    register_request_handlers(app)
    register_logging(app)


    return app

def register_blueprint(app):
    app.register_blueprint(blog_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp,url_prefix='/admin')

def register_extensions(app):
    db.init_app(app)
    moment.init_app(app)
    ckeditor.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    dropzone.init_app(app)
    migrate.init_app(app,db)

def register_logging(app):
    class RequestFormatter(logging.Formatter):

        def format(self, record):
            record.url = request.url
            record.remote_addr = request.remote_addr
            return super(RequestFormatter, self).format(record)

    request_formatter = RequestFormatter(
        '[%(asctime)s] %(remote_addr)s requested %(url)s\n'
        '%(levelname)s in %(module)s: %(message)s'
    )

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    file_handler = RotatingFileHandler(os.path.join(basedir, 'logs/bluelog.log'),
                                       maxBytes=10 * 1024 * 1024, backupCount=10)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    mail_handler = SMTPHandler(
        mailhost=app.config['MAIL_SERVER'],
        fromaddr=app.config['MAIL_USERNAME'],
        toaddrs=['ADMIN_EMAIL'],
        subject='Bluelog Application Error',
        credentials=(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD']))
    mail_handler.setLevel(logging.ERROR)
    mail_handler.setFormatter(request_formatter)

    if not app.debug:
        app.logger.addHandler(mail_handler)
        app.logger.addHandler(file_handler)



def register_errors(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html'),400
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'),404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'),500
    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        return render_template('errors/400.html',descripiton=e.descripition),400






def register_template_context(app):
    @app.context_processor
    def make_template_context():
        admin=Admin.query.first()
        categories=Category.query.order_by(Category.name).all()
        links=Link.query.order_by(Link.name).all()

        return dict(
            admin=admin,categories=categories,
            links=links
        )

def register_request_handlers(app):
    @app.after_request
    def query_profiler(response):
        for q in get_debug_queries():
            if q.duration >= app.config['BLUELOG_SLOW_QUERY_THRESHOLD']:
                app.logger.warning(
                    'Slow query: Duration: %fs\n Context: %s\nQuery: %s\n '
                    % (q.duration, q.context, q.statement)
                )
        return response


myapp=creat_app()