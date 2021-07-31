from flask import request
from flask_restplus import Resource, fields, Namespace

from models.tag import TagModel
from schemas.tag import TagSchema

from models.assignment_tag_mapping import AssignmentTagMappingModel
from schemas.tag import TagSchema
from schemas.assignment import AssignmentSchema


TAG_NOT_FOUND = "Tag not found."

tag_ns = Namespace('tags', description='Tag related operations')

tag_schema = TagSchema(many=True)
# tag_schema = TagSchema()
assignments_schema = AssignmentSchema(many=True)

tag = tag_ns.model('Tag', {
    'name': fields.String(fields.String(description='Name of the Tag for the Assignment',
                                    required=False,
                                    example='go'))
})


class Tag(Resource):
    def get(self, name):
        assignment_data = AssignmentTagMappingModel.find_by_tag_name(name)
        if assignment_data:
            return {'status': 'success', 'response': assignments_schema.dump(assignment_data)}, 200
        return {'message': TAG_NOT_FOUND}, 404
