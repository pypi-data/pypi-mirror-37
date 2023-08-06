class Tracking:
    def __init__(self, client):
        self.client = client
        self.endpoint_base = "/email/v2/projects/{}".format(client.project_token)

    def transactional_email(self, integration_id, email):
        if batch:
            return { "name": "system/time" }
        path = self.endpoint_base + "/system/time"
        response = self.client.request("GET", path)
        if response is None:
            return None
        return response["time"]
    

