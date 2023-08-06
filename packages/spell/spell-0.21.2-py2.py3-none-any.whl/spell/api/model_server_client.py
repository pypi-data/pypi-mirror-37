from spell.api import base_client
from spell.api.utils import url_path_join


MODEL_SERVER_URL = "model_servers"


class ModelServerClient(base_client.BaseClient):

    def new_model_server(self, server_name, tag, path, docker_image=None):
        """Create a new model server.

        Keyword arguments:
        server_name - the name of the model server
        tag - the tag of the model server
        path - path which points to the model
        docker_image - docker image to use if overriding default

        Returns:
        a ModelServer object for the created model

        """
        payload = {
            "server_name": server_name,
            "tag": tag,
            "resource_path": path,
            "docker_image": docker_image
        }
        url = url_path_join(MODEL_SERVER_URL, self.owner)
        r = self.request("post", url, payload=payload)
        self.check_and_raise(r)
        return self.get_json(r)["model_server"]

    def get_model_servers(self):
        """Get a list of model servers.

        Returns:
        a list of Model Server objects for this user

        """
        url = url_path_join(MODEL_SERVER_URL, self.owner)
        r = self.request("get", url)
        self.check_and_raise(r)
        return self.get_json(r)["model_servers"]

    def get_model_server(self, server_name, tag):
        """Get a info about a model server

        Keyword arguments:
        server_name - name of the model server to retrieve
        tag - tag of the model server to retrieve

        Returns:
        a ModelServer object with the specified name and tag
        """
        specifier = "{}:{}".format(server_name, tag)
        url = url_path_join(MODEL_SERVER_URL, self.owner, specifier)
        r = self.request("get", url)
        self.check_and_raise(r)
        return self.get_json(r)["model_server"]

    def delete_model_server(self, server_name, tag):
        """Removes a model server

        Keyword arguments:
        server_name - name of the model server to remove
        tag - tag of the model server to remove

        """
        specifier = "{}:{}".format(server_name, tag)
        url = url_path_join(MODEL_SERVER_URL, self.owner, specifier)
        r = self.request("delete", url)
        self.check_and_raise(r)

    def start_model_server(self, server_name, tag):
        """Starts a model server

        Keyword arguments:
        server_name - name of the model server to start
        tag - tag of the model server to start

        """
        specifier = "{}:{}".format(server_name, tag)
        url = url_path_join(MODEL_SERVER_URL, self.owner, specifier, "start")
        r = self.request("post", url)
        self.check_and_raise(r)

    def stop_model_server(self, server_name, tag):
        """Stops a model server

        Keyword arguments:
        server_name - name of the model server to stop
        tag - tag of the model server to stop

        """
        specifier = "{}:{}".format(server_name, tag)
        url = url_path_join(MODEL_SERVER_URL, self.owner, specifier, "stop")
        r = self.request("post", url)
        self.check_and_raise(r)
