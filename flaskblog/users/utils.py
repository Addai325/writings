import os
import secrets
from flask import url_for, current_app
from PIL import Image
from flaskblog import mail
from flask_mail import Message



def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _,p_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + p_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn 


def send_reset_email(user):
    token = user.get_request_reset()
    msg = Message('Reset Request Password', sender='noreply325nr@gmail.com', recipients=[user.email])
    msg.body = f''' Follow the link to reset your password
    
{url_for('users.reset_token', token=token, _external=True)}

If this was not you, please ignore
    
    '''
    mail.send(msg)
