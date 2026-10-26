import re
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="Web Server Log Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_FILE = BASE_DIR / "results" / "part-r-00000"

# Previously recorded Hadoop execution statistics
INPUT_RECORDS = 726739
MAP_OUTPUT_RECORDS = 2166993
REDUCE_OUTPUT_RECORDS = 11807
MALFORMED_LINES = 4408

# Reference counts from the previous analysis.
# Verify against the actual reducer output before final submission.
REFERENCE_STATUS = {
    "200 OK": 566192,
    "302 Found": 30260,
    "304 Not Modified": 97560,
    "400 Bad Request": 13,
    "401 Unauthorized": 46,
    "403 Forbidden": 4740,
    "404 Not Found": 23435,
    "500 Internal Server Error": 42,
    "501 Not Implemented": 43,
}

REFERENCE_METHODS = {
    "GET": 721661,
    "HEAD": 567,
    "POST": 103,
}


@st.cache_data(show_spinner=False)
def load_output(path, modified):
    file = Path(path)

    if not file.exists():
        return pd.DataFrame(columns=["Key", "Value", "Raw"])

    rows = []

    for line in file.read_text(errors="replace").splitlines():
        if not line.strip() or line.startswith("_"):
            continue

        parts = line.split("\t", 1)
        key = parts[0].strip()
        value = parts[1].strip() if len(parts) > 1 else ""

        rows.append({
            "Key": key,
            "Value": value,
            "Raw": line,
        })

    return pd.DataFrame(rows)


output_modified = OUTPUT_FILE.stat().st_mtime if OUTPUT_FILE.exists() else 0
output_df = load_output(str(OUTPUT_FILE), output_modified)


# Attempt to identify status counts from actual reducer keys.
def detect_status_counts(df):
    found = {}

    for _, row in df.iterrows():
        key = str(row["Key"])
        value = str(row["Value"])

        status_match = re.search(
            r"(?<!\d)(200|302|304|400|401|403|404|500|501)(?!\d)",
            key,
        )

        count_match = re.search(r"\d[\d,]*", value)

        if (
            status_match
            and count_match
            and re.search(r"status|http|code|response", key, re.I)
        ):
            found[status_match.group(1)] = int(
                count_match.group(0).replace(",", "")
            )

    return found


def detect_method_counts(df):
    found = {}

    for _, row in df.iterrows():
        key = str(row["Key"])
        value = str(row["Value"])

        method_match = re.search(
            r"\b(GET|POST|HEAD|PUT|DELETE|OPTIONS|PATCH)\b",
            key,
            re.I,
        )

        count_match = re.search(r"\d[\d,]*", value)

        if (
            method_match
            and count_match
            and re.search(r"method|request", key, re.I)
        ):
            found[method_match.group(1).upper()] = int(
                count_match.group(0).replace(",", "")
            )

    return found


detected_status = detect_status_counts(output_df)
detected_methods = detect_method_counts(output_df)

status_counts = detected_status or REFERENCE_STATUS
method_counts = detected_methods or REFERENCE_METHODS

status_source = (
    "Local Hadoop output"
    if detected_status
    else "Previously recorded reference counts"
)

method_source = (
    "Local Hadoop output"
    if detected_methods
    else "Previously recorded reference counts"
)

status_df = pd.DataFrame([
    {"Status": key, "Requests": value}
    for key, value in status_counts.items()
])

if not status_df.empty:
    status_df["Code"] = status_df["Status"].str.extract(
        r"(\d{3})",
        expand=False,
    )

    status_df["Category"] = status_df["Code"].str[0].map({
        "2": "Success",
        "3": "Redirect",
        "4": "Client Error",
        "5": "Server Error",
    }).fillna("Other")

    status_total = status_df["Requests"].sum()

    status_df["Percentage"] = (
        status_df["Requests"] / status_total * 100
    ).round(2)

method_df = pd.DataFrame([
    {"Method": key, "Requests": value}
    for key, value in method_counts.items()
])

if not method_df.empty:
    method_total = method_df["Requests"].sum()

    method_df["Percentage"] = (
        method_df["Requests"] / method_total * 100
    ).round(3)


# Sidebar navigation
with st.sidebar:
    st.title("⚡ Navigation")

    page = st.radio(
        "Select View",
        [
            "Executive Dashboard",
            "HTTP Status Codes",
            "Request Methods",
            "Hadoop Pipeline & S3",
            "Dataset Information",
            "Data Explorer",
        ],
    )

    st.divider()

    st.subheader("🎓 Academic PBL Details")
    st.write("Domain: Big Data Analytics")
    st.write("Processing: Hadoop MapReduce")
    st.write("Storage: Amazon S3")
    st.write("Dashboard: Streamlit")

    st.divider()

    if OUTPUT_FILE.exists():
        st.success("Hadoop output file found")
    else:
        st.warning("Local reducer output not found")


# Main heading
st.title("📊 Web Server Log Analytics Dashboard")

st.subheader("Hadoop MapReduce-Based Web Server Log Analysis")

st.caption(
    "Dataset: Calgary Access Log | "
    "Processing: Hadoop MapReduce | "
    "Storage: Amazon S3"
)


# Executive Dashboard
if page == "Executive Dashboard":

    st.header("📈 Pipeline Execution & Analytics Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Input Records", f"{INPUT_RECORDS:,}")
    col2.metric("Map Output Records", f"{MAP_OUTPUT_RECORDS:,}")
    col3.metric("Reduce Output Records", f"{REDUCE_OUTPUT_RECORDS:,}")
    col4.metric("Malformed Lines", f"{MALFORMED_LINES:,}")

    st.divider()

    st.subheader("HTTP Response Analysis")

    left, right = st.columns(2)

    with left:
        if not status_df.empty:
            fig = px.bar(
                status_df.sort_values("Requests"),
                x="Requests",
                y="Status",
                color="Category",
                orientation="h",
                text="Requests",
                title="HTTP Response Counts",
            )

            st.plotly_chart(fig, use_container_width=True)

    with right:
        if not status_df.empty:
            category_df = status_df.groupby(
                "Category",
                as_index=False,
            )["Requests"].sum()

            fig = px.pie(
                category_df,
                names="Category",
                values="Requests",
                hole=0.5,
                title="Response Category Distribution",
            )

            st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.subheader("HTTP Request Methods")

    if not method_df.empty:
        columns = st.columns(min(4, len(method_df)))

        for col, (_, row) in zip(columns, method_df.iterrows()):
            col.metric(
                str(row["Method"]),
                f'{int(row["Requests"]):,}',
            )

        fig = px.bar(
            method_df,
            x="Method",
            y="Requests",
            text="Requests",
            title="Requests by Method",
        )

        st.plotly_chart(fig, use_container_width=True)

    if not detected_status:
        st.warning(
            "HTTP status counts are reference figures, not yet verified "
            "against the actual reducer output."
        )

    if not detected_methods:
        st.warning(
            "Request-method counts are reference figures, not yet verified "
            "against the actual reducer output."
        )


# HTTP Status Codes
elif page == "HTTP Status Codes":

    st.header("HTTP Status Code Analysis")

    st.caption(f"Data source: {status_source}")

    selected = st.multiselect(
        "Filter status codes",
        status_df["Status"].tolist(),
        default=status_df["Status"].tolist(),
    )

    filtered = status_df[
        status_df["Status"].isin(selected)
    ]

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Displayed Requests",
        f'{int(filtered["Requests"].sum()):,}',
    )

    col2.metric("Selected Status Codes", len(filtered))

    col3.metric(
        "Response Categories",
        filtered["Category"].nunique(),
    )

    fig = px.bar(
        filtered,
        x="Status",
        y="Requests",
        color="Category",
        text="Requests",
        title="HTTP Response Counts by Status Code",
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Status Code Summary")

    st.dataframe(
        filtered,
        use_container_width=True,
        hide_index=True,
    )

    st.download_button(
        "Download Status Summary CSV",
        filtered.to_csv(index=False),
        "http_status_summary.csv",
        "text/csv",
    )


# Request Methods
elif page == "Request Methods":

    st.header("HTTP Request Method Analysis")

    st.caption(f"Data source: {method_source}")

    left, right = st.columns(2)

    with left:
        fig = px.pie(
            method_df,
            names="Method",
            values="Requests",
            hole=0.45,
            title="Request Method Distribution",
        )

        st.plotly_chart(fig, use_container_width=True)

    with right:
        fig = px.bar(
            method_df,
            x="Method",
            y="Requests",
            text="Requests",
            title="Request Counts by Method",
        )

        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Method Summary")

    st.dataframe(
        method_df,
        use_container_width=True,
        hide_index=True,
    )

    st.download_button(
        "Download Method Summary CSV",
        method_df.to_csv(index=False),
        "request_method_summary.csv",
        "text/csv",
    )


# Hadoop Pipeline and S3
elif page == "Hadoop Pipeline & S3":

    st.header("Hadoop MapReduce Pipeline")

    st.markdown("""
    **Processing workflow**

    1. Load the Calgary web server access log.
    2. Parse web server log records in the Mapper.
    3. Emit intermediate key-value pairs.
    4. Shuffle and sort intermediate data.
    5. Aggregate keys and counts in the Reducer.
    6. Write results to the Hadoop output location.
    7. Visualize available analysis results using Streamlit.
    """)

    st.subheader("Recorded Processing Statistics")

    col1, col2 = st.columns(2)

    col1.metric("Map Input Records", f"{INPUT_RECORDS:,}")
    col1.metric("Map Output Records", f"{MAP_OUTPUT_RECORDS:,}")

    col2.metric("Reduce Output Records", f"{REDUCE_OUTPUT_RECORDS:,}")
    col2.metric("Malformed Lines", f"{MALFORMED_LINES:,}")

    st.subheader("Amazon S3 Locations")

    st.code(
        "Input:\n"
        "s3://bda-web-log-analysis-rohitsasmal-2026/input/full-data/calgary_access_log.gz\n\n"
        "Output:\n"
        "s3://bda-web-log-analysis-rohitsasmal-2026/output/calgary-full-analysis-001/",
        language="text",
    )

    st.info(
        "The recorded Hadoop job ran in local execution mode using S3 "
        "for input and output. This is not a multi-node Hadoop cluster."
    )


# Dataset Information
elif page == "Dataset Information":

    st.header("Dataset Information")

    st.subheader("Calgary Access Log")

    st.write(
        "The project analyses compressed web server access logs using "
        "a Hadoop MapReduce program."
    )

    st.subheader("Recorded Dataset Details")

    dataset_df = pd.DataFrame([
        {"Metric": "Input Records", "Value": f"{INPUT_RECORDS:,}"},
        {"Metric": "Map Output Records", "Value": f"{MAP_OUTPUT_RECORDS:,}"},
        {"Metric": "Reduce Output Records", "Value": f"{REDUCE_OUTPUT_RECORDS:,}"},
        {"Metric": "Malformed Lines", "Value": f"{MALFORMED_LINES:,}"},
        {"Metric": "Compressed Dataset Size", "Value": "Approximately 5.4 MB"},
        {"Metric": "Uncompressed Dataset Size", "Value": "Approximately 52.3 MB"},
    ])

    st.dataframe(
        dataset_df,
        use_container_width=True,
        hide_index=True,
    )

    st.subheader("Hadoop Output Files")

    st.write("`_SUCCESS` — indicates successful completion of the output job.")
    st.write("`part-r-00000` — contains reducer output records.")


# Data Explorer
elif page == "Data Explorer":

    st.header("Hadoop Reducer Output Explorer")

    if output_df.empty:

        st.warning(
            "The local reducer output file was not found at "
            "results/part-r-00000."
        )

        st.write(
            "Copy your actual Hadoop part-r-00000 file into the "
            "project's results folder and refresh this page."
        )

        st.code(
            "mkdir -p results\n"
            "# Place the actual part-r-00000 file in results/",
            language="bash",
        )

    else:

        st.success(
            f"Loaded {len(output_df):,} rows from the actual reducer output."
        )

        search = st.text_input("Search reducer output")

        filtered = output_df.copy()

        if search:
            mask = (
                filtered["Key"].str.contains(
                    search,
                    case=False,
                    na=False,
                )
                |
                filtered["Raw"].str.contains(
                    search,
                    case=False,
                    na=False,
                )
            )

            filtered = filtered[mask]

        st.caption(
            f"Showing {len(filtered):,} of {len(output_df):,} rows"
        )

        st.dataframe(
            filtered[["Key", "Value"]],
            use_container_width=True,
            hide_index=True,
            height=500,
        )

        st.download_button(
            "Download Filtered Output CSV",
            filtered[["Key", "Value"]].to_csv(index=False),
            "hadoop_reducer_output.csv",
            "text/csv",
        )

        with st.expander("Preview Raw Hadoop Output"):
            st.text("\n".join(filtered["Raw"].head(100).tolist()))


st.divider()

st.caption(
    "Web Server Log Analysis Using Hadoop | "
    "Big Data Analytics Academic Project"
)