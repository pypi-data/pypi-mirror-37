"""
Provides a class for AWS's ECS Task Definitions
"""

import boto3

class TaskDefinition:
    """
    Abstracts an ECS's Task Definition
    """

    __description = []

    def __init__(self, name, boto3_session):
        assert isinstance(boto3_session, boto3.session.Session), \
        "Please, provide an boto3 Session as argument!"

        self.name = name
        self.ecs = boto3_session.client('ecs')

    def update_description(self):
        """
        Calls AWS's describe_task_definition (http://bit.ly/2nLZaJw)
        to get more data about the current service
        """

        try:
            data = self.ecs.describe_task_definition(taskDefinition=self.name)

            # Do we have data?
            assert data

            # Is it in the format we expect?
            assert isinstance(data, dict)

            # Does the metadata points to a successful request?
            assert int(data['ResponseMetadata']['HTTPStatusCode']) < 400

            # Is there actual data in it and do we have exactly one service?
            assert isinstance(data['taskDefinition'], dict)

        except AssertionError as e:
            print("Found an assertion error {}".format(e))
            raise

        else:
            self.__description = data['taskDefinition']

    @property
    def description(self):
        """
        If the Task Definition's description is not known, we load it.
        If we already know it, we just return it.
        """
        if not self.__description:
            self.update_description()

        return self.__description

    # TODO: Make it accept multiple variables
    # TODO: Allow the deletion of variables
    def update_env(self, env_name, env_value, insert_if_missing=True):
        """
        This method will update an environment variable with name `env_name`
        and value `env_value` in all containers defined within the current
        task definition.

        There's an optional argument, insert_if_missing, that will do just
        as described - if there isn't a value for the current variable,
        we will create one.

        AWS uses a weird list-of-dictionaries syntax to list the envs.
        Instead of the expected:

        {
            environment_name: env1
        }

        We get:

        [
            {
                name: environment_name,
                value: environment_value
            }
        ]

        Two small comprehensions - a dict and then a list - do
        the job of converting between Amazon's list-of-dict
        to a dict and then back to list-of-dicts to send
        to AWS.
        """

        containers = self.description['containerDefinitions']
        updated_containers = []

        for container in containers:
            # Dict comprehension to convert list-of-dicts to dict. See method docstring
            environment = {x['name']: x['value'] for x in container['environment']}

            if env_name in environment or insert_if_missing:
                environment[env_name] = env_value

            # List comprehension to convert dict to list-of-dicts. See method docstring
            environment = [{'name': key, 'value': value} for key, value in environment.items()]

            container['environment'] = environment

            updated_containers.append(container)

        # The settings we will use for our new task definition keeps all the current ones
        # except for the containerDefinitions, which we have updated.
        current_settings = self.description

        # Now we remove all the keys that doesn't make
        # sense for registering a new task definition
        current_settings.pop('containerDefinitions')  # This is the parameter we changed
        current_settings.pop('taskDefinitionArn')  # Points to the current definition
        current_settings.pop('revision')  # Points to the current revision
        current_settings.pop('status')  # The current status of the present task definition
        current_settings.pop('requiresAttributes')  #  Not supported for new task definitions
        current_settings.pop('compatibilities')  #  Not supported as well

        # Register a new task definition using all the current
        # settings except for the containers
        return self.ecs.register_task_definition(
            containerDefinitions=updated_containers,
            **current_settings
        )
