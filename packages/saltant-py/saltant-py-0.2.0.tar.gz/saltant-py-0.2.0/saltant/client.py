"""Contains the saltant API client."""

# TODO(mwiens91): add support for JWT auth tokens

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import functools
import os
import requests
from saltant.constants import DEFAULT_TIMEOUT_SECONDS, HTTP_200_OK
from saltant.exceptions import AuthenticationError, BadEnvironmentError
from saltant.models.container_task_instance import ContainerTaskInstanceManager
from saltant.models.container_task_type import ContainerTaskTypeManager
from saltant.models.executable_task_instance import (
    ExecutableTaskInstanceManager,
)
from saltant.models.executable_task_type import ExecutableTaskTypeManager
from saltant.models.task_queue import TaskQueueManager
from saltant.models.user import UserManager


class Client:
    """API client for communicating with a saltant server.

    Example:

        >>> from saltant.client import Client
        >>> client = Client(
        ...     base_api_url='https://shahlabjobs.ca/api/',
        ...     auth_token='p0gch4mp101fy451do9uod1s1x9i4a')

    Attributes:
        base_api_url (str): The URL of the saltant API.
        session (:class:`requests.Session`): A session object to make
            requests with.
        container_task_instances (:class:`saltant.models.container_task_instance.ContainerTaskInstanceManager`):
            A manager for performing actions related to container task
            instances.
        container_task_types (:class:`saltant.models.container_task_type.ContainerTaskTypeManager`):
            A manager for performing actions related to container task
            types.
        executable_task_instances (:class:`saltant.models.executable_task_instance.ExecutableTaskInstanceManager`):
            A manager for performing actions related to executable task
            instances.
        executable_task_types (:class:`saltant.models.executable_task_type.ExecutableTaskTypeManager`):
            A manager for performing actions related to executable task
            types.
        task_queues (:class:`saltant.models.task_queues.TaskQueueManager`):
            A manager for performing actions related to task queues.
        users (:class:`saltant.models.user.UserManager`):
            A manager for performing actions related to users.
    """

    def __init__(
        self,
        base_api_url,
        auth_token,
        default_timeout=DEFAULT_TIMEOUT_SECONDS,
        test_if_authenticated=True,
    ):
        """Initialize the saltant API client.

        Args:
            base_api_url (str): The URL of the saltant API.
            auth_token (str): The registered user's authentication token.
            default_timeout (int, optional): The maximum number
                of seconds to wait for a request to complete. Defaults
                to 90 seconds.
            test_if_authenticated (bool, optional): A flag signalling
                whether to try making a read-only authenticated request
                when initializing the client. This is useful for
                ensuring a working connection and correct authentication
                details as soon as possible. Defaults to True.
        """
        # The base URL of the saltant API
        self.base_api_url = base_api_url

        # Start a requests session
        self.session = requests.Session()
        self.session.headers.update({"Authorization": "Token " + auth_token})

        # Test that we're authorized
        if test_if_authenticated:
            self.test_authentication()

        # Record the default timeout we want
        self.session.request = functools.partial(
            self.session.request, timeout=default_timeout
        )

        # Add in model managers
        self.container_task_instances = ContainerTaskInstanceManager(
            _client=self
        )
        self.container_task_types = ContainerTaskTypeManager(_client=self)
        self.executable_task_instances = ExecutableTaskInstanceManager(
            _client=self
        )
        self.executable_task_types = ExecutableTaskTypeManager(_client=self)
        self.task_queues = TaskQueueManager(_client=self)
        self.users = UserManager(_client=self)

    def test_authentication(self):
        """Test that the client is authorized.

        This currently assumes that read-only operations require
        authentication, which is the intended authentication protocol
        for saltant servers.

        Raises:
            :class:`saltant.exceptions.AuthenticationError`: The
                authentication provided was invalid.
        """
        response = self.session.get(self.base_api_url + "users/")

        try:
            assert response.status_code == HTTP_200_OK
        except AssertionError:
            raise AuthenticationError("Authentication invalid!")

    @classmethod
    def from_env(cls, default_timeout=DEFAULT_TIMEOUT_SECONDS):
        """Return a client configured from environment variables.

        Essentially copying this:
        https://github.com/docker/docker-py/blob/master/docker/client.py#L43.

        The environment variables looked for are the following:

        .. envvar:: SALTANT_API_URL

            The URL of the saltant API. For example,
            https://shahlabjobs.ca/api/.

        .. envvar:: SALTANT_AUTH_TOKEN

            The registered saltant user's authentication token.

        Example:

            >>> from saltant.client import from_env
            >>> client = from_env()

        Args:
            default_timeout (int, optional): The maximum number of
                seconds to wait for a request to complete. Defaults to
                90 seconds.

        Returns:
            :class:`Client`: A saltant API client object.

        Raises:
            :class:`saltant.exceptions.BadEnvironmentError`: The user
                has an incorrectly configured environment.
        """
        # Get variables from environment
        try:
            base_api_url = os.environ["SALTANT_API_URL"]
        except KeyError:
            raise BadEnvironmentError("SALTANT_API_URL not defined!")

        try:
            # Try to get an auth token
            auth_token = os.environ["SALTANT_AUTH_TOKEN"]
        except KeyError:
            raise BadEnvironmentError("SALTANT_AUTH_TOKEN not defined!")

        # Return the configured client
        return cls(
            base_api_url=base_api_url,
            auth_token=auth_token,
            default_timeout=default_timeout,
        )


# Allow convenient import access to environment-configured client
from_env = Client.from_env
