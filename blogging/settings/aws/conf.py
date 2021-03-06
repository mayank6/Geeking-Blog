import datetime,os

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_FILE_EXPIRE = 200
AWS_PRELOAD_METADATA = True
AWS_QUERYSTRING_AUTH = False

DEFAULT_FILE_STORAGE = 'blogging.settings.aws.utils.MediaRootS3BotoStorage'
STATICFILES_STORAGE = 'blogging.settings.aws.utils.StaticRootS3BotoStorage'
AWS_STORAGE_BUCKET_NAME = 'geekingblog'
S3DIRECT_REGION = 'ap-south-1'
S3_URL = '//geekingblog.s3.amazonaws.com/'
MEDIA_URL = '//geekingblog.s3.amazonaws.com/media/' 
MEDIA_ROOT = MEDIA_URL
STATIC_URL = S3_URL + 'static/'
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

two_months = datetime.timedelta(days=61)
date_two_months_later = datetime.date.today() + two_months
expires = date_two_months_later.strftime("%A, %d %B %Y 20:00:00 GMT")

AWS_HEADERS = { 
    'Expires': expires,
    'Cache-Control': 'max-age=%d' % (int(two_months.total_seconds()), ),
}

AWS_DEFAULT_ACL = None
AWS_S3_SIGNATURE_VERSION = 's3v4'