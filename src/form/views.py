from django.shortcuts import render, redirect
from .models import Form, Answer
from user.models import User

def render_form(request, id):
    if request.session.get('user'):
        form = Form.objects.get(pk = id)
        status = request.GET.get('status')
        print(form.questions['questions'], form.name)
        return render(request, 'form.html',
                      {"questions": form.questions['questions'], "name": form.name, "id": id, "status": status})
    else:
        return redirect('/auth/login/?status=2')

def check_form(request):
    answers = [{"question":f"question{i}", "answer" :request.POST.get(f"question{i}")} for i in range(1,19) ]
    form_id = request.POST.get('id')
    print(answers)
    for i in answers:
        if i["answer"] == '':
            return redirect(f'/form/form/{form_id}/?status=1')

    user_id = request.session.get('user')
    form = Form.objects.get(pk = form_id)
    user = User.objects.get(pk = user_id)
    answer = Answer(form=form, leader=user, choices={"answers": answers})
    answer.save()
    return redirect(f'/form/?status=0')

def home(request):
    print("ENTROU +++++++++++++")
    pass
