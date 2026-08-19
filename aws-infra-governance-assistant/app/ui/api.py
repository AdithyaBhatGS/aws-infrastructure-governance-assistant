import requests
import time
import streamlit as st

BASE_URL = "http://localhost:8000"

@st.cache_data(ttl=30)
def get_stacks():

    response = requests.get(
        f"{BASE_URL}/stacks/list"
    )

    response.raise_for_status()

    return response.json()

@st.cache_data(ttl=30)
def get_latest_drift():

    response = requests.get(
        f"{BASE_URL}/drift/latest"
    )

    response.raise_for_status()

    return response.json()

def discover_resources():

    response = requests.get(
        f"{BASE_URL}/resource_discovery"
    )

    response.raise_for_status()

    return response.json()

def analyze_account_drift():
    response = requests.post(
        f"{BASE_URL}/drift/analyze/account"
    )

    response.raise_for_status()

    return response.json()

def analyze_stack_drift(stack_name):
    response = requests.post(
        f"{BASE_URL}/drift/analyze/stack/{stack_name}"
    )

    response.raise_for_status()

    return response.json()

def get_drift_history():
    response = requests.get(
        f"{BASE_URL}/drift/history"
    )

    response.raise_for_status()

    return response.json()