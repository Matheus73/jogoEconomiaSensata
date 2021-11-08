from django.shortcuts import render, redirect
from .models import Form, Answer, Poll
from user.models import User

def poll(request):
    if request.session.get('user'):
        user_id = request.session.get('user')
        user = User.objects.get(pk = user_id)
        polls = Poll.objects.filter( bloc = user.bloc )
        final_polls = []
        for i in polls:
            creator = User.objects.get( pk = i.created_by.id )
            is_my = creator.id == user_id
            if not i.has_open or is_my or user_id in i.votes["votes"]:
                if i.pros > i.against:
                    result = True
                else:
                    result = False
                final_polls.append({"country": creator.country, "active": False, "poll_id": i.id, "result": result })
            else:
                final_polls.append({"country": creator.country, "active": i.has_open, "poll_id": i.id })
        return render(request, 'polls.html', {"polls": final_polls})

    else:
        return redirect('/auth/signin/?status=2')

def check_poll(request):
    choice = request.POST.get("choice")
    poll_id = request.POST.get("poll_id")
    print(choice, poll_id)
    poll = Poll.objects.get( pk = poll_id )
    if choice == "1":
        poll.pros += 1
    else:
        poll.against += 1
    votes = poll.votes['votes']
    votes.append(request.session.get("user"))
    poll.votes = {"votes": votes }
    poll.save()
    return redirect('/?status=2')

def render_form(request, id):
    if request.session.get('user'):
        form = Form.objects.get(pk = id)
        if form.active == False:
            return redirect('/?status=1')
        status = request.GET.get('status')
        print(form.questions['questions'], form.name)
        return render(request, 'form.html',
                      {"questions": form.questions['questions'], "name": form.name, "id": id, "status": status})
    else:
        return redirect('/auth/signin/?status=2')

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
    return redirect(f'/?status=0')

def home(request):
    if request.session.get('user'):
        status = request.GET.get('status')
        return render(request, 'home.html',
                      {"status": status})
    else:
        return redirect('/auth/signin/?status=2')
