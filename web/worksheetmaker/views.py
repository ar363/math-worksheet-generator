from django.shortcuts import render
from django.http import HttpResponseBadRequest, HttpResponse
from django.views.generic import TemplateView
from . import generate_worksheet


def generate_and_display_worksheet(request):

    max_question_count = 1200

    calc_type = request.GET.get('calc_type') or 'mix'
    digits = request.GET.get('digits') or 2
    question_count = request.GET.get('qcount') or 80
    
    try:
        digits = int(digits)
    except ValueError:
        digits = 2
    
    try:
        question_count = int(question_count)
    except ValueError:
        question_count = 80

    if calc_type not in ['+', '-', 'x', '/', 'mix']:
        return HttpResponseBadRequest('calc type can only be +, -, x or /')

    if digits not in [1, 2, 3]:
        return HttpResponseBadRequest('digits can only be 1, 2 or 3')

    if question_count > max_question_count or question_count < 1:
        return HttpResponseBadRequest(f'question count must be between 1 to {max_question_count}')

    worksheet = generate_worksheet(calc_type, digits, question_count)

    response = HttpResponse(worksheet, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="worksheet.pdf"'
    return response

class HomeView(TemplateView):
    template_name = 'worksheetmaker/home.html'