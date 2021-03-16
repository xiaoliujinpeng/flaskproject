import json
from myblog.extensions import db
from myblog.settings import Operations
#提供了多种用于对数据签名的辅助类
from itsdangerous import BadSignature,SignatureExpired
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


try:
    from urlparse import urlparse,urljoin
except ImportError:
    from urllib.parse import urlparse,urljoin

from flask import request,redirect,url_for,current_app

def is_safe_url(target):
    ref_url=urlparse(request.host_url)
    test_url=urlparse(urljoin(request.host_url,target))
    return test_url.scheme in ('http','https') and ref_url.netloc == test_url.netloc

def redirect_back(default='blog.index',**kwargs):
    for target in request.args.get('next'),request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default,**kwargs))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in current_app.config['BLUELOG_ALLOWED_IMAGE_EXTENSIONS']


def get_json(filename):
    f=open(filename,"r")
    return json.loads(f.read())


def generate_token(user,operation,expire_in=None,**kwargs):
    s=Serializer(current_app.config["SECRET_KEY"],expire_in)  ##使用和创建令牌时相同的密钥创建序列,expire_in设置过期时间默认3600s
    data={'id':user.id,'operation':operation}
    data.update(**kwargs)   ##将额外传入的关键字参数也保存道data中
    return s.dumps(data)


def validate_token(user,token,opreation,new_password=None,**kwargs):
    s=Serializer(current_app.config["SECRET_KEY"])   ##使用和创建令牌时相同的密钥创建序列

    try:
        data=s.loads(token)    ##加载token值提取出数据
    except (SignatureExpired,BadSignature):
        return False

    if opreation != data.get('operation') or user.id != data.get("id"):
        return False

    if opreation == Operations.CONFIRM:
        user.confirmed=True

    if opreation == Operations.RESET_PASSWORD:
        user.set_password(new_password)

    db.session.commit()
    return True