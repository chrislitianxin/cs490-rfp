# cs490-rfp

## Installation & Deployment 
### Installation
- Install Python
- Install pip - Python Package Manager 
- Create a python virtual environment `python3 -m venv venv`
- Install required packages `pip3 install -r requirements.txt`

### Deployment 
The deployment is automatic via Heroku. Just push your code changes and merge it into master, then give it a minute, it will be recognize by heroku and automatically compile and deploy. 
Note: if you are using any new packages, remeber to update the `requirements.txt` so heroku can detect changes and install in its environment. 

## RFP API
### /tenders/active
API endpoint to retrieve all active tenders

### /tenders/historical
API endpoint to retrieve all historical tenders

### /tenders/active/update_status
API endpoint to update status for an existing tender. 

**Params:** `id` `status`

### /clients
Get list of clients

### /consultants
Get list of consultants

### /tenders/pred
Get prediction on probability of tender accepted for profit margin in range `[0,100]`, pass in the tender id. 

**Params:** `id`