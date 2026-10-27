from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
import streamlit as st
import pandas as pd
import os
import sys
from datetime import datetime

def speedometer(value, title, unit="Mbps", max_value=100):

    value = float(value)

    if value < 0:
        value = 0

    if value > max_value:
        value = max_value

    percentage = value / max_value

    st.markdown(
        f"""
        <div style="
            background:#111111;
            border-radius:20px;
            padding:20px;
            text-align:center;
            margin:10px 0;
        ">

            <h3 style="color:#dddddd;">
                ⚡ {title}
            </h3>

            <div style="
                width:220px;
                height:110px;
                margin:auto;
                border-radius:220px 220px 0 0;
                background:conic-gradient(
                    #16c7ff {percentage * 50}%,
                    #292944 0
                );
                position:relative;
            ">

                <div style="
                    position:absolute;
                    width:180px;
                    height:90px;
                    background:#111111;
                    border-radius:180px 180px 0 0;
                    left:20px;
                    top:20px;
                ">
                </div>

            </div>

            <div style="
                font-size:40px;
                color:white;
                margin-top:10px;
            ">
                {value:.2f}
            </div>

            <div style="
                font-size:18px;
                color:#999999;
            ">
                {unit}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

# =========================================================
# PATHS
# =========================================================

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

DATA_FILE = os.path.join(
    PROJECT_ROOT,
    "data",
    "raw",
    "network_data.csv"
)

ALGORITHM_PATH = os.path.join(
    PROJECT_ROOT,
    "src",
    "algorithm"
)

if ALGORITHM_PATH not in sys.path:
    sys.path.append(ALGORITHM_PATH)

from scoring import calculate_scores


# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="CAMNS Network Selection System",
    page_icon="📡",
    layout="wide"
)


# =========================================================
# DATA COLUMNS
# =========================================================

COLUMNS = [
    "timestamp",
    "operator",
    "location",
    "signal_dbm",
    "download_mbps",
    "upload_mbps",
    "latency_ms",
    "packet_loss_percent",
    "network_type",
    "device"
]


# =========================================================
# LOAD DATA
# =========================================================

def load_data():

    if os.path.exists(DATA_FILE):

        data = pd.read_csv(DATA_FILE)

        for column in COLUMNS:

            if column not in data.columns:
                data[column] = ""

        return data[COLUMNS]

    return pd.DataFrame(columns=COLUMNS)


# =========================================================
# SAVE DATA
# =========================================================

def save_data(data):

    os.makedirs(
        os.path.dirname(DATA_FILE),
        exist_ok=True
    )

    data.to_csv(
        DATA_FILE,
        index=False
    )


df = load_data()


# =========================================================
# HEADER
# =========================================================

st.title("📡 CAMNS Network Selection System")

st.subheader(
    "Context-Aware Mobile Network Selection and Failover System"
)

st.caption(
    "Mobile network monitoring and intelligent network selection "
    "for weak-signal areas."
)

st.divider()


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("⚙️ CAMNS Control Panel")

menu = st.sidebar.radio(
    "Select Function",
    [
        "📊 Dashboard",
        "➕ Add Measurement",
        "✏️ Edit Measurement",
        "🗑️ Delete Measurement",
        "⚡ Speed Test"
    ]
)

# =========================================================
# ADD MEASUREMENT
# =========================================================

if menu == "➕ Add Measurement":

    st.header("➕ Add New Network Measurement")

    st.info(
        "Enter the measurement collected from your mobile "
        "phone or modem."
    )

    with st.form("add_form"):

        col1, col2 = st.columns(2)

        with col1:

            operator = st.selectbox(
                "Operator",
                [
                    "Dialog",
                    "Mobitel",
                    "Hutch",
                    "Airtel"
                ]
            )

            location = st.text_input(
                "Location",
                placeholder="Example: Home"
            )

            signal = st.number_input(
                "Signal (dBm)",
                min_value=-150.0,
                max_value=0.0,
                value=-90.0
            )

            download = st.number_input(
                "Download (Mbps)",
                min_value=0.0,
                value=0.0
            )

            upload = st.number_input(
                "Upload (Mbps)",
                min_value=0.0,
                value=0.0
            )

        with col2:

            latency = st.number_input(
                "Latency (ms)",
                min_value=0.0,
                value=0.0
            )

            packet_loss = st.number_input(
                "Packet Loss (%)",
                min_value=0.0,
                max_value=100.0,
                value=0.0
            )

            network_type = st.selectbox(
                "Network Type",
                [
                    "4G",
                    "5G",
                    "3G",
                    "Other"
                ]
            )

            device = st.text_input(
                "Device",
                placeholder="Example: Samsung Galaxy A15"
            )

        save_button = st.form_submit_button(
            "💾 Save Measurement"
        )

    if save_button:

        new_record = {
            "timestamp": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "operator": operator,
            "location": location,
            "signal_dbm": signal,
            "download_mbps": download,
            "upload_mbps": upload,
            "latency_ms": latency,
            "packet_loss_percent": packet_loss,
            "network_type": network_type,
            "device": device
        }

        new_row = pd.DataFrame(
            [new_record]
        )

        df = pd.concat(
            [df, new_row],
            ignore_index=True
        )

        save_data(df)

        st.success(
            "✅ Measurement added successfully!"
        )

        st.rerun()


# =========================================================
# EDIT MEASUREMENT
# =========================================================

elif menu == "✏️ Edit Measurement":

    st.header("✏️ Edit Existing Measurement")

    if df.empty:

        st.warning(
            "No measurements available."
        )

    else:

        selected_row = st.selectbox(
            "Select measurement",
            df.index,
            format_func=lambda x:
                f"Row {x + 1} | "
                f"{df.loc[x, 'operator']} | "
                f"{df.loc[x, 'timestamp']}"
        )

        current = df.loc[selected_row]

        with st.form("edit_form"):

            operator = st.selectbox(
                "Operator",
                [
                    "Dialog",
                    "Mobitel",
                    "Hutch",
                    "Airtel"
                ],
                index=[
                    "Dialog",
                    "Mobitel",
                    "Hutch",
                    "Airtel"
                ].index(current["operator"])
                if current["operator"]
                in [
                    "Dialog",
                    "Mobitel",
                    "Hutch",
                    "Airtel"
                ]
                else 0
            )

            location = st.text_input(
                "Location",
                value=str(current["location"])
            )

            signal = st.number_input(
                "Signal (dBm)",
                min_value=-150.0,
                max_value=0.0,
                value=float(current["signal_dbm"])
            )

            download = st.number_input(
                "Download (Mbps)",
                min_value=0.0,
                value=float(current["download_mbps"])
            )

            upload = st.number_input(
                "Upload (Mbps)",
                min_value=0.0,
                value=float(current["upload_mbps"])
            )

            latency = st.number_input(
                "Latency (ms)",
                min_value=0.0,
                value=float(current["latency_ms"])
            )

            packet_loss = st.number_input(
                "Packet Loss (%)",
                min_value=0.0,
                max_value=100.0,
                value=float(current["packet_loss_percent"])
            )

            network_type = st.selectbox(
                "Network Type",
                ["4G", "5G", "3G", "Other"],
                index=[
                    "4G",
                    "5G",
                    "3G",
                    "Other"
                ].index(current["network_type"])
                if current["network_type"]
                in ["4G", "5G", "3G", "Other"]
                else 0
            )

            device = st.text_input(
                "Device",
                value=str(current["device"])
            )

            update_button = st.form_submit_button(
                "💾 Update Measurement"
            )

        if update_button:

            df.loc[selected_row, "operator"] = operator
            df.loc[selected_row, "location"] = location
            df.loc[selected_row, "signal_dbm"] = signal
            df.loc[selected_row, "download_mbps"] = download
            df.loc[selected_row, "upload_mbps"] = upload
            df.loc[selected_row, "latency_ms"] = latency
            df.loc[selected_row, "packet_loss_percent"] = packet_loss
            df.loc[selected_row, "network_type"] = network_type
            df.loc[selected_row, "device"] = device

            save_data(df)

            st.success(
                "✅ Measurement updated successfully!"
            )

            st.rerun()


# =========================================================
# DELETE MEASUREMENT
# =========================================================

elif menu == "🗑️ Delete Measurement":

    st.header("🗑️ Delete Measurement")

    if df.empty:

        st.warning(
            "No measurements available."
        )

    else:

        selected_row = st.selectbox(
            "Select measurement to delete",
            df.index,
            format_func=lambda x:
                f"Row {x + 1} | "
                f"{df.loc[x, 'operator']} | "
                f"{df.loc[x, 'timestamp']}"
        )

        st.write("### Selected Record")

        st.dataframe(
            df.loc[[selected_row]],
            use_container_width=True
        )

        st.warning(
            "⚠️ This action permanently removes the "
            "selected record from the CSV file."
        )

        delete_button = st.button(
            "🗑️ Delete Selected Measurement",
            type="primary"
        )

        if delete_button:

            df = df.drop(
                index=selected_row
            ).reset_index(drop=True)

            save_data(df)

            st.success(
                "✅ Measurement deleted successfully!"
            )

            st.rerun()
# =========================================================
# Speed Test
# =========================================================

elif menu == "⚡ Speed Test":


    st.header("⚡ Internet Speed Test")

    st.info(
        "This test measures the speed of the Internet connection "
        "currently connected to this laptop."
    )

    operator = st.selectbox(
        "Select Operator",
        ["Dialog", "Mobitel", "Hutch", "Airtel", "Other"]
    )

    location = st.text_input(
        "Test Location",
        placeholder="Example: Maharagama"
    )

    network_type = st.selectbox(
        "Network Type",
        ["4G", "5G", "Wi-Fi", "Ethernet", "Other"]
    )
    signal_dbm = st.number_input(
    "📶 Signal Strength (dBm)",
            min_value=-150.0,
            max_value=0.0,
            value=-90.0,
            step=1.0,
            help="Enter the RSRP/Signal value shown by your phone or modem.",
            key="speed_test_signal"
        )

    


    if st.button("🚀 Start Speed Test", type="primary"):
        try:
            from src.collection.speed_test import run_speed_test

            with st.spinner("Testing internet connection..."):
                result = run_speed_test()

            required_keys = [
                "download_mbps",
                "upload_mbps",
                "latency_ms"
            ]

            if not all(key in result for key in required_keys):
                raise ValueError("Speed test result is incomplete.")

            st.session_state["speed_test_result"] = result
            st.session_state["speed_test_metadata"] = {
                "operator": operator,
                "location": location,
                "network_type": network_type,
                "signal_dbm": signal_dbm,
                "timestamp": pd.Timestamp.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            }
            st.session_state.pop("measurement_saved", None)

        except Exception as error:
            st.error(f"Speed test failed: {error}")

    if "speed_test_result" in st.session_state:
        result = st.session_state["speed_test_result"]
        metadata = st.session_state["speed_test_metadata"]

        st.success("✅ Speed test completed!")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "⬇️ Download Speed",
            f"{result['download_mbps']:.2f} Mbps"
        )
        col2.metric(
            "⬆️ Upload Speed",
            f"{result['upload_mbps']:.2f} Mbps"
        )
        col3.metric(
            "🏓 Latency",
            f"{result['latency_ms']:.2f} ms"
        )

        result_df = pd.DataFrame([{
            "Timestamp": metadata["timestamp"],
            "Operator": metadata["operator"],
            "Location": metadata["location"],
            "Network Type": metadata["network_type"],
            "Download (Mbps)": result["download_mbps"],
            "Upload (Mbps)": result["upload_mbps"],
            "Latency (ms)": result["latency_ms"]
        }])

        st.subheader("📋 Speed Test Result")
        st.dataframe(result_df, use_container_width=True)

        if st.button("💾 Save Measurement", type="primary",
                     key="save_speed_measurement"):

            new_record = {
                "timestamp": metadata["timestamp"],
                "operator": metadata["operator"],
                "location": metadata["location"],
                "signal_dbm": metadata["signal_dbm"],
                "download_mbps": result["download_mbps"],
                "upload_mbps": result["upload_mbps"],
                "latency_ms": result["latency_ms"],
                "packet_loss_percent": result.get(
                    "packet_loss_percent", None
                ),
                "network_type": metadata["network_type"],
                "device": "Laptop"
            }

            latest_df = load_data()
            latest_df = pd.concat(
                [latest_df, pd.DataFrame([new_record])],
                ignore_index=True
            )

            save_data(latest_df)
            st.session_state["measurement_saved"] = True
            st.success("✅ Measurement saved successfully!")

        if st.session_state.get("measurement_saved", False):
            st.info("This measurement has been saved to the app's CSV file.")

# =========================================================
# DASHBOARD
# =========================================================

elif menu == "📊 Dashboard":

    st.header("📊 CAMNS Network Dashboard")

    if df.empty:

        st.info(
            "📭 No network measurements available."
        )

        st.stop()

    numeric_columns = [
        "signal_dbm",
        "download_mbps",
        "upload_mbps",
        "latency_ms",
        "packet_loss_percent"
    ]

    for column in numeric_columns:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    try:

        scored_df = calculate_scores(df)

    except Exception as error:

        st.error(
            f"CAMNS scoring error: {error}"
        )

        st.stop()

    # -----------------------------------------------------
    # Operator average score
    # -----------------------------------------------------

    operator_scores = (
        scored_df
        .groupby("operator")["camns_score"]
        .mean()
        .sort_values(
            ascending=False
        )
    )

    best_operator = operator_scores.index[0]
    best_score = operator_scores.iloc[0]

    st.success(
        f"🏆 Recommended Network: "
        f"**{best_operator}**"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Best Network",
            best_operator
        )

    with col2:

        st.metric(
            "Average CAMNS Score",
            f"{best_score:.2f}"
        )

    st.divider()

    # -----------------------------------------------------
    # Score comparison
    # -----------------------------------------------------

    st.header("📈 Average Download Speed")
    download_line = (
            df.groupby("operator")["download_mbps"]
            .mean()
            .round(2)
    )
    st.line_chart(download_line)
    


    # -----------------------------------------------------
    # Score and Performance Comparison
    # -----------------------------------------------------

    st.header("📈 Network Comparison")

    graph_col1, graph_col2 = st.columns(2)

    # CAMNS Score Graph
    with graph_col1:

        st.subheader("🏆 CAMNS Score")

     
    st.bar_chart(
            operator_scores
        )


    download_comparison = (
            df
            .groupby("operator")["download_mbps"]
            .mean()
            .sort_values(
                ascending=False
            )
            .round(2)
        )

        # -----------------------------------------------------
        # Performance summary
        # -----------------------------------------------------



    summary = (
        df
            .groupby("operator")
            [
                [
                    "signal_dbm",
                    "download_mbps",
                    "upload_mbps",
                    "latency_ms",
                    "packet_loss_percent"
                ]
            ]
            .mean()
            .round(2)
        )

    st.dataframe(
            summary,
            use_container_width=True
        )

        # -----------------------------------------------------
        # Raw measurements
        # -----------------------------------------------------

    st.header("📋 All Measurements")

    st.dataframe(
            scored_df,
            use_container_width=True
        )

    st.caption(
            "⚠️ Sample data is for software testing only. "
            "Use real measurements for research analysis."
        )
    

    
