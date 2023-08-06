import boto3

from .task_definition import TaskDefinition

class Service:
    """
    Class to handle ECS Services
    """

    __description = None
    __task_definition = None
    __tasks = []

    def __init__(self, name, cluster, boto3_session):
        assert isinstance(boto3_session, boto3.session.Session), \
        "Please, provide an boto3 Session as argument!"

        self.boto3_session = boto3_session
        self.name = name
        self.cluster = cluster
        self.ecs = boto3_session.client('ecs')

    def update_description(self):
        """
        Calls AWS's describe_services (http://bit.ly/2OHJqm8) to get
        more data about the current service
        """

        try:
            data = self.ecs.describe_services(cluster=self.cluster.name, services=[self.name])

            # Do we have data?
            assert data

            # Is it in the format we expect?
            assert isinstance(data, dict)

            # Do we have failures?
            assert not list(data['failures'])

            # Does the metadata points to a successful request?
            assert int(data['ResponseMetadata']['HTTPStatusCode']) < 400

            # Is there actual data in it and do we have exactly one service?
            assert len(data['services']) == 1

        except AssertionError as assertion_error:
            print("Found an assertion error {}".format(assertion_error))
            print("The current state of failures is: ")
            print("\n".join(data['failures']))
        else:
            self.__description = data['services'][0]

    @property
    def task_definition(self):
        """
        Gets the current service's task definition
        """

        if not self.__task_definition:
            if not self.__description:
                self.update_description()

            self.__task_definition = TaskDefinition(
                self.__description['taskDefinition'],
                self.boto3_session
            )

        return self.__task_definition

    @property
    def description(self):
        """
        If the Service's description is not known, we load it.
        If we already know it, we just return it.
        """
        if not self.__description:
            self.update_description()

        return self.__description

    @property
    def deployments(self):
        """
        Returns the current service's deployments
        """
        return self.description['deployments']

    def __getattr__(self, attribute):
        """
        Wrapper that exposes every field inside the dictionary
        of description as attributes
        """

        # If the attribute does not exist as a key inside
        # the description dictionary, we raise an exception
        if attribute not in self.description:
            raise AttributeError("{} does not exist!".format(attribute))

        # If it does exist, we return it
        return self.description[attribute]

    def __repr__(self):
        """
        Basic string representation for a service is its name
        """
        return self.name

    def update_service(self, new_task_definition, force_new_deployment=True):
        """
        Calls the update_service method to use a new task definition.
        It forces a new deployment by default
        """
        return self.ecs.update_service(
            cluster=self.cluster.name, service=self.name,
            taskDefinition=new_task_definition,
            forceNewDeployment=force_new_deployment
        )
