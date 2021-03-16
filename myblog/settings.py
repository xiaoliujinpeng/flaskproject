import os
import sys
basedir=os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
WIN=sys.platform.startswith('win')
if WIN:
    prefix='sqlite:///'
else:
    prefix='sqlite:////'


class Operations():
    CONFIRM="confirm"
    RESET_PASSWORD="reset-password"
    CHANGE_EMAIL="change-email"
class BaseConfig(object):
    SECRET_KEY=os.getenv('SECRET_KEY',"no secret_key")
    DEBUG_TB_INTERCEPT_REDIRECTS=False
    
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SQLALCHEMY_RECORD_QUERIES=True

    CKEDITOR_ENABLE_CSRF=True
    CKEDITOR_FILE_UPLOADER='admin.upload_image'

    MAIL_SERVER=os.getenv('MAIL_SERVER')
    MAIL_PORT=465
    MAIL_USE_SSL=True
    MAIL_PASSWORD=os.getenv('MAIL_PASSWORD')
    MAIL_USERNAME=os.getenv('MAIL_USERNAME')
    MAIL_DEFAULT_SENDER=('Admin',MAIL_USERNAME)
    MAIL_SUBJECT_PREFIX = '[Blog]'

    BLUELOG_EMAIL=os.getenv('BLUELOG_EMAIL')
    BLUELOG_POST_PER_PAGE=10
    BLUELOG_MANAGE_POST_PER_PAGE=15
    BLUELOG_COMMENT_PER_PAGE=15

    BLUELOG_THEMES={'perfect_blue':'Perfect Blue','black_swan':'Black Swan',"cerulean":"蔚蓝","superhero":"Superhero","sketchy":"素描"}
    BLUELOG_SLOW_QUERY_THRESHOLD=1

    BLUELOG_UPLOAD_PATH = os.path.join(basedir, 'uploads')
    BLUELOG_ALLOWED_IMAGE_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']

    # 文件上传dropzone的设置
    DROPZONE_ALLOWED_FILE_CUSTOM=True
    DROPZONE_ALLOWED_FILE_TYPE="image/*,audio/*,video/*,text/*,application/*,.md"
    DROPZONE_MAX_FILE_SIZE=100
    DROPZONE_DEFAULT_MESSAGE="点击上传文件"
    DROPZONE_INVALID_FILE_TYPE="你不能上传这种类型的文件"
    DROPZONE_FILE_TOO_BIG="文件过大:{{filesize}}.最大值允许{{maxFileSize}}MB"
    DROPZONE_BROWSER_UNSUPPORTED="你的游览器不支持"
    DROPZONE_MAX_FILE_EXCEED="不能再上传文件"
    DROPZONE_ENABLE_CSRF=True
    DROPZONE_UPLOAD_MULTIPLE=True
    DROPZONE_PARALLEL_UPLOADS=2

class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI=prefix + os.path.join(basedir,'data-dev.db')


class TestingConfig(BaseConfig):
    TESTING=True
    WTF_CSRF_ENABLED=False
    SQLALCHEMY_DATABASE_URI='sqlite:////:memory:'

class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_URL',prefix+os.path.join(basedir, 'data.db'))


config={
    "development":DevelopmentConfig,
    "testing":TestingConfig,
    "production":ProductionConfig
}

