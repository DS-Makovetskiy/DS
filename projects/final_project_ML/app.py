from flask import Flask, render_template, request
import pickle
import numpy as np
import pandas as pd
from scipy.sparse import load_npz
import os
import random

# app = Flask(__name__)

# train_pivot = pd.read_csv('data/train_pivot.csv')
# train_pivot_sparse = load_npz('data/train_pivot_sparse.npz')

# random_visitorids = random.sample(range(train_pivot_sparse.shape[1]), 10)


# def load_model(file_path):
#     with open(file_path, 'rb') as model_file:
#         model = pickle.load(model_file)
#     return model

# def get_user_input():
#     while True:
#         try:
#             # visitorid = int(request.form['visitorid'])
#             visitorid = int(request.args.get('visitorid'))
#             return visitorid
#         except ValueError:
#             return render_template('index.html', error="Ошибка ввода. Пожалуйста, введите целое число.")

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         visitorid = get_user_input()
#         unique_items = np.array(pd.read_csv('data/train_pivot.csv').columns)
#         model = load_model('models/fm_model.pkl')
#         recommendations_ids, scores = model.recommend(visitorid, train_pivot_sparse[visitorid])
#         recommendations = unique_items[recommendations_ids]
#         return render_template('recommendations.html', visitorid=visitorid, recommendations=recommendations)
#     return render_template('index.html')

# @app.route('/recommendations', methods=['GET'])
# def recommendations():
#     visitorid = request.args.get('visitorid')
#     recommendations_ids = request.args.getlist('recommendations[]')
    
#     # return render_template('recommendations.html', visitorid=request.args.get('visitorid'), recommendations=request.args.getlist('recommendations'))
#     return render_template('recommendations.html', visitorid=visitorid, recommendations_ids=recommendations_ids)

# if __name__ == "__main__":
#     current_directory = os.path.dirname(os.path.abspath(__file__))
#     app.run(debug=True, host='0.0.0.0')
    
    
    
    
from flask import Flask, request, render_template
import pickle
import numpy as np
import pandas as pd
from scipy.sparse import load_npz
import os
import random

app = Flask(__name__)

MODEL_PATH = ''

def load_model(file_path):
    with open(file_path, 'rb') as model_file:
        model = pickle.load(model_file)
    return model

def get_user_input():
    return render_template('index.html')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        visitorid = int(request.form['visitorid'])
        
        train_pivot_sparse = load_npz(os.path.join(MODEL_PATH, 'train_pivot_sparse.npz'))
        model = load_model(os.path.join(MODEL_PATH, 'fm_model.pkl'))

        unique_items = np.array(pd.read_csv(os.path.join(MODEL_PATH, 'train_pivot.csv')).columns)

        recommendations_ids, scores = model.recommend(visitorid, train_pivot_sparse[visitorid])
        recommendations = unique_items[recommendations_ids]

        return render_template('recommendations.html', visitorid=visitorid, recommendations=recommendations)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
    