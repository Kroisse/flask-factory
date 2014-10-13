from flask_factory import Factory

create_app = Factory(__name__)
create_app.step('.db:init_db')
