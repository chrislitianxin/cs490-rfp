""" This is for integration with CRM's firebase """
import pyrebase

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

        try:
            # query crm db for client infomation
            client = db.child("clients").order_by_child(
                "Name").equal_to(client_name).get().val()
            _, client_info = client.popitem(last=False)

            return client_info

        except IndexError as err:
            return 'ClientNotFound'

    def get_all_clients_info(self):
        "Get all clients info"
        db = self.crm.database()

        try:
            # query crm db for client infomation
            clients = db.child("clients").get().val()
            return clients

        except IndexError as err:
            return 'Record Empty: ' + err
