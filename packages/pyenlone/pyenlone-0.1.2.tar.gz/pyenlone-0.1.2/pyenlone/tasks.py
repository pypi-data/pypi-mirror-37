from proxy import Proxy, TokenProxy, KeyProxy
from enloneexception import EnlOneException

class Tasks:
    _proxy : Proxy
    _base_url = "v.enl.one/"
    def __init__(self, **kwargs):
        if "token" in kwargs:
            _proxy = TokenProxy(_base_url, kwargs["token"])
        elif "apikey" in kwargs:
            _proxy = KeyProxy(_base_url, kwargs["apikey"])
        else:
            raise EnlOneException("You need to either provide token or apikey as keyword argument.")

    # OPs
    def get_op(self):
        raise EnlOneException("Not implemented yet.")
    def get_ops(self):
        raise EnlOneException("Not implemented yet.")
    def post_op(self):
        raise EnlOneException("Not implemented yet.")
    def put_op(self):
        raise EnlOneException("Not implemented yet.")
    def delete_op(self):
        raise EnlOneException("Not implemented yet.")
    def get_grant(self):
        raise EnlOneException("Not implemented yet.")
    def get_grants(self):
        raise EnlOneException("Not implemented yet.")
    def get_permissions(self):
        raise EnlOneException("Not implemented yet.")
    def get_messages(self):
        raise EnlOneException("Not implemented yet.")
    def get_message(self):
        raise EnlOneException("Not implemented yet.")
    def delete_message(self):
        raise EnlOneException("Not implemented yet.")
    def search_ops(self):
        raise EnlOneException("Not implemented yet.")
    def get_users(self):
        raise EnlOneException("Not implemented yet.")
    def sync_rocks_comm(self):
        raise EnlOneException("Not implemented yet.")

    # Tasks
    def get_tasks(self):
        raise EnlOneException("Not implemented yet.")
    def get_op_tasks(self):
        raise EnlOneException("Not implemented yet.")
    def search_tasks(self):
        raise EnlOneException("Not implemented by backend.")
    def get_task():
        raise EnlOneException("Not implemented yet.")
    def post_task():
        raise EnlOneException("Not implemented yet.")
