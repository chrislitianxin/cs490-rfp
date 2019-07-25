""" This is for integration with CRM's firebase """
import pyrebase
import flask

""" Added rules for query -> for CRM team 
{
  "rules": {
    "clients": {
        ".indexOn": ["Name","Category","Contact Details", "Main Contact Name", "Size", "Total Assets", "Province"]
    },
    ".read": true,
    ".write": true
  }
}
"""


class CRM(object):
    def __init__(self, config, *args, **kwargs):
        self.crm = pyrebase.initialize_app(config)
        return super().__init__(*args, **kwargs)

    def get_client_info(self, client_name):
        "Quering client info by client name"
        db = self.crm.database()
        print(client_name)
        try:
            # query crm db for client infomation
            client = db.child("clients").order_by_child(
                "Name").equal_to(client_name).get().val()
            _, client_info = client.popitem(last=False)

        except Exception:
            client_info = self.get_default_client_info()

        return client_info

    def get_default_client_info(self):
        _, client = self.crm.database().child("clients").order_by_child(
            "Name").equal_to('Canada Compassion').get().val().popitem(last=False)
        return client

    def get_all_clients_info(self):
        "Get all clients info"
        db = self.crm.database()
        try:
            # query crm db for client infomation
            clients = db.child("clients").get().val()
            client_list = [client['Name'] for _, client in clients.items()]

            return client_list

        except IndexError as err:
            return 'Record Empty: ' + err

    def add_new_client(self, name):
        "Add new client, post to CRM database"
        db = self.crm.database()
        req = {
            "Category ": "Welfare",
            "Contact Details": "647-378-4809",
            "Date Joined": "01/04/2019",
            "Main Contact Name": "Blah Ablah",
            "Name": name,
            "Province": "ON",
            "Size": "123",
            "Total Assets": "123456",
            "Total Tax Receipted Gifts": "247140"
        }

        try:
            return db.child("clients").push(req)

        except Exception as err:
            return err
