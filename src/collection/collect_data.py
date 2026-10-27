import csv
import os
from datetime import datetime


FILE_PATH = "data/raw/network_data.csv"


def collect_data():
    print("\n=== CAMNS Network Data Collection ===\n")

    operator = input("Operator (Dialog/Mobitel/Hutch/Airtel): ")
    location = input("Location: ")
    signal = input("Signal (dBm): ")
    download = input("Download (Mbps): ")
    upload = input("Upload (Mbps): ")
    latency = input("Latency (ms): ")
    packet_loss = input("Packet Loss (%): ")
    network_type = input("Network Type (4G/5G): ")
    device = input("Device: ")

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    os.makedirs("data/raw", exist_ok=True)

    file_exists = os.path.exists(FILE_PATH)

    with open(FILE_PATH, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
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
            ])

        writer.writerow([
            timestamp,
            operator,
            location,
            signal,
            download,
            upload,
            latency,
            packet_loss,
            network_type,
            device
        ])

    print("\nData saved successfully!")
    print(f"Saved to: {FILE_PATH}")


if __name__ == "__main__":
    collect_data()