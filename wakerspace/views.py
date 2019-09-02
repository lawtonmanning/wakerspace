from wakerspace import admin, db
import wakerspace.models as model
from flask_admin.contrib.sqla import ModelView

admin.add_view(ModelView(model.Maker, db.session))
admin.add_view(ModelView(model.Visit, db.session))
admin.add_view(ModelView(model.Training, db.session))
admin.add_view(ModelView(model.TrainingType, db.session))
admin.add_view(ModelView(model.Activity, db.session))
admin.add_view(ModelView(model.Color, db.session))
