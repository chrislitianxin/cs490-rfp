from flask import Flask
from flask_cors import CORS
from flask import request, jsonify
# from firebase import Firebase
import pyrebase
import json
import datetime
import uuid

from crm import CRM
from model import Model

app = Flask(__name__)

CORS(app)

config_RFP = {
    "apiKey": "apiKey",
    "authDomain": "potato",
    "databaseURL": "https://cs490-5eacc.firebaseio.com",
    "storageBucket": "potatotwo",
}

config_HR = {
    "apiKey": "AIzaSyCNkrsI8P9HH63yxZSDmvAEL4-vu6c8wl0",
    "authDomain": "recruitment-6cae5.firebaseapp.com",
    "databaseURL": "https://recruitment-6cae5.firebaseio.com",
    "projectId": "recruitment-6cae5",
    "storageBucket": "recruitment-6cae5.appspot.com",
    "messagingSenderId": "307067666683",
    "appId": "1:307067666683:web:39e93a69988eacbc"
}

#fb = Firebase(config)
fb = pyrebase.initialize_app(config_RFP)

fb_hr = pyrebase.initialize_app(config_HR)

# configs
crm_config = {
    "apiKey": "AIzaSyApbbE90LsWekODFSlRLDz4nOIegHajMSc",
    "authDomain": "cs490-e9fd5.firebaseapp.com",
    "databaseURL": "https://cs490-e9fd5.firebaseio.com",
    "projectId": "cs490-e9fd5",
    "storageBucket": "",
    "messagingSenderId": "1073025923441",
    "appId": "1:1073025923441:web:1e5196bf90ba1485"
}

# initialize CRM integration
crm_fb = CRM(crm_config)

# initlize model
model = Model('model')

#######################################################################################################################
'''
Tender Entry SCHEMA:
<Firebase_unique_key>:{
    "client_name":"Canadian Red Cross Society",
    "consultants":{
        "lead":"Bob Rossi",
        "member1":"Andrew Roberts"
    },
    "contact":{
        "email":"nhelpal@crc.org.fake",
        "name":"Nancy Helpal"
    },
    "currency":"CAD",
    "date_accessed":"16-07-2019",       #Date this tender was last accessed
    "date_due":"20-07-2019",            #Date the tender is due
    "date_received":"07-01-2019",       #Date the tender was received
    "location":{
        "city":"Toronto",
        "country":"Canada",
        #Region can be "Atlantic Canada" || "Ontario" || "Quebec" || "Western Canada"
        "region":"Ontario"
    },
    "price":150000,
    "prob_accept": 27.5%,
    "status":"approved",                 #Status can be "approved" || "new" || "rejected"
    "tender_id": 20190722-150937994339   #YYYYMMDD-HHMMSSmicroseconds
}
'''


""" API endpoint help page """
@app.route('/', methods=['GET'])
def help_page():

    return '<h1>RFP API</h1> \
    <h3>/tenders/active</h3> \
        <p>API endpoint to retrieve all active tenders</p> \
    <h3>/tenders/historical</h3> \
        <p>API endpoint to retrieve all historical tenders</p> \
    <h3>/tenders/active/update_status</h3> \
        <p>API endpoint to update status for an existing tender. <br> Params: id   status</p> \
    <h3>/clients</h3> \
        <p>Get list of clients</p> \
    <h3>/consultants</h3> \
        <p>Get list of consultants</p> \
    <h3>/tenders/pred</h3> \
        <p>Get prediction on probability of tender accepted for profit margin in range [0,100], pass in the tender id \
            <br> Params: id </p>'


#######################################################################################################################
# API endpoint to retrieve all active tenders
@app.route('/tenders/active', methods=['GET'])
def get_active_tenders():
    # database = firebase.FirebaseApplication('https://cs490-5eacc.firebaseio.com', None)
    # result = database.get('/tenders/active', None,)
    # ret = json.dumps(result, indent=4, sort_keys=True)

    db = fb.database()
    result = db.child("tenders").child("active").get()

    print(result)
    return result.val()
#######################################################################################################################

#######################################################################################################################
# API endpoint to retrieve all historical tenders
@app.route('/tenders/historical', methods=['GET'])
def get_historical_tenders():
    # database = Firebase.FirebaseApplication('https://cs490-5eacc.firebaseio.com', None)
    # result = database.get('/tenders/historical', None,)
    # ret = json.dumps(result, indent=4, sort_keys=True)

    db = fb.database()
    result = db.child("tenders").child("historical").get()

    print(result)
    return result.val()
#######################################################################################################################

#######################################################################################################################
# API endpoint to add a tender to the database
# EXAMPLE: http://localhost:5000/tenders/add?name=Company%20Alpha&consultants=Alex,Andrew,Albert&contact_email=aaa@org.fake&contact_name=Adele%20Aka&currency=CAD&date_due=08-01-2019&date_rec=07-21-2019&city=Toronto&country=Canada&region=Ontario&price=12000&prob_accept=20.5
@app.route('/tenders/add', methods=['GET'])
def add_tender():
    # Get necessary tender parameters
    client_name = request.args.get('name', None)
    consultants = request.args.get('consultants', None)
    contact_email = request.args.get('contact_email', None)
    contact_name = request.args.get('contact_name', None)
    currency = request.args.get('currency', None)
    date_due = request.args.get('date_due', None)
    date_received = request.args.get('date_rec', None)
    location_city = request.args.get('city', None)
    location_country = request.args.get('country', None)
    location_region = request.args.get('region', None)
    price = request.args.get('price', None)
    probability_accepted = request.args.get('prob_accept', None)

    # Get values based on date and time
    d = datetime.datetime.today()
    # tender_id = d.strftime('%Y%m%d-%H%M%S%f')
    tender_id = "RFP-" + str(uuid.uuid4())[0:5]

    # Create the Database Entry
    entry = {}
    entry['client_name'] = client_name
    # Add consultants
    entry['consultants'] = {}
    cons = consultants.split(',')
    counter = 0
    for c in cons:
        if counter == 0:
            entry['consultants']['lead'] = c
        else:
            entry['consultants']['member' + str(counter)] = c
        counter += 1
    entry['contact'] = {}
    entry['contact']['email'] = contact_email
    entry['contact']['name'] = contact_name
    entry['currency'] = currency
    entry['date_accessed'] = d.strftime('%m-%d-%Y')  # datetime.date.today()
    entry['date_due'] = date_due
    entry['date_received'] = date_received
    entry['location'] = {}
    entry['location']['city'] = location_city
    entry['location']['country'] = location_country
    entry['location']['region'] = location_region
    entry['price'] = int(price)
    entry['prob_accept'] = float(probability_accepted)
    entry['status'] = "new"
    entry['tender_id'] = tender_id

    db = fb.database()
    # Push entry to database and use client_name as the key
    # result = db.child("tenders").child("active").child(client_name).set(entry)

    # Push entry to database and let Firebase create random unique key
    result = db.child("tenders").child("active").push(entry)

    # print(result.val())
    return result
#######################################################################################################################

#######################################################################################################################
@app.route('/tenders/delete', methods=['GET'])
def delete_tender(tender_id=None):

    if not tender_id:
        tender_id = request.args.get('id', None)
    db = fb.database()

    # Try to query active tenders
    try:
        # result = db.child("tenders").child("active").order_by_child("client_name").equal_to(client_name).get()
        activeQuery = db.child("tenders").child("active").order_by_child(
            "tender_id").equal_to(tender_id).get()
        # need this to force an IndexError if no tenders were found
        print(activeQuery.val())
        returnVal = "DELETED \n " + json.dumps(activeQuery.val())
        # returnVal += json.dumps(activeQuery.val())
        print(activeQuery.key())
        # revised delete
        db.child("tenders").child("active").child(
            activeQuery.each()[0].key()).remove()
        return returnVal
    except IndexError as e:
        # if we get index error then there were no entries with that name
        activeQuery = ""
        activeResultExists = False

    # Try to query historical tenders
    try:
        historicalQuery = db.child("tenders").child(
            "historical").order_by_child("tender_id").equal_to(tender_id).get()
        # need this to force an IndexError if no tenders were found
        print(historicalQuery.val())
        returnVal = "DELETED \n " + json.dumps(historicalQuery.val())
        # returnVal += json.dumps(historicalQuery.val())
        print(historicalQuery.key())
        db.child("tenders").child("historical").child(
            historicalQuery.each()[0].key()).remove()
        return returnVal

    except IndexError as e:
        # if we get index error then there were no entries with that name
        historicalQuery = ""
        historicalResultExists = False

    return "No Entry Found - DELETE FAILED"
#######################################################################################################################

# API endpoint to update status for an existing tender
# EXAMPLE: http://limitless-hollows-30605.herokuapp.com/tenders/active/update_status?id=RFP-12345&status=approved"
@app.route('/tenders/active/update_status', methods=['GET'])
def update_tender_status():

    # get params
    rfp_id = request.args.get('id', None)
    status = request.args.get('status', None)

    d = datetime.datetime.today()
    date_accessed = d.strftime('%d-%m-%Y')

    db = fb.database()
    # ensure status is correct and client name not null
    if (status == "approved" or status == "rejected") \
            and rfp_id is not None:
        try:
            # retrieve tender info
            rfp_key, tender = db.child("tenders").child("active").order_by_child(
                "tender_id").equal_to(rfp_id).get().val().popitem(last=False)

            tender["status"] = status
            tender["date_accessed"] = date_accessed

            if tender is not None:
                # move to historical tender
                db.child("tenders").child("historical").child(
                    rfp_key).set(tender)

                # Delete active tender
                delete_tender(tender['tender_id'])
                return tender

        except IndexError as e:
            return "Tender does not exist or not active"

    else:
        # 1. Only supports approved / rejected status update.
        # 2. if client_name does not exists, it will update a None client, will not add clutter to database
        return "Nothing updated."

#######################################################################################################################
# API endpoint to query the database based on client name OR tender id
@app.route('/tenders/query', methods=['GET'])
def query():
    search_text = request.args.get('search', None)
    # client_name = request.args.get('name', None)
    # tender_id = request.args.get('id', None)
    if search_text is None:
        return "BAD QUERY"

    db = fb.database()
    returnVal = ""
    activeResultExists = True
    historicalResultExists = True

    # Try to query active tenders
    try:
        if "RFP" not in search_text:
            activeQuery = db.child("tenders").child("active").order_by_child(
                "client_name").equal_to(search_text).get()
        else:
            activeQuery = db.child("tenders").child("active").order_by_child(
                "tender_id").equal_to(search_text).get()
        # need this to force an IndexError if no tenders were found
        print(activeQuery.val())
        returnVal += json.dumps(activeQuery.val())
    except IndexError as e:
        # if we get index error then there were no entries with that name
        activeQuery = ""
        activeResultExists = False

    # Try to query historical tenders
    try:
        if "RFP" not in search_text:
            historicalQuery = db.child("tenders").child("historical").order_by_child(
                "client_name").equal_to(search_text).get()
        else:
            historicalQuery = db.child("tenders").child(
                "historical").order_by_child("tender_id").equal_to(search_text).get()
        # need this to force an IndexError if no tenders were found
        print(historicalQuery.val())
        returnVal += "\n \n"
        returnVal += json.dumps(historicalQuery.val())
    except IndexError as e:
        # if we get index error then there were no entries with that name
        historicalQuery = ""
        historicalResultExists = False

    # Check if no results exist
    if not activeResultExists and not historicalResultExists:
        returnVal = "NO RESULTS"

    return returnVal
#######################################################################################################################


""" API endpoint to get a inference on probability of tender acceptance """
@app.route('/tenders/predict', methods=['GET'])
def pred_tender_acceptance():
    "Given RFP_ID, return the probability of acceptance of a tender"
    rfp_id = request.args.get('id', None)
    if not rfp_id:
        return "RFP not found"
    db = fb.database()

    # get rfp info
    rfp_key, rfp_info = db.child("tenders").child("active").order_by_child(
        "tender_id").equal_to(rfp_id).get().val().popitem(last=False)
    print(rfp_info['consultants'])
    # get client info
    client_name = rfp_info['client_name']
    client_info = crm_fb.get_client_info(client_name)

    prob = model.pred_probability(client_info, rfp_info)

    # update record probability
    # db.child("tenders").child("active").child(
    #     rfp_key).update({"prob_accept": prob})

    return prob


""" Trigger retrain of our model """
@app.route('/model/retrain', methods=['GET'])
def retrain():
    pass

    # # get historical records
    # db = fb.database()
    # historical = db.child("tenders").child("historical").get().val().items()

    # # get all clients info
    # clients = crm_fb.get_all_clients_info()

    # model.retrain_model(historical, clients)

    return None


""" Trigger retrain of our model """
@app.route('/crm/add_client/<name>', methods=['GET', 'POST'])
def create_client(name):
    req = request.json

    if request.method == 'POST':
        return crm_fb.add_new_client(name)
    else:
        return 'blah'

#######################################################################################################################
# This will let us retrieve consultant information
@app.route('/consultants', methods=['GET'])
def get_consultant_info():
    db = fb_hr.database()

    db_entry = db.child("employees").get()
    count = 0
    returnVal = ""

    for e in db_entry.each():
        returnVal += e.val()["name"] + "," + e.val()["salary"] + ","
        count += 1

    returnVal = str(count) + "," + returnVal
    return returnVal
    # return db_entry.val()
#######################################################################################################################
# This will let us retrieve client information
@app.route('/clients', methods=['GET'])
def get_clients_name():
    return jsonify(crm_fb.get_all_clients_info())
#######################################################################################################################

#######################################################################################################################
#Transition from Historical to Active
@app.route('/tenders/move', methods=['GET'])
def tender_active_to_historical():
    search_text = request.args.get('search', None)
    db = fb.database()

    #Get the existing active tender
    db_entry = db.child("tenders").child("historical").order_by_child("tender_id").equal_to(search_text).get()

    if db_entry is not None:
        #Create a database entry for the tender under active node
        db.child("tenders").child("active").push(db_entry.each()[0].val())

        #Delete the existing historical tender
        db.child("tenders").child("historical").child(db_entry.each()[0].key()).remove()
        #return db_entry.val()
        return db_entry.each()[0].val()
    else:
        return "Request error"
#######################################################################################################################

@app.route('/cosmin', methods=['POST'])
def cosmin_test():
    req = request.json

    print(req)


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5000, debug=True)
    app.run()

# venv/Scripts/activate
# deactivate
