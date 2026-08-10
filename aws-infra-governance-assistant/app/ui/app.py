import streamlit as st
from api import (
    get_stacks,
    get_latest_drift,
    discover_resources,
    analyze_account_drift,
    analyze_stack_drift
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
        "Account Drift Detection",
        "Stack Drift",
        "Resource Discovery",
        "History"
    ]
)

# st.write(f"Current page: {page}")

if page == "Dashboard":
    st.header("Infrastructure Dashboard")

    with st.spinner("Loading Infrastructure Status..."):
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

    st.info(
        "Resource discovery queries AWS directly across supported "
        "resources and may take a few seconds. Results are not cached."
    )

    if st.button("Run Resource Discovery"):

        with st.spinner("Scanning AWS resources..."):
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

elif page == "Account Drift Detection":
    st.header("Account Drift Detection")

    st.info(
        "Runs a fresh drift detection across the account. "
        "This may take a few minutes."
    )

    if st.button("Analyze Account Drift:"):

        with st.spinner("Analyzing Account Drift..."):
            result = analyze_account_drift()

        st.write(
            f"Account Status: {result.get("account_status")}"
        )

        st.write(
            f"Total Stacks: {result.get("total_stacks")}"
        )

        st.write(
            f"Drifted Stacks: {result.get("drifted_stacks")}"
        )

        stack_results = result.get("results", [])

        display_results = []

        for stack in stack_results:

            row = {
                "Stack Name": stack.get("stack_name"),
                "Status": stack.get("status")
            }

            if stack.get("status") == "FAILED":
                row["Reason"] = stack.get(
                    "reason",
                    "Unknown error"
                )

            else:
                row["Detection ID"] = stack.get(
                    "detection_id"
                )

                row["Drifted Resource Count"] = len(
                    stack.get("resources", [])
                )

            display_results.append(row)

        st.dataframe(
            display_results,
            width="stretch"
        )

        for stack in stack_results:

            if stack.get("status") == "DRIFTED":

                with st.expander(
                    f"Resource drift - {stack.get('stack_name')}"
                ):

                    st.json(
                        stack.get("resources", [])
                    )

            if stack.get("status") == "FAILED":

                with st.expander(
                    f"Failure details - {stack.get('stack_name')}"
                ):

                    st.write(
                        stack.get(
                            "reason",
                            "Unknown error"
                        )
                    )

elif page == "Stack Drift":
    st.header("Stack Drift Detection")

    st.info(
        "Runs a fresh drift detection for the selected "
        "CloudFormation stack. This may take a few minutes."
    )

    stacks = get_stacks()

    stack_list = stacks.get("stacks", [])

    stack_names = [
        stack["stack_name"]
        for stack in stack_list
    ]

    if stack_names:

        selected_stack = st.selectbox(
            "Select a stack",
            stack_names
        )

        if st.button("Analyze Stack Drift"):

            with st.spinner(f"Analyzing drift for {selected_stack}..."):
                result = analyze_stack_drift(
                    selected_stack
                )

            st.write(
                f"Stack: {result.get('stack_name')}"
            )

            st.write(
                f"Status: {result.get('status')}"
            )

            if result.get("status") == "FAILED":

                st.error(
                    result.get(
                        "reason",
                        "Drift detection failed."
                    )
                )

            else:
                st.write(
                    f"Detection ID: {result.get('detection_id')}"
                )

                resources = result.get(
                    "resources",
                    []
                )

                st.write(
                    f"Drifted Resources: {len(resources)}"
                )

                if resources:

                    with st.expander("Resource drift details:"):

                        st.json(resources)
    else:
        st.info("No cloudformation stacks found.")



