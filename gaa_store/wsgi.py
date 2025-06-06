# gaa_store/wsgi.py

import os
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gaa_store.settings")
_django_app = get_wsgi_application()

# Step A: Wrap the Django app in WhiteNoise to serve static files
application = WhiteNoise(
    _django_app,
    root=os.path.join(os.path.dirname(__file__), "..", "staticfiles"),
    prefix="static/"
)

# (Optionally) If you also want WhiteNoise to serve media (UPLOAD) files,
# you can add something like these two lines:
application.add_files(os.path.join(os.path.dirname(__file__), "..", "media"), prefix="media/")
#
# That tells WhiteNoise: “When someone requests /media/…, read from the local media folder.”
