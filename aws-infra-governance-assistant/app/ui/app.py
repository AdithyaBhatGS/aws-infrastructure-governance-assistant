import streamlit as st
from api import (
    get_stacks,
    get_latest_drift,
    discover_resources
)
from datetime import datetime, timezone
from utils import format_elapsed_time
st.set_page_config(
    page_title="Infrastructure Platform Assistant",
    layout="wide"
)

st.title("Infrastructure Platform Assistant")

st.write(
    "AWS infrastructure monitoring and governance dashboard"
)

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Drift Detection",
        "Resource Discovery",
        "History"
    ]
)

st.write(f"Current page: {page}")

if page == "Dashboard":
    st.header("Infrastructure Dashboard")

    stacks = get_stacks()
    drift = get_latest_drift()
    drift_results = drift.get("Results", [])
    drift_status_map = {
        result["stack_name"]: result["status"]
        for result in drift_results
    }

    stack_rows = []

    for stack in stacks.get("stacks", []):
        stack_name = stack["stack_name"]

        stack_rows.append(
            {
                "Stack Name": stack_name,
                "Stack Status": stack["status"],
                "Drift Status": drift_status_map.get(
                    stack_name,
                    "NOT_SCANNED"
                )
            }
        )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Stacks",
            stacks.get("count")
        )

    with col2:
        st.metric(
            "Infrastructure Status:",
            drift.get("AccountStatus")
        )

    with col3:
        st.metric(
            "Drifted Stacks:",
            drift.get("DriftedStacks")
        )

    st.subheader("CloudFormation Stacks")

    st.dataframe(
        stack_rows,
        width="stretch"
    )

    scan_time = drift.get("ScanTime")

    if scan_time:
        st.caption(
            f"Last drift scan: {format_elapsed_time(scan_time)}"
        )
    else:
        st.caption(
            "Last drift scanned: Not scanned"
        )

elif page == "Resource Discovery":
    st.header("Resource Discovery")

    if st.button("Run Resource Discovery"):

        result = discover_resources()

        recommendations = result.get(
            "recommendations",
            []
        )

        warnings = result.get(
            "warnings",
            []
        )

        st.write(
            f"Recommendations: {len(recommendations)}"
        )

        st.write(
            f"Warnings: {len(warnings)}"
        )

        if recommendations:

            st.subheader("Recommendations")

            st.dataframe(
                recommendations,
                width="stretch"
            )

        if warnings:

            st.subheader("Warnings")

            st.dataframe(
                warnings,
                width="stretch"
            )