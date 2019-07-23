from firebase import firebase

firebase = firebase.FirebaseApplication(
    "https://cs490-5eacc.firebaseio.com/", None)


new_historical_tender = {"client_id": 48627901,
                         "client_name": "Unversity of Waterloo",
                         "client_size": "medium",
                         "consultants": {"lead": "Mr Goose"},
                         "contact": {"email": "mrgoose@uwaterloo.ca", "name": "Goose Master"},
                         "currency": "CAD",
                         "date_received": "06-01-2019",
                         "last_accessed": "07-02-2019",
                         "location": {"city": "Toronto", "country": "Canada", "region": "Ontario"},
                         "price": 123455}


def post_to_db(data):
    result = firebase.post('/tenders/historical', data=data,
                           params={'print': 'pretty'})
    return result


def get_all_data():
    #query = '/tenders/historical?orderBy=\"price\"&startAt=21000'
    query = '/tenders/historical'
    result = firebase.get(query, None)
    return result
