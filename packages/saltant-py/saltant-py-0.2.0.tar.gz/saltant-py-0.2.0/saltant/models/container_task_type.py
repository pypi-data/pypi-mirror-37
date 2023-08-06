"""Container task type model and manager."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from .base_task_type import BaseTaskType, BaseTaskTypeManager


class ContainerTaskType(BaseTaskType):
    """Model for container task types.

    Attributes:
        id (int): The ID of the task type.
        name (str): The name of the task type.
        description (str): The description of the task type.
        user (str): The user associated with the task type.
        datetime_created (:class:`datetime.datetime`): The datetime when
            the task type was created.
        command_to_run (str): The command to run inside the container to
            execute the task.
        environment_variables (list): The environment variables required
            on the host to execute the task.
        required_arguments (list): The argument names for the task type.
        required_arguments_default_values (dict): Default values for the
            tasks required arguments.
        logs_path (str): The path of the logs directory inside the
            container.
        results_path (str): The path of the results directory inside the
            container.
        container_image (str): The container name and tag. For example,
            ubuntu:14.04 for Docker; and docker://ubuntu:14:04 or
            shub://vsoch/hello-world for Singularity.
        container_type (str): The type of the container.
        manager (:class:`saltant.models.container_task_type.ContainerTaskTypeManager`):
            The task type manager which spawned this task type.
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
        logs_path,
        results_path,
        container_image,
        container_type,
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
            logs_path (str): The path of the logs directory inside the
                container.
            results_path (str): The path of the results directory inside
                the container.
            container_image (str): The container name and tag. For
                example, ubuntu:14.04 for Docker; and docker://ubuntu:14:04
                or shub://vsoch/hello-world for Singularity.
            container_type (str): The type of the container.
            manager (:class:`saltant.models.container_task_type.ContainerTaskTypeManager`):
                The task type manager which spawned this task type.
        """
        # Call the parent constructor
        super(ContainerTaskType, self).__init__(
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

        # Add in the attributes unique to container task types
        self.logs_path = logs_path
        self.results_path = results_path
        self.container_image = container_image
        self.container_type = container_type

    def put(self):
        """Updates this task type on the saltant server.

        Returns:
            :class:`saltant.models.container_task_type.ContainerTaskType`:
                A task type model instance representing the task type
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
            logs_path=self.logs_path,
            results_path=self.results_path,
            container_image=self.container_image,
            container_type=self.container_type,
        )


class ContainerTaskTypeManager(BaseTaskTypeManager):
    """Manager for Container task types.

    Attributes:
        _client (:class:`saltant.client.Client`): An authenticated
            saltant client.
        list_url (str): The URL to list task types.
        detail_url (str): The URL format to get specific task types.
        model (:class:`saltant.models.container_task_type.ContainerTaskType`):
            The model of the task instance being used.
    """

    list_url = "containertasktypes/"
    detail_url = "containertasktypes/{id}/"
    model = ContainerTaskType

    def create(
        self,
        name,
        command_to_run,
        container_image,
        container_type,
        description="",
        logs_path="",
        results_path="",
        environment_variables=None,
        required_arguments=None,
        required_arguments_default_values=None,
        extra_data_to_post=None,
    ):
        """Create a container task type.

        Args:
            name (str): The name of the task.
            command_to_run (str): The command to run to execute the task.
            container_image (str): The container name and tag. For
                example, ubuntu:14.04 for Docker; and docker://ubuntu:14:04
                or shub://vsoch/hello-world for Singularity.
            container_type (str): The type of the container.
            description (str, optional): The description of the task type.
            logs_path (str, optional): The path of the logs directory
                inside the container.
            results_path (str, optional): The path of the results
                directory inside the container.
            environment_variables (list, optional): The environment
                variables required on the host to execute the task.
            required_arguments (list, optional): The argument names for
                the task type.
            required_arguments_default_values (dict, optional): Default
                values for the task's required arguments.
            extra_data_to_post (dict, optional): Extra key-value pairs
                to add to the request data. This is useful for
                subclasses which require extra parameters.

        Returns:
            :class:`saltant.models.container_task_type.ContainerTaskType`:
                A container task type model instance representing the
                task type just created.
        """
        # Add in extra data specific to container task types
        if extra_data_to_post is None:
            extra_data_to_post = {}

        extra_data_to_post.update(
            {
                "container_image": container_image,
                "container_type": container_type,
                "logs_path": logs_path,
                "results_path": results_path,
            }
        )

        # Call the parent create function
        return super(ContainerTaskTypeManager, self).create(
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
        logs_path,
        results_path,
        container_image,
        container_type,
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
            extra_data_to_put (dict, optional): Extra key-value pairs to
                add to the request data. This is useful for subclasses
                which require extra parameters.
            logs_path (str): The path of the logs directory inside the
                container.
            results_path (str): The path of the results directory inside
                the container.
            container_image (str): The container name and tag. For
                example, ubuntu:14.04 for Docker; and docker://ubuntu:14:04
                or shub://vsoch/hello-world for Singularity.
            container_type (str): The type of the container.
        """
        # Add in extra data specific to container task types
        if extra_data_to_put is None:
            extra_data_to_put = {}

        extra_data_to_put.update(
            {
                "logs_path": logs_path,
                "results_path": results_path,
                "container_image": container_image,
                "container_type": container_type,
            }
        )

        # Call the parent create function
        return super(ContainerTaskTypeManager, self).put(
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
