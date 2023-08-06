"""Contains base classes for models and related classes."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from saltant.exceptions import BadHttpRequestError
from saltant.constants import HTTP_200_OK


class Model(object):
    """Base class for representing a model.

    Attributes:
        manager (:class:`saltant.models.resource.Manager`):
            The manager which spawned this model instance.
    """

    def __init__(self, manager):
        """Initialize the model.

        Args:
            manager (:class:`saltant.models.resource.Manager`):
                The manager which spawned this model instance.
        """
        self.manager = manager


class ModelManager(object):
    """Base class for a model manager.

    Attributes:
        _client (:class:`saltant.client.Client`): An authenticated
            saltant client.
        list_url (str): The URL to list models.
        detail_url (str): The URL format to get specific models.
        model (:class:`saltant.models.resource.Model`): The model
            being used.
    """

    list_url = "NotImplemented"
    detail_url = "NotImplemented"
    model = Model

    def __init__(self, _client):
        """Save the client so we can make API calls in the manager.

        Args:
            _client (:class:`saltant.client.Client`): An
                authenticated saltant client.
        """
        self._client = _client

    def list(self, filters=None):
        """List model instances.

        Currently this gets *everything* and iterates through all
        possible pages in the API. This may be unsuitable for production
        environments with huge databases, so finer grained page support
        should likely be added at some point.

        Args:
            filters (dict, optional): API query filters to apply to the
                request. For example:

                .. code-block:: python

                    {'name__startswith': 'azure',
                     'user__in': [1, 2, 3, 4],}

                See saltant's API reference at
                https://saltant-org.github.io/saltant/ for each model's
                available filters.

        Returns:
            list:
                A list of :class:`saltant.models.resource.Model`
                subclass instances (for example, container task type
                model instances).
        """
        # Add in the page and page_size parameters to the filter, such
        # that our request gets *all* objects in the list. However,
        # don't do this if the user has explicitly included these
        # parameters in the filter.
        if not filters:
            filters = {}

        if "page" not in filters:
            filters["page"] = 1

        if "page_size" not in filters:
            # The below "magic number" is 2^63 - 1, which is the largest
            # number you can hold in a 64 bit integer. The main point
            # here is that we want to get everything in one page (unless
            # otherwise specified, of course).
            filters["page_size"] = 9223372036854775807

        # Form the request URL - first add in the query filters
        query_filter_sub_url = ""

        for idx, filter_param in enumerate(filters):
            # Prepend '?' or '&'
            if idx == 0:
                query_filter_sub_url += "?"
            else:
                query_filter_sub_url += "&"

            # Add in the query filter
            query_filter_sub_url += "{param}={val}".format(
                param=filter_param, val=filters[filter_param]
            )

        # Stitch together all sub-urls
        request_url = (
            self._client.base_api_url + self.list_url + query_filter_sub_url
        )

        # Make the request
        response = self._client.session.get(request_url)

        # Validate that the request was successful
        self.validate_request_success(
            response_text=response.text,
            request_url=request_url,
            status_code=response.status_code,
            expected_status_code=HTTP_200_OK,
        )

        # Return a list of model instances
        return self.response_data_to_model_instances_list(response.json())

    def get(self, id):
        """Get the model instance with a given id.

        Args:
            id (int or str): The primary identifier (e.g., pk or UUID)
                for the task instance to get.

        Returns:
            :class:`saltant.models.resource.Model`:
                A :class:`saltant.models.resource.Model` subclass
                instance representing the resource requested.
        """
        # Get the object
        request_url = self._client.base_api_url + self.detail_url.format(id=id)

        response = self._client.session.get(request_url)

        # Validate that the request was successful
        self.validate_request_success(
            response_text=response.text,
            request_url=request_url,
            status_code=response.status_code,
            expected_status_code=HTTP_200_OK,
        )

        # Return a model instance
        return self.response_data_to_model_instance(response.json())

    def response_data_to_model_instance(self, response_data):
        """Convert get response data to a model.

        Args:
            response_data (dict): The data from the request's response.

        Returns:
            :class:`saltant.models.resource.Model`:
                A :class:`saltant.models.resource.Model` subclass
                instance representing the resource given in the
                request's response data.
        """
        # Add in this manager to the data
        response_data["manager"] = self

        # Instantiate a model
        return self.model(**response_data)

    def response_data_to_model_instances_list(self, response_data):
        """Convert list response data to a list of models.

        Args:
            response_data (dict): The data from the request's response.

        Returns:
            list:
                A list of :class:`saltant.models.resource.Model`
                subclass instances.
        """
        return [
            self.response_data_to_model_instance(subdata)
            for subdata in response_data["results"]
        ]

    @staticmethod
    def validate_request_success(
        response_text, request_url, status_code, expected_status_code
    ):
        """Validates that a request was successful.

        Args:
            response_text (str): The response body of the request.
            request_url (str): The URL the request was made at.
            status_code (int): The status code of the response.
            expected_status_code (int): The expected status code of the
                response.

        Raises:
            :class:`saltant.exceptions.BadHttpRequestError`: The HTTP
                request failed.
        """
        try:
            assert status_code == expected_status_code
        except AssertionError:
            msg = (
                "Request to {url} failed with status {status_code}:\n"
                "The reponse from the request was as follows:\n\n"
                "{content}"
            ).format(
                url=request_url, status_code=status_code, content=response_text
            )
            raise BadHttpRequestError(msg)
