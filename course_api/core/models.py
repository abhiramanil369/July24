from mongoengine import Document, StringField, IntField, ListField, FileField

class BasicInfo(Document):
    course_name = StringField(required=True)
    course_code = StringField(required=True, unique=True)
    year = IntField(required=True)
    branch = StringField(required=True)
    semester = IntField(required=True)
    group = StringField(required=True)

class CourseOutcome(Document):
    course_code = StringField(required=True)
    shortform_course_code = StringField(required=True)
    course_outcome = StringField(required=True)

class Syllabus(Document):
    course_code = StringField(required=True)
    syllabus = StringField(required=True)

class Question(Document):
    course_code = StringField(required=True)
    questions = StringField(required=True)

class CourseMaterial(Document):
    course_code = StringField(required=True)
    file = StringField(required=True)
    file_type = StringField(required=True)

class UserRequest(Document):
    user_id = StringField(required=True)
    course_code = StringField(required=True)
    user_question = StringField(required=True)
    previous_question_rating = IntField(required=True)
    response = StringField()
