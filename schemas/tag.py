from ma import ma
from models.tag import TagModel


class TagSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TagModel
        load_instance = True
        include_fk = True