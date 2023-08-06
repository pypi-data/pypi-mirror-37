"""Executable task type model and manager."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from .base_task_type import BaseTaskType, BaseTaskTypeManager


class ExecutableTaskType(BaseTaskType):
    """Model for executable task types.

    Attributes:
        id (int): The ID of the task type.
        name (str): The name of the task type.
        description (str): The description of the task type.
        user (str): The user associated with the task type.
        datetime_created (:class:`datetime.datetime`): The datetime when
            the task type was created.
        command_to_run (str): The command to run to execute the task.
        environment_variables (list): The environment variables required
            on the host to execute the task.
        required_arguments (list): The argument names for the task type.
        required_arguments_default_values (dict): Default values for the
            task's required arguments.
        json_file_option (str): The name of a command line option, e.g.,
            --json-file, which accepts a JSON-encoded file for the
            command to run.
        manager (:class:`saltant.models.executable_task_type.ExecutableTaskTypeManager`):
            The task type manager which spawned this task type instance.
    """

    def __init__(
        self,
        id,
        name,
        description,
        user,
        datetime_created,
        command_to_run,
        environment_variables,
        required_arguments,
        required_arguments_default_values,
        json_file_option,
        manager,
    ):
        """Initialize a container task type.

        Args:
            id (int): The ID of the task type.
            name (str): The name of the task type.
            description (str): The description of the task type.
            user (str): The user associated with the task type.
            datetime_created (:class:`datetime.datetime`): The datetime
                when the task type was created.
            command_to_run (str): The command to run to execute the task.
            environment_variables (list): The environment variables
                required on the host to execute the task.
            required_arguments (list): The argument names for the task type.
            required_arguments_default_values (dict): Default values for
                the tasks required arguments.
            json_file_option (str): The name of a command line option,
                e.g., --json-file, which accepts a JSON-encoded file for
                the command to run.
            manager (:class:`saltant.models.container_task_type.ContainerTaskTypeManager`):
                The task type manager which spawned this task type.
        """
        # Call the parent constructor
        super(ExecutableTaskType, self).__init__(
            id=id,
            name=name,
            description=description,
            user=user,
            datetime_created=datetime_created,
            command_to_run=command_to_run,
            environment_variables=environment_variables,
            required_arguments=required_arguments,
            required_arguments_default_values=required_arguments_default_values,
            manager=manager,
        )

        # Add in the attributes unique to executable task types
        self.json_file_option = json_file_option

    def put(self):
        """Updates this task type on the saltant server.

        Returns:
            :class:`saltant.models.container_task_type.ExecutableTaskType`:
                An executable task type model instance representing the task type
                just updated.
        """
        return self.manager.put(
            id=self.id,
            name=self.name,
            description=self.description,
            command_to_run=self.command_to_run,
            environment_variables=self.environment_variables,
            required_arguments=self.required_arguments,
            required_arguments_default_values=(
                self.required_arguments_default_values
            ),
            json_file_option=self.json_file_option,
        )


class ExecutableTaskTypeManager(BaseTaskTypeManager):
    """Manager for executable task types.

    Attributes:
        _client (:class:`saltant.client.Client`): An authenticated
            saltant client.
        list_url (str): The URL to list task types.
        detail_url (str): The URL format to get specific task types.
        model (:class:`saltant.models.executable_task_type.ExecutableTaskType`):
            The model of the task instance being used.
    """

    list_url = "executabletasktypes/"
    detail_url = "executabletasktypes/{id}/"
    model = ExecutableTaskType

    def create(
        self,
        name,
        command_to_run,
        description="",
        environment_variables=None,
        required_arguments=None,
        required_arguments_default_values=None,
        json_file_option=None,
        extra_data_to_post=None,
    ):
        """Create a container task type.

        Args:
            name (str): The name of the task.
            command_to_run (str): The command to run to execute the task.
            description (str, optional): The description of the task type.
            environment_variables (list, optional): The environment
                variables required on the host to execute the task.
            required_arguments (list, optional): The argument names for
                the task type.
            required_arguments_default_values (dict, optional): Default
                values for the task's required arguments.
            json_file_option (str, optional): The name of a command line
                option, e.g., --json-file, which accepts a JSON-encoded
                file for the command to run.
            extra_data_to_post (dict, optional): Extra key-value pairs
                to add to the request data. This is useful for
                subclasses which require extra parameters.

        Returns:
            :class:`saltant.models.container_task_type.ExecutableTaskType`:
                An executable task type model instance representing the
                task type just created.
        """
        # Add in extra data specific to container task types
        if extra_data_to_post is None:
            extra_data_to_post = {}

        extra_data_to_post.update({"json_file_option": json_file_option})

        # Call the parent create function
        return super(ExecutableTaskTypeManager, self).create(
            name=name,
            command_to_run=command_to_run,
            description=description,
            environment_variables=environment_variables,
            required_arguments=required_arguments,
            required_arguments_default_values=required_arguments_default_values,
            extra_data_to_post=extra_data_to_post,
        )

    def put(
        self,
        id,
        name,
        description,
        command_to_run,
        environment_variables,
        required_arguments,
        required_arguments_default_values,
        json_file_option,
        extra_data_to_put=None,
    ):
        """Updates a task type on the saltant server.

        Args:
            id (int): The ID of the task type.
            name (str): The name of the task type.
            description (str): The description of the task type.
            command_to_run (str): The command to run to execute the task.
            environment_variables (list): The environment variables
                required on the host to execute the task.
            required_arguments (list): The argument names for the task type.
            required_arguments_default_values (dict): Default values for
                the tasks required arguments.
            json_file_option (str): The name of a command line option,
                e.g., --json-file, which accepts a JSON-encoded file for
                the command to run.
            extra_data_to_put (dict, optional): Extra key-value pairs to
                add to the request data. This is useful for subclasses
                which require extra parameters.
        """
        # Add in extra data specific to container task types
        if extra_data_to_put is None:
            extra_data_to_put = {}

        extra_data_to_put.update({"json_file_option": json_file_option})

        # Call the parent create function
        return super(ExecutableTaskTypeManager, self).put(
            id=id,
            name=name,
            description=description,
            command_to_run=command_to_run,
            environment_variables=environment_variables,
            required_arguments=required_arguments,
            required_arguments_default_values=(
                required_arguments_default_values
            ),
            extra_data_to_put=extra_data_to_put,
        )
