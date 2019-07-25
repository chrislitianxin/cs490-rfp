from joblib import dump, load
from sklearn import tree
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn import preprocessing, decomposition, model_selection, metrics, pipeline
from sklearn.metrics import log_loss
from flask import jsonify
import itertools


""" HELPER FUNCTION
"""


def flatmap(func, iterable):
    "Flatmap implemented using itertools"
    return list(itertools.chain.from_iterable(iterable))


class Model(object):
    """ Loading our ML model and run inferences.
        EXAMPLE: http://localhost:8000/tenders/predict?uuid=
    """

    def __init__(self, path, *args, **kwargs):
        self.model = load(path)
        return super().__init__(*args, **kwargs)

    def pred_probability(self, client_info, rfp_info):
        "run prediction algo and return the probability based on client info and tender info"
        company_assets = int(client_info["Total Assets"])
        company_size = int(client_info["Size"])
        # rfp_price = rfp_info["price"]
        rfp_num_consultants = len(rfp_info["consultants"])
        cost = int(rfp_info["cost"])

        # features for prediction
        features = [[company_assets, company_size, rfp_num_consultants,
                     cost, m/100, cost * (1+m/100)] for m in range(0, 100, 1)]
        prob = self.model.predict_proba(features)[..., :1].tolist()
        # flatten the list
        prob = flatmap(list.__add__, prob)

        return jsonify(prob)

    def retrain_model(self, hist_data, clients):
        """ Retrain the model and dump it over what we had"""
        print(hist_data)
        print(clients)
