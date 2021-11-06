import pickle
import os


path = os.path.dirname(__file__)

minis_model = {
    "Agricultura e desenvolvimento rural": "agricultura",
    "Educação": "educacao",
    "Mudanças climáticas e meio ambiente": "ambiente",
    "Saúde": "saude",
    "Infraestreutura, Ciência e Tecnologia": "ciencia",
    "Desenvolvimento": "desenvolvimento",
    "Banco Central": "banco",
    "Economia": "economia"
}


def predict_min(data, name):
    model = pickle.load(open(f"{path}/models/model_{name}.pkl", 'rb'))
    normalizer = pickle.load(
        open(f"{path}/models/normalizer_{name}.pkl", 'rb'))

    input = normalizer.transform([data])
    input = [input[0][:-1]]

    result = model.predict(input)
    result[0][0]
    result = [result[0][0], 0, 0, 0, 0]
    result = normalizer.inverse_transform([result])
    return result[0][0]
