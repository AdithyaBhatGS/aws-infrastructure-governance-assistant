import requests
import time
import streamlit as st

BASE_URL = "http://localhost:8000"


@st.cache_data(ttl=30)
def get_stacks():
    """Fetch the current list of CloudFormation stacks.

    Returns:
        dict: A JSON payload containing the active stacks and metadata.
    """
    response = requests.get(
        f"{BASE_URL}/stacks/list"
    )

    response.raise_for_status()

    return response.json()


@st.cache_data(ttl=30)
def get_latest_drift():
    """Fetch the most recent drift snapshot for the account.

    Returns:
        dict: A JSON payload containing the latest drift snapshot.
    """
    response = requests.get(
        f"{BASE_URL}/drift/latest"
    )

    response.raise_for_status()

    return response.json()


def discover_resources():
    """Discover AWS resources and recommendations for the current account.

    Returns:
        dict: A JSON payload containing resource findings, warnings, and
            recommendations.
    """
    response = requests.get(
        f"{BASE_URL}/resource_discovery"
    )

    response.raise_for_status()

    return response.json()


def analyze_account_drift():
    """Trigger drift analysis for the entire AWS account.

    Returns:
        dict: A drift summary for the current account.
    """
    response = requests.post(
        f"{BASE_URL}/drift/analyze/account"
    )

    response.raise_for_status()

    return response.json()


def analyze_stack_drift(stack_name):
    """Trigger drift analysis for a specific CloudFormation stack.

    Args:
        stack_name (str): The name of the CloudFormation stack to analyze.

    Returns:
        dict: Drift analysis results for the specified stack.
    """
    response = requests.post(
        f"{BASE_URL}/drift/analyze/stack/{stack_name}"
    )

    response.raise_for_status()

    return response.json()


def get_drift_history():
    """Fetch the historical drift records for the current account.

    Returns:
        list[dict]: A list of historical drift entries.
    """
    response = requests.get(
        f"{BASE_URL}/drift/history"
    )

    response.raise_for_status()

    return response.json()