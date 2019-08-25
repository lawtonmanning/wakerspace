from wakerspace import admin, db
import wakerspace.models as model
from flask_admin.contrib.sqla import ModelView

admin.add_view(ModelView(model.Maker, db.session))
admin.add_view(ModelView(model.Equipment, db.session))
admin.add_view(ModelView(model.Room, db.session))
admin.add_view(ModelView(model.Training, db.session))
