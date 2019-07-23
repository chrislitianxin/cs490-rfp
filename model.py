from joblib import dump, load
from sklearn import tree
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn import preprocessing, decomposition, model_selection, metrics, pipeline
from sklearn.metrics import log_loss


class Model(object):
    """ Loading our ML model and run inferences.
        EXAMPLE: http://localhost:8000/tenders/predict?id=RFP-12345
    """

    def __init__(self, path, *args, **kwargs):
        self.model = load(path)
        return super().__init__(*args, **kwargs)

    def pred_probability(self, client_info, rfp_info):
        "run prediction algo and return the probability based on client info and tender info"
        company_assets = client_info["Total Assets"]
        company_size = client_info["Size"]
        rfp_price = rfp_info["price"]
        rfp_num_consultants = len(rfp_info["consultants"])
        # TODO
        cost = 10000
        margin = 0.3

        # features for prediction
        features = [company_assets, company_size, rfp_num_consultants,
                    cost, margin, rfp_price]
        prob = self.model.predict_proba([features])[0][0]
        print(features)
        return '{:.2f}%'.format(prob)

    def retrain_model(self, hist_data, clients):
        """ Retrain the model and dump it over what we had"""
        print(hist_data)
        print(clients)
