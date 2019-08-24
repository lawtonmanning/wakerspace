from wakerspace import admin, db
from wakerspace.models import Maker
from flask_admin.contrib.sqla import ModelView

admin.add_view(ModelView(Maker, db.session))
