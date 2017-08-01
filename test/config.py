# Toggle debug logging.
DEBUG = True

# SMTP server setup for sending moderation requests.
SMTP_SERVER = 'smtp.example.com'
SMTP_PORT = 465
SMTP_LOGIN = 'test@example.com'
SMTP_PASSWD = 'password'

# Email address used as from address in the moderation request.
FROM_EMAIL = 'ssg-commnts@example.com'
# Email to send moderation request to.
TO_EAMIL = 'webmaster@example.com'

# Path of messages waiting to be moderated.
QUEUED_MSG_PATH = 'qmsg'
# Path of the moderated messages.
MODDED_MSG_PATH = 'mmsg'

#APPLICATION_ROOT = '/ssg_comments'

PROPAGATE_EXCEPTIONS = True

SERVER_NAME = 'localhost:8080'
