"""Contains constants for the program."""

# How many seconds to wait for a request response
DEFAULT_TIMEOUT_SECONDS = 90


# What refresh period to use in seconds when waiting for task instances
# to finish
DEFAULT_TASK_INSTANCE_WAIT_REFRESH_PERIOD = 5


# Useful HTTP status codes (nice and verbose :D)
HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_202_ACCEPTED = 202


# Options for the task instance's state field
CREATED = "created"
PUBLISHED = "published"
RUNNING = "running"
SUCCESSFUL = "successful"
FAILED = "failed"
TERMINATED = "terminated"

TASK_INSTANCE_FINISH_STATUSES = (SUCCESSFUL, FAILED, TERMINATED)
