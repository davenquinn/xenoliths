
# Django settings for ctx_site project.
import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
	('Daven', 'accounts@davenquinn.com'),
)

#MANAGERS = ADMINS

DATABASES = {
	'default': {
		'ENGINE': 'django.contrib.gis.db.backends.postgis', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
		'NAME': 'xenoliths',                      # Or path to database file if using sqlite3.
		'USER': '',                      # Not used with sqlite3.
		'PASSWORD': '',                  # Not used with sqlite3.
		'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
		'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
	}
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Los_Angeles'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"

SITE_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)),"..")

# Location to store images
IMAGE_ROOT = os.path.join(SITE_DIR, '_images')
MEDIA_ROOT = os.path.join(SITE_DIR, '_media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(SITE_DIR,".static-collection")

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
	os.path.join(SITE_DIR,"data"),
	os.path.join(SITE_DIR,"frontend"),
	# Put strings here, like "/home/html/static" or "C:/www/django/static".
	# Always use forward slashes, even on Windows.
	# Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
	'django.contrib.staticfiles.finders.FileSystemFinder',
	'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'o(1dg4s@2c*vw-jr$rkjx!m6j=60g1s$4d)8$%$o%2+&amp;e*@e%7'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
	'django.template.loaders.filesystem.Loader',
	'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
	'django.middleware.common.CommonMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	#'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	# Uncomment the next line for simple clickjacking protection:
	# 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'wsgi.application'

TEMPLATE_DIRS = (
	os.path.join(SITE_DIR,"_templates"),
	# Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
	# Always use forward slashes, even on Windows.
	# Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
	'south',
	'django.contrib.contenttypes',
	'django.contrib.staticfiles',
	'django.contrib.gis',
	'django_extensions',
	'taggit',
	'samples',
	'jsonrpc'
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
	'version': 1,
	'disable_existing_loggers': False,
	'filters': {
		'require_debug_false': {
			'()': 'django.utils.log.RequireDebugFalse'
		}
	},
	'handlers': {
		'mail_admins': {
			'level': 'ERROR',
			'filters': ['require_debug_false'],
			'class': 'django.utils.log.AdminEmailHandler'
		}
	},
	'loggers': {
		'django.request': {
			'handlers': ['mail_admins'],
			'level': 'ERROR',
			'propagate': True,
		},
	}
}

CATIONS = "Si Fe Mg Ti Al Na Ca Mn Cr Ni".split()
OXIDES = "SiO2 FeO MgO TiO2 Al2O3 Na2O CaO MnO Cr2O3 NiO".split()
SAMPLES = "CK-1 CK-2 CK-3 CK-4 CK-5 CK-6 CK-7 CKD1 CKD2".split()

MINERALS = [
	("cpx", "Clinopyroxene"),
	("opx", "Orthopyroxene"),
	("sp", "Spinel"),
	("ol", "Olivine"),
	("na", "Unknown")
]

MINERAL_SYSTEMS = {
	"silicate": {
		"si": {"SiO2": 1},
		"fe": {"FeO": 1},
		"mg": {"MgO": 1}
	},
	"pyroxene": {
		"Wo": {"SiO2":1,"CaO":1},
		"En": {"SiO2":1,"MgO":1},
		"Fs": {"SiO2":1,"FeO":1}
	},
	"na_px": {
		"di": {"SiO2":2,"CaO":1,"MgO":1},
		"he": {"SiO2":2, "CaO":1,"FeO":1},
		"ja": {"SiO2":2, "Al2O3":.5,"Na2O":.5}
	},
	"olivine": {
		"Fo": {"SiO2":1,"MgO":2},
		"Fa": {"SiO2":1,"FeO":2}
	},
	"minerals": {
		"sp": {"FeO + MgO": 1, "Al2O3 + Cr2O3": 1},
		"ol": {"FeO + MgO":2,"SiO2":1},
		"cpx": {"FeO + MgO":1,"CaO":1,"SiO2": 2},
		"opx": {"FeO + MgO":2,"SiO2": 2}
	}
}
