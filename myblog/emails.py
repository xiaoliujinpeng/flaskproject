from flask import url_for
from flask import current_app
from flask_mail import Message
from myblog.extensions import mail
from threading import Thread

def _send_async_mail(app,message):
    with app.app_context():
        mail.send(message)

def send_mail(subject, to, html):
    app=current_app._get_current_object()
    message=Message(subject,recipients=[to],html=html)
    thr=Thread(target=_send_async_mail,args=[app,message])
    thr.start()
    return thr

def send_new_comment_email(post):
    post_url=url_for('blog.show_post',post_id=post.id, _external=True)+'#comments'
    send_mail(subject='New comment',to=current_app.config['BLUELOG_ADMIN_EMAIL'],
              html='sss'
              )

def send_new_reply_email(comment):
    post_url=url_for('blog.show_post',post_id=comment.post_id,_external=True)+'#comments'
    send_mail(subject='New reply',to=comment.email,html='待补充')
