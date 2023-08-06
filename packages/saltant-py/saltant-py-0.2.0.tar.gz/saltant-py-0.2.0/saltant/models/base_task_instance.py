"""Base class for task instance models."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import json
import time
import dateutil.parser
from saltant.constants import (
    DEFAULT_TASK_INSTANCE_WAIT_REFRESH_PERIOD,
    HTTP_201_CREATED,
    HTTP_202_ACCEPTED,
    TASK_INSTANCE_FINISH_STATUSES,
)
from .resource import Model, ModelManager


class BaseTaskInstance(Model):
    """Base model for a task instance.

    Attributes:
        uuid (str): The UUID of the task instance.
        name (str): The name of the task instance.
        state (str): The state of the task instance.
        user (str): The username of the user who started the task.
        task_queue (int): The ID of the task queue the instance is
            running on.
        task_type (int): The ID of the task type for the instance.
        datetime_created (:class:`datetime.datetime`): The datetime when
            the task instance was created.
        datetime_finished (:class:`datetime.datetime`): The datetime
            when the task instance finished.
        arguments (dict): The arguments the task instance was run with.
        manager (:class:`saltant.models.base_task_instance.BaseTaskInstanceManager`):
            The task instance manager which spawned this task instance.
            This is used to conveniently add clone, terminate, and
            wait_until_finished methods to the task instance model
            itself (such convenience!).
    """

    def __init__(
        self,
        uuid,
        name,
        state,
        user,
        task_queue,
        task_type,
        datetime_created,
        datetime_finished,
        arguments,
        manager,
    ):
        """Initialize a task instance.

        Args:
            uuid (str): The UUID of the task instance.
            name (str): The name of the task instance.
            state (str): The state of the task instance.
            user (str): The username of the user who started the task.
            task_queue (int): The ID of the task queue the instance is
                running on.
            task_type (int): The ID of the task type for the instance.
            datetime_created (:class:`datetime.datetime`): The datetime
                when the task instance was created.
            datetime_finished (:class:`datetime.datetime`): The datetime
                when the task instance finished.
            arguments (dict): The arguments the task instance was run
                with.
            manager (:class:`saltant.models.base_task_instance.BaseTaskInstanceManager`):
                The task instance manager which spawned this task
                instance.
        """
        # Call the parent constructor
        super(BaseTaskInstance, self).__init__(manager)

        # Add in task instance stuff
        self.name = name
        self.uuid = uuid
        self.state = state
        self.user = user
        self.task_queue = task_queue
        self.task_type = task_type
        self.datetime_created = datetime_created
        self.datetime_finished = datetime_finished
        self.arguments = arguments

    def __str__(self):
        """String representation of the task instance."""
        return self.uuid

    def sync(self):
        """Sync this model with latest data on the saltant server.

        Note that in addition to returning the updated object, it also
        updates the existing object.

        Returns:
            :class:`saltant.models.base_task_instance.BaseTaskInstance`:
                This task instance ... instance after syncing.
        """
        self = self.manager.get(uuid=self.uuid)

        return self

    def clone(self):
        """Clone this task instance.

        Returns:
            :class:`saltant.models.base_task_instance.BaseTaskInstance`:
                A task instance model instance representing the task
                instance created due to the clone.
        """
        return self.manager.clone(self.uuid)

    def terminate(self):
        """Terminate this task instance.

        Returns:
            :class:`saltant.models.base_task_instance.BaseTaskInstance`:
                This task instance model after it was told to terminate.
        """
        return self.manager.terminate(self.uuid)

    def wait_until_finished(
        self, refresh_period=DEFAULT_TASK_INSTANCE_WAIT_REFRESH_PERIOD
    ):
        """Wait until a task instance with the given UUID is finished.

        Args:
            refresh_period (int, optional): How many seconds to wait
                before checking the task's status. Defaults to 5
                seconds.

        Returns:
            :class:`saltant.models.base_task_instance.BaseTaskInstance`:
                This task instance model after it finished.
        """
        return self.manager.wait_until_finished(
            uuid=self.uuid, refresh_period=refresh_period
        )


class BaseTaskInstanceManager(ModelManager):
    """Base manager for task instances.

    Attributes:
        _client (:class:`saltant.client.Client`): An authenticated
            saltant client.
        list_url (str): The URL to list task instances.
        detail_url (str): The URL format to get specific task instances.
        clone_url (str): The URL format to clone a task instance.
        terminate_url (str): The URL format to terminate a task
            instance.
        model (:class:`saltant.models.resource.Model`): The model of the
            task instance being used.
    """

    clone_url = "NotImplemented"
    terminate_url = "NotImplemented"
    model = BaseTaskInstance

    def get(self, uuid):
        """Get the task instance with given UUID.

        Args:
            uuid (str): The UUID of the task instance to get.

        Returns:
            :class:`saltant.models.base_task_instance.BaseTaskInstance`:
                A task instance model instance representing the task
                instance requested.
        """
        # Basically identical to parent get method, except re-name id
        # to uuid
        return super(BaseTaskInstanceManager, self).get(id=uuid)

    def create(self, task_type_id, task_queue_id, arguments=None, name=""):
        """Create a task instance.

        Args:
            task_type_id (int): The ID of the task type to base the task
                instance on.
            task_queue_id (int): The ID of the task queue to run the job
                on.
            arguments (dict, optional): The arguments to give the task
                type.
            name (str, optional): A non-unique name to give the task
                instance.

        Returns:
            :class:`saltant.models.base_task_instance.BaseTaskInstance`:
                A task instance model instance representing the task
                instance just created.
        """
        # Make arguments an empty dictionary if None
        if arguments is None:
            arguments = {}

        # Create the object
        request_url = self._client.base_api_url + self.list_url
        data_to_post = {
            "name": name,
            "arguments": json.dumps(arguments),
            "task_type": task_type_id,
            "task_queue": task_queue_id,
        }

        response = self._client.session.post(request_url, data=data_to_post)

        # Validate that the request was successful
        self.validate_request_success(
            response_text=response.text,
            request_url=request_url,
            status_code=response.status_code,
            expected_status_code=HTTP_201_CREATED,
        )

        # Return a model instance representing the task instance
        return self.response_data_to_model_instance(response.json())

    def clone(self, uuid):
        """Clone the task instance with given UUID.

        Args:
            uuid (str): The UUID of the task instance to clone.

        Returns:
            :class:`saltant.models.base_task_instance.BaseTaskInstance`:
                A task instance model instance representing the task
                instance created due to the clone.
        """
        # Clone the object
        request_url = self._client.base_api_url + self.clone_url.format(
            id=uuid
        )

        response = self._client.session.post(request_url)

        # Validate that the request was successful
        self.validate_request_success(
            response_text=response.text,
            request_url=request_url,
            status_code=response.status_code,
            expected_status_code=HTTP_201_CREATED,
        )

        # Return a model instance
        return self.response_data_to_model_instance(response.json())

    def clone_many(self, uuids):
        """Clone the task instances with given UUIDs.

        Args:
            uuids (list): A list of strings containing the UUIDs of the
                task instances to clone.

        Returns:
            list:
                A list of
                :class:`saltant.models.base_task_instance.BaseTaskInstance`
                subclass instances representing the task instances
                created due to the clone.
        """
        return [self.clone(uuid) for uuid in uuids]

    def terminate(self, uuid):
        """Terminate the task instance with given UUID.

        Args:
            uuid (str): The UUID of the task instance to terminate.

        Returns:
            :class:`saltant.models.base_task_instance.BaseTaskInstance`:
                A task instance model instance representing the task
                instance that was told to terminate.
        """
        # Clone the object
        request_url = self._client.base_api_url + self.terminate_url.format(
            id=uuid
        )

        response = self._client.session.post(request_url)

        # Validate that the request was successful
        self.validate_request_success(
            response_text=response.text,
            request_url=request_url,
            status_code=response.status_code,
            expected_status_code=HTTP_202_ACCEPTED,
        )

        # Return a model instance
        return self.response_data_to_model_instance(response.json())

    def terminate_many(self, uuids):
        """Terminate the task instances with given UUIDs.

        Args:
            uuids (list): A list of strings containing the UUIDs of the
                task instances to terminate.

        Returns:
            list:
                A list of
                :class:`saltant.models.base_task_instance.BaseTaskInstance`
                instances representing the task instances told to
                terminate.
        """
        return [self.terminate(uuid) for uuid in uuids]

    def wait_until_finished(
        self, uuid, refresh_period=DEFAULT_TASK_INSTANCE_WAIT_REFRESH_PERIOD
    ):
        """Wait until a task instance with the given UUID is finished.

        Args:
            uuid (str): The UUID of the task instance to wait for.
            refresh_period (float, optional): How many seconds to wait
                in between checking the task's status. Defaults to 5
                seconds.

        Returns:
            :class:`saltant.models.base_task_instance.BaseTaskInstance`:
                A task instance model instance representing the task
                instance which we waited for.
        """
        # Wait for the task to finish
        task_instance = self.get(uuid)

        while task_instance.state not in TASK_INSTANCE_FINISH_STATUSES:
            # Wait a bit
            time.sleep(refresh_period)

            # Query again
            task_instance = self.get(uuid)

        return task_instance

    def response_data_to_model_instance(self, response_data):
        """Convert response data to a task instance model.

        Args:
            response_data (dict): The data from the request's response.

        Returns:
            :class:`saltant.models.base_task_instance.BaseTaskInstance`:
                A task instance model instance representing the task
                instance from the reponse data.
        """
        # Coerce datetime strings into datetime objects
        response_data["datetime_created"] = dateutil.parser.parse(
            response_data["datetime_created"]
        )

        if response_data["datetime_finished"]:
            response_data["datetime_finished"] = dateutil.parser.parse(
                response_data["datetime_finished"]
            )

        # Instantiate a model for the task instance
        return super(
            BaseTaskInstanceManager, self
        ).response_data_to_model_instance(response_data)
