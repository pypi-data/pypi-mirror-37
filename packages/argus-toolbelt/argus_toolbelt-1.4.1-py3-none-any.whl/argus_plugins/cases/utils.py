"""This is a helper module for all things case related"""
import time
from datetime import datetime

from argus_api.api.customers.v1.customer import get_customer_by_shortname

STATUSES = ["pendingCustomer", "pendingSoc", "pendingVendor", "workingSoc", "workingCustomer", "pendingClose", "closed"]
CASE_TYPES = ["securityIncident", "operationalIncident", "informational", "change"]
PRIORITIES = ["low", "medium", "high", "critical"]
KEYWORD_FIELDS = ["subject", "description", "comments", "id", "all"]


def get_customer_id(name: str) -> int:
    """Gets a customer's ID from their name

    :param name: The name of the customer
    """
    customers = get_customer_by_shortname(shortName=name.lower())["data"]
    customer_id = customers["id"]  # This might get the wrong customer if there are more with the same name?
    return customer_id
