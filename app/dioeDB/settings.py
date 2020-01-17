"""
Django settings for dioeDB project.

Generated by 'django-admin startproject' using Django 1.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import random, string

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#################################################################################################################
# Umgebungsvariablen:																							#
#################################################################################################################
# DIOEDB_DEBUG = "False"									(Default: "True")									#
# DIOEDB_SECRET_KEY = Benutze: https://www.miniwebtool.com/django-secret-key-generator/							#
# DIOEDB_STATIC_ROOT = "/var/www/example.com/static/"		(Default: None)										#
# DIOEDB_STATIC_URL = "/static/"							(Default: "/static/")								#
# DIOEDB_AUDIO_URL = "/private-media/"						(Default: "/private-media/")						#
# django-private-storage:																						#
# DIOEDB_PRIVATE_STORAGE_ROOT = '/'							(Default: '/')										#
# DIOEDB_PRIVATE_STORAGE_AUTH_FUNCTION = 'private_storage.permissions.allow_authenticated'						#
# DIOEDB_PRIVATE_STORAGE_SERVER = 'nginx'					(Default: 'django')									#
# DIOEDB_PRIVATE_STORAGE_INTERNAL_URL = '/private-x-accel-redirect/'											#
# Datenbank:																									#
# DIOEDB_DB="django.db.backends.postgresql"					(Default: "django.db.backends.sqlite3")				#
# DIOEDB_DB_NAME="PersonenDB"								(Default: os.path.join(BASE_DIR, 'db.sqlite3'))		#
# DIOEDB_DB_USER="user"										(Default: None)										#
# DIOEDB_DB_PASSWORD="passwort"								(Default: None)										#
# DIOEDB_DB_HOST="postgresql://localhost"					(Default: None)										#
# DIOEDB_DB_PORT="5433"										(Default: None)										#
#################################################################################################################

LOGIN_URL = 'dioedb_login'
LOGOUT_URL = 'dioedb_logout'
LOGIN_REDIRECT_URL = 'Startseite:start'
CRISPY_TEMPLATE_PACK = 'bootstrap3'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '5@l-y9u7y_7plh(7xq2u-_ilgushpm*&^7&j0%6o-(b0&d31bj'

# SECURITY WARNING: don't run with debug turned on in production!
if 'DIOEDB_DEBUG' in os.environ and (os.environ['DIOEDB_DEBUG'] == 'False' or os.environ['DIOEDB_DEBUG'] is False):
	DEBUG = False
else:
	DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]', '.dioe.at']

SESSION_COOKIE_HTTPONLY = False
CSRF_COOKIE_HTTPONLY = False

ALLOWED_SETTINGS_IN_TEMPLATES = ("AUDIO_URL", "CACH_RANDOM")

CACH_RANDOM = ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for i in range(8))

DIOEDB_APPLIST = ['PersonenDB', 'KorpusDB', 'AnnotationsDB', 'mioeDB']
DIOEDB_MAXVERWEISE = 50

# Application definition

INSTALLED_APPS = (
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'corsheaders',
	'crispy_forms',
	'private_storage',
	'Startseite',
	'PersonenDB',
	'KorpusDB',
	'AnnotationsDB',
	'DB',
	'mioeDB'
)

MIDDLEWARE_CLASSES = (
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
	'django.middleware.security.SecurityMiddleware',
	'corsheaders.middleware.CorsMiddleware',
	'django.middleware.common.CommonMiddleware',
	'DB.middleware.SetLastVisitMiddleware',
)

# CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = ('127.0.0.1:8000', 'localhost:8080', 'transcribe.dioe.at', 'dioedb.dioe.at')
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = (
	'DELETE',
	'GET',
	'OPTIONS',
	'PATCH',
	'POST',
	'PUT',
	'HEAD'
)

CORS_ALLOW_HEADERS = (
	'accept',
	'accept-encoding',
	'authorization',
	'content-type',
	'dnt',
	'origin',
	'user-agent',
	'x-csrftoken',
	'x-requested-with',
	'range'
)

ROOT_URLCONF = 'dioeDB.urls'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [os.path.join(BASE_DIR, 'dioeDB', 'templates'), os.path.join(BASE_DIR, 'Startseite', 'templates'), os.path.join(BASE_DIR, 'DB', 'templates'), os.path.join(BASE_DIR, 'KorpusDB', 'templates'), os.path.join(BASE_DIR, 'mioeDB', 'templates')],
		'APP_DIRS': True,
		'OPTIONS': {
			'context_processors': [
				'django.template.context_processors.debug',
				'django.template.context_processors.request',
				'django.contrib.auth.context_processors.auth',
				'django.contrib.messages.context_processors.messages',
			],
		},
	},
]

WSGI_APPLICATION = 'dioeDB.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
	}
}

# Umgebungsvariablen:
if 'DIOEDB_SECRET_KEY' in os.environ:
	SECRET_KEY = os.environ['DIOEDB_SECRET_KEY']

if 'DIOEDB_DB' in os.environ and os.environ['DIOEDB_DB']:
	DATABASES['default']['ENGINE'] = os.environ['DIOEDB_DB']
	if 'DIOEDB_DB_NAME' in os.environ:
		DATABASES['default']['DBNAME'] = os.environ['DIOEDB_DB_NAME']
		DATABASES['default']['NAME'] = os.environ['DIOEDB_DB_NAME']
	if 'DIOEDB_DB_USER' in os.environ:
		DATABASES['default']['USER'] = os.environ['DIOEDB_DB_USER']
	if 'DIOEDB_DB_PASSWORD' in os.environ:
		DATABASES['default']['PASSWORD'] = os.environ['DIOEDB_DB_PASSWORD']
	if 'DIOEDB_DB_HOST' in os.environ:
		DATABASES['default']['HOST'] = os.environ['DIOEDB_DB_HOST']
	if 'DIOEDB_DB_PORT' in os.environ:
		DATABASES['default']['PORT'] = os.environ['DIOEDB_DB_PORT']

# print(DATABASES)

FILE_UPLOAD_PERMISSIONS = 0o644

PRIVATE_STORAGE_ROOT = '/'
PRIVATE_STORAGE_AUTH_FUNCTION = 'private_storage.permissions.allow_authenticated'
PRIVATE_STORAGE_SERVER = 'django'
PRIVATE_STORAGE_INTERNAL_URL = '/private-x-accel-redirect/'
if 'DIOEDB_PRIVATE_STORAGE_ROOT' in os.environ:
	PRIVATE_STORAGE_ROOT = os.environ['DIOEDB_PRIVATE_STORAGE_ROOT']
if 'DIOEDB_PRIVATE_STORAGE_AUTH_FUNCTION' in os.environ:
	PRIVATE_STORAGE_AUTH_FUNCTION = os.environ['DIOEDB_PRIVATE_STORAGE_AUTH_FUNCTION']
if 'DIOEDB_PRIVATE_STORAGE_SERVER' in os.environ:
	PRIVATE_STORAGE_SERVER = os.environ['DIOEDB_PRIVATE_STORAGE_SERVER']
if 'DIOEDB_PRIVATE_STORAGE_INTERNAL_URL' in os.environ:
	PRIVATE_STORAGE_INTERNAL_URL = os.environ['DIOEDB_PRIVATE_STORAGE_INTERNAL_URL']

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'de-DE'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = False
USE_THOUSAND_SEPARATOR = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
AUDIO_URL = '/private-media/'

# Umgebungsvariablen:
if 'DIOEDB_STATIC_ROOT' in os.environ and os.environ['DIOEDB_STATIC_ROOT']:
	STATIC_ROOT = os.environ['DIOEDB_STATIC_ROOT']
if 'DIOEDB_STATIC_URL' in os.environ and os.environ['DIOEDB_STATIC_URL']:
	STATIC_URL = os.environ['DIOEDB_STATIC_URL']
if 'DIOEDB_AUDIO_URL' in os.environ and os.environ['DIOEDB_AUDIO_URL']:
	AUDIO_URL = os.environ['DIOEDB_AUDIO_URL']

STATICFILES_DIRS = (
	os.path.join(BASE_DIR, 'dioeDB', 'static'),
	os.path.join(BASE_DIR, 'KorpusDB', 'static'),
	os.path.join(BASE_DIR, 'DB', 'static'),
	os.path.join(BASE_DIR, 'mioeDB', 'static'),
)
