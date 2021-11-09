from django.shortcuts import render, redirect
from .models import Form, Answer, Poll
from .dashboard import app
from user.models import User

import pickle
import pandas as pd
import os

from sklearn.preprocessing import MinMaxScaler

from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from catboost import CatBoostRegressor

from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

from sklearn.ensemble import ExtraTreesRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import AdaBoostRegressor


def dashboard(request):
    return render(request, 'dashboard.html')


def create_poll(request):
    user_id = request.session.get('user')
    user = User.objects.get(pk=user_id)
    form_name = request.POST.get("form_name")
    form_name = request.GET['form_name'].replace("_", " ")
    form = Form.objects.filter(name=form_name)[0]

    exists_polls = len(Poll.objects.filter(created_by=user, form=form)) > 0
    if exists_polls:
        return redirect('/?status=4')
    else:
        new_poll = Poll(created_by=user, bloc=user.bloc,
                        form=form, has_open=True)
        new_poll.save()
        return redirect('/?status=3')


def poll(request):
    if request.session.get('user'):
        user_id = request.session.get('user')
        user = User.objects.get(pk=user_id)
        polls = Poll.objects.filter(bloc=user.bloc)
        forms = Form.objects.filter(active=True)
        final_polls = []
        for i in polls:
            creator = User.objects.get(pk=i.created_by.id)
            is_my = creator.id == user_id
            if not i.has_open or is_my or user_id in i.votes["votes"]:
                if i.pros > i.against:
                    result = True
                else:
                    result = False
                final_polls.append({"form": i.form.name, "country": creator.country,
                                   "active": False, "owner": is_my, "poll_id": i.id, "result": result})
            else:
                final_polls.append(
                    {"form": i.form.name, "country": creator.country, "owner": is_my, "active": i.has_open, "poll_id": i.id})
        return render(request, 'polls.html', {"polls": final_polls, "forms": [{"value": i.name.replace(" ", "_"), "name": i.name} for i in forms]})

    else:
        return redirect('/auth/signin/?status=2')


def check_poll(request):
    choice = request.POST.get("choice")
    poll_id = request.POST.get("poll_id")
    print(choice, poll_id)
    poll = Poll.objects.get(pk=poll_id)
    if choice == "1":
        poll.pros += 1
    else:
        poll.against += 1
    votes = poll.votes['votes']
    votes.append(request.session.get("user"))
    poll.votes = {"votes": votes}
    poll.save()
    return redirect('/?status=2')


def render_form(request, id):
    if request.session.get('user'):
        form = Form.objects.get(pk=id)
        if form.active == False:
            return redirect('/?status=1')
        status = request.GET.get('status')
        print(form.questions['questions'], form.name)
        return render(request, 'form.html',
                      {"questions": form.questions['questions'], "name": form.name, "id": id, "status": status})
    else:
        return redirect('/auth/signin/?status=2')


def check_form(request):

    json = {"questions": [
        {
            "model": "agricultura",
            "questions": ["question1"]
        },
        {
            "model": "educacao",
            "questions": ["question2", "question3", "question4", ]
        },
        {
            "model": "ambiente",
            "questions": ["question5", "question6", "question7", ]
        },
        {
            "model": "saude",
            "questions": ["question8", ]
        },
        {
            "model": "ciencia",
            "questions": ["question9", ]
        },
        {
            "model": "desenvolvimento",
            "questions": ["question10", ]
        },
        {
            "model": "banco",
            "questions": ["question11", ]
        },
        {
            "model": "economia",
            "questions": ["question12", "question13", "question14", ]
        }
    ]
    }
    answers = [{"question": f"question{i}", "answer": request.POST.get(
        f"question{i}")} for i in range(1, 15)]
    final_json = {}
    for i in json['questions']:
        final_json[i['model']] = [
            int(j["answer"]) for j in answers if j['question'] in i["questions"]]

    final_json['agricultura'] = [final_json['agricultura'][0]/100 * 10**12]
    final_json['economia'] = [i/100 * 10**12 for i in final_json['economia']]
    final_json['desenvolvimento'] = [
        100 - final_json['desenvolvimento'][0]/0.4 * 100]
    final_json['ambiente'] = [0.5 * i for i in final_json['ambiente']]

    results = {}
    for i in final_json:
        tmp = final_json[i]
        tmp.append(0)
        results[i] = predict_min(tmp, i)

    user_id = request.session.get('user')
    form_id = request.POST.get('id')
    form = Form.objects.get(pk=form_id)
    user = User.objects.get(pk=user_id)

    poll = Poll.objects.filter(created_by=user, form=form)
    if len(poll) > 0:
        poll = poll[0]
        aproved = poll.pros > poll.against
    else:
        aproved = False

    for i in answers:
        if i["answer"] == '':
            return redirect(f'/form/{form_id}/?status=1')
        elif int(i["answer"]) > 40:
            return redirect(f'/form/{form_id}/?status=2')
        elif int(i["answer"]) > 20 and not aproved:
            return redirect(f'/form/{form_id}/?status=3')

    answer = Answer(form=form, leader=user, choices={"answers": answers}, result_agricultura=results['agricultura'],
                    result_educacao=results['educacao'], result_ambiente=results['ambiente'], result_saude=results["saude"],
                    result_infraestrutura=results['ciencia'], result_desenvolvimento=results['desenvolvimento'],
                    result_bancoCentral=results['banco'], result_economia=results['economia'])
    answer.save()
    return redirect(f'/?status=0')


def home(request):
    if request.session.get('user'):
        status = request.GET.get('status')
        return render(request, 'home.html',
                      {"status": status})
    else:
        return redirect('/auth/signin/?status=2')


def about(request):
    if request.session.get('user'):
        status = request.GET.get('status')
        return render(request, 'about.html',
                      {"status": status})
    else:
        return redirect('/auth/signin/?status=2')


def predict_min(data, name):
    path = os.path.dirname("../")
    model = pickle.load(open(f"{path}/models/model_{name}.pkl", 'rb'))
    normalizer = pickle.load(
        open(f"{path}/models/normalizer_{name}.pkl", 'rb'))

    input = normalizer.transform([data])
    input = [input[0][:-1]]

    result = model.predict(input)

    return result[0]
