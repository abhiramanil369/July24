import os
import uuid
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import BasicInfo, CourseOutcome, Syllabus, Question, CourseMaterial, UserRequest
from bson import json_util


def error_response(message):
    return JsonResponse({"success": False, "message": message}, status=400)


@csrf_exempt
def basic_info(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        required = ["course_name", "course_code", "year", "branch", "semester", "group"]
        if not all(k in data for k in required):
            return error_response("Missing fields")
        if BasicInfo.objects(course_code=data["course_code"]).first():
            return error_response("Course code already exists")
        info = BasicInfo(**data).save()
        info_json = json.loads(json_util.dumps(info.to_mongo()))
        return JsonResponse({
            "success": True,
            "message": "Basic info saved successfully",
            "data": info_json
        })


@csrf_exempt
def course_outcome(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        codes = data.get("course_code", [])
        shortcodes = data.get("shortform_course_code", [])
        outcomes = data.get("course_outcome", [])
        if not (len(codes) == len(shortcodes) == len(outcomes)):
            return error_response("Mismatched list lengths")
        if not all(BasicInfo.objects(course_code=code) for code in codes):
            return error_response("One or more course codes do not exist")

        results = []
        for i in range(len(codes)):
            obj = CourseOutcome(
                course_code=codes[i],
                shortform_course_code=shortcodes[i],
                course_outcome=outcomes[i]
            ).save()
            results.append(json.loads(json_util.dumps(obj.to_mongo())))
        return JsonResponse({
            "success": True,
            "message": f"{len(results)} course outcomes saved successfully",
            "data": results
        })


@csrf_exempt
def syllabus(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        codes = data.get("course_code", [])
        syls = data.get("syllabus", [])
        if not (len(codes) == len(syls)):
            return error_response("Mismatched list lengths")

        results = []
        for i in range(len(codes)):
            if not BasicInfo.objects(course_code=codes[i]):
                return error_response(f"Course code {codes[i]} does not exist")
            obj = Syllabus(course_code=codes[i], syllabus=syls[i]).save()
            results.append(json.loads(json_util.dumps(obj.to_mongo())))
        return JsonResponse({
            "success": True,
            "message": f"{len(results)} syllabi saved successfully",
            "data": results
        })


@csrf_exempt
def questions(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        codes = data.get("course_code", [])
        qs = data.get("questions", [])
        if not (len(codes) == len(qs)):
            return error_response("Mismatched list lengths")

        results = []
        for i in range(len(codes)):
            if not BasicInfo.objects(course_code=codes[i]):
                return error_response(f"Course code {codes[i]} does not exist")
            obj = Question(course_code=codes[i], questions=qs[i]).save()
            results.append(json.loads(json_util.dumps(obj.to_mongo())))
        return JsonResponse({
            "success": True,
            "message": f"{len(results)} question sets saved successfully",
            "data": results
        })


@csrf_exempt
def course_materials(request):
    if request.method == 'POST':
        codes = request.POST.getlist("course_code")
        file_types = request.POST.getlist("file_type")
        files = request.FILES.getlist("file")

        if not (len(codes) == len(file_types) == len(files)):
            return error_response("Mismatched file inputs")

        results = []
        for i in range(len(codes)):
            if not BasicInfo.objects(course_code=codes[i]):
                return error_response(f"Course code {codes[i]} does not exist")
            ext = os.path.splitext(files[i].name)[1].lower()
            if file_types[i] not in ["TXT", "PDF", "OCR"]:
                return error_response("Invalid file_type")
            filename = f"{uuid.uuid4()}{ext}"
            filepath = os.path.join(settings.MEDIA_ROOT, filename)
            with open(filepath, 'wb+') as f:
                for chunk in files[i].chunks():
                    f.write(chunk)
            obj = CourseMaterial(course_code=codes[i], file=filename, file_type=file_types[i]).save()
            results.append(json.loads(json_util.dumps(obj.to_mongo())))
        return JsonResponse({
            "success": True,
            "message": f"{len(results)} course materials saved successfully",
            "data": results
        })


@csrf_exempt
def process_file(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        code = data.get("course_code")
        if not code or not BasicInfo.objects(course_code=code):
            return error_response("Invalid course_code")
        return JsonResponse({
            "success": True,
            "message": "course materials processed successfully"
        })


@csrf_exempt
def user_request(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        required = ["user_id", "course_code", "user_question", "previous_question_rating"]
        if not all(k in data for k in required):
            return error_response("Missing fields")
        if not BasicInfo.objects(course_code=data["course_code"]):
            return error_response("Course code does not exist")

        data["response"] = "this is a sample ai response"
        obj = UserRequest(**data).save()
        obj_json = json.loads(json_util.dumps(obj.to_mongo()))
        return JsonResponse({
            "success": True,
            "message": "User request saved successfully",
            "response": obj.response,
            "data": obj_json
        })
