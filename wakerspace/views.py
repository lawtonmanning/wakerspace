from wakerspace import admin, db
import wakerspace.models as model
from flask_admin.contrib.sqla import ModelView

class FullModelView(ModelView):
    def __init__(self,model,session):
        self.column_list = [str(col).split('.')[1] for col in model.__table__.columns]
        super().__init__(model,session)
        
        for col in self.column_list:
            print(col)

admin.add_view(ModelView(model.Maker, db.session))
admin.add_view(ModelView(model.Visit, db.session))
admin.add_view(ModelView(model.Training, db.session))
admin.add_view(ModelView(model.TrainingType, db.session))
admin.add_view(ModelView(model.Activity, db.session))
admin.add_view(ModelView(model.Color, db.session))
