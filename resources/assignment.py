from flask import request
from flask_restplus import Resource, fields, Namespace

from models.assignment import AssignmentModel
from schemas.assignment import AssignmentSchema

from models.tag import TagModel
from schemas.tag import TagSchema

from models.assignment_tag_mapping import AssignmentTagMappingModel
from schemas.assignment_tag_mapping import AssignmentTagMappingSchema

ASSIGNMENT_NOT_FOUND = "Assignment not found."


assignment_ns = Namespace('assignment', description='Get an assignment')
assignments_ns = Namespace('assignment', description='Create an Assignment')

assignment_schema = AssignmentSchema()
tag_schema = TagSchema()
assignment_tag_mapping_schema = AssignmentTagMappingSchema()

assignment = assignments_ns.model('Assignment', {
    'name': fields.String(description='Name of the Assignment',
                                    required=True,
                                    example='go_lang_professional_certification'),
    'title': fields.String(description='Title of the Assignment',
                                    required=True,
                                    example='Go Lang Programming Certificate - profession level'),
    'description': fields.String(description='Description of the Assignment',
                                    required=False,
                                    example='This Assignment is for go lang certificate - professional level. You will be having live coding session with author James'),
    'assignment_type': fields.String(description='Type of the Assignment',
                                    required=False,
                                    example='coding session'),
    'duration': fields.Integer(description='Duration of the Assignment in Minutes',
                                    required=False,
                                    example=30),
    'tags': fields.List(fields.String(description='Tags for the Assignment',
                                    required=False,
                                    example='go'))
})

assignment_success = assignments_ns.model('AssignmentCreated', {
    'id': fields.String(description='Id of the Assignment',
                                    required=True,
                                    example=1),
    'name': fields.String(description='Name of the Assignment',
                                    required=True,
                                    example='go_lang_professional_certification'),
    'title': fields.String(description='Title of the Assignment',
                                    required=True,
                                    example='Go Lang Programming Certificate - profession level'),
    'description': fields.String(description='Description of the Assignment',
                                    required=False,
                                    example='This Assignment is for go lang certificate - professional level. You will be having live coding session with author James'),
    'assignment_type': fields.String(description='Type of the Assignment',
                                    required=False,
                                    example='coding session'),
    'duration': fields.Integer(description='Duration of the Assignment in Minutes',
                                    required=False,
                                    example=30),
    'tags': fields.List(fields.String(description='Tags for the Assignment',
                                    required=False,
                                    example='go'))
})


class Assignments(Resource):

    @assignments_ns.response(201,'Created Assignment', model=assignment_success)
    @assignments_ns.response(400, 'Bad Request')
    @assignments_ns.expect(assignment)
    @assignments_ns.doc('Create Assignment')
    def post(self):

        try:
            assignment_json = request.get_json()

            # Get the tags from the Assignment and check if it already present
            # else create a new tag
            assignment_tags = assignment_json.get('tags')
            assignment_json.pop('tags')

            assignment_data = assignment_schema.load(assignment_json)
            assignment_data.save_to_db()
            for tag in assignment_tags:
                # Check if the tag is already present in the DB.
                # If already present add it to mapping table
                # else create the tag and then add it to the mapping table
                tag_info = TagModel.find_by_name(tag)
                if tag_info is None:
                    tag_info = tag_schema.load({'name': tag})
                    tag_info.save_to_db()

                assignment_tag_mapping_data = assignment_tag_mapping_schema.load(
                    {'assignment_id': assignment_schema.dump(assignment_data)['id'],
                    'tag_id': tag_schema.dump(tag_info)['id']})
                assignment_tag_mapping_data.save_to_db()
            return {'status': 'success', 'response': assignment_schema.dump(assignment_data)}, 201

        except BaseException as e:
            print(e, flush=True)
            return {'status': 'failure', 'message': 'Assignment Creation Failed'}, 400
            
class Assignment(Resource):

    def get(self, id):
        assignment_data = AssignmentModel.find_by_id(id)
        if assignment_data:
            return {'status': 'success', 'response': assignment_schema.dump(assignment_data)}, 201
        return {'message': ASSIGNMENT_NOT_FOUND}, 404
