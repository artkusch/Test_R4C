from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .models import Robot


@csrf_exempt
def create_robot(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            model = data.get('model')
            version = data.get('version')
            created = data.get('created')

            serial = f"{model}-{version}"

            robot = Robot.objects.create(serial=serial, model=model, version=version, created=created)

            response_data = {'message': 'Robot created successfully', 'robot_id': robot.id}
            return JsonResponse(response_data, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid HTTP method'}, status=405)
