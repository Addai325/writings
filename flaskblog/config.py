import os

class Config():
    SECRET_KEY ="bbc815aaf2ae896374431d7e66f1e8be"
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT =587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Omni3255??!!@localhost/thedb'
    # SQLALCHEMY_DATABASE_URI = "mysql://root:pSdtXdRTeLmfeHpJohajWCRAEWEHskmc@mysql.railway.internal:3306/railway"
    # SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://root:pSdtXdRTeLmfeHpJohajWCRAEWEHskmc@mysql.railway.internal:3306/railway"
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:pSdtXdRTeLmfeHpJohajWCRAEWEHskmc@autorack.proxy.rlwy.net:52095/railway"

