from django.http import HttpResponse
import openpyxl
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

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



def export_data_to_xlsx(request):
    workbook = openpyxl.Workbook()

    versions = Robot.objects.values_list('version', flat=True).distinct()

    models = Robot.objects.values_list('model', flat=True).distinct()

    for model in models:
        model_sheet = workbook.create_sheet(f'Model {model}')

        headers = ['Модель', 'Версия', 'Количество за неделю']
        model_sheet.append(headers)

        for version in versions:
            robot_data = Robot.objects.filter(model=model, version=version)
            for data_row in robot_data:
                row = [data_row.model, data_row.version, data_row.count_week]
                model_sheet.append(row)

    del workbook["Sheet"]

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="exported_data.xlsx"'
    workbook.save(response)

    return response