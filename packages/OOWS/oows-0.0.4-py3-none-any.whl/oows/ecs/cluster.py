import boto3

from .service import Service

class Cluster:
    """
    Class to handle an ECS Cluster
    """
    def __init__(self, name, boto3_session):
        assert isinstance(boto3_session, boto3.session.Session), \
        "Please, provide an boto3 Session as argument!"

        self.name = name
        self.boto3_session = boto3_session
        self.ecs = boto3_session.client('ecs')
        self.__services = []

    @property
    def services(self):
        """
        Lists all the services in a cluster
        """
        if not self.__services:
            data = self.ecs.list_services(cluster=self.name)
            for item in data['serviceArns']:
                self.__services.append(Service(item, self, self.boto3_session))

        return self.__services
