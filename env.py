import os

os.environ.setdefault('MY_ENVIRONMENT_VARIABLE', 'variable_value')
os.environ["SECRET_KEY"] = (
	"django-insecure-@dm98x&xsd44xol0&+hmv2577+_2k2gfm81*xtx7u!%&d60#k9"
)
os.environ["DEBUG"] = "True"  # Set to "False" in production
