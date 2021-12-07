import os
pathURI_allow = ['/static','/login','/forget']
regexPath = '^(%s)'%'|'.join(pathURI_allow)

pathURI_Admin = ['/admin','/staff','/api/editStaff','/api/addStaff','/api/addClass']
regexPathAdmin = '^(%s)'%'|'.join(pathURI_Admin)

class Config():
    SECRET_KEY = os.urandom(50).hex()

class Mail():
    MAIL_SERVER ='smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'managatoonltw@gmail.com'
    MAIL_PASSWORD = 'gbforhxxewhjcmis'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True    

class ReCaptcha():
    RECAPTCHA_USE_SSL= False
    RECAPTCHA_PUBLIC_KEY = '6Le8E3MdAAAAAIvYyBWqZ6sjL_7uvaX5uWqwWlsc'
    RECAPTCHA_PRIVATE_KEY  = '6Le8E3MdAAAAAG5ZxKl8qJEtYWWDA1rxe0-tpvy_'
    RECAPTCHA_DATA_ATTRS = {'theme': 'light'}