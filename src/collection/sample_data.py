import csv
import os
from datetime import datetime, timedelta
import random


# -----------------------------------------
# SAMPLE DATA GENERATOR
# -----------------------------------------

OUTPUT_FILE = "data/raw/network_data.csv"

operators = [
    "Dialog",
    "Mobitel",
    "Hutch",
    "Airtel"
]

locations = [
    "Test Location A",
    "Test Location B",
    "Test Location C"
]

network_types = [
    "4G",
    "4G",
    "4G",
    "5G"
]

devices = [
    "Sample Device 1",
    "Sample Device 2"
]


# -----------------------------------------
# Create output directory
# -----------------------------------------

os.makedirs("data/raw", exist_ok=True)


# -----------------------------------------
# Generate sample measurements
# -----------------------------------------

random.seed(42)

rows = []

start_time = datetime.now() - timedelta(hours=3)

for location in locations:

    for operator in operators:

        for test_number in range(5):

            timestamp = start_time + timedelta(
                minutes=len(rows) * 3
            )

            # Generate realistic-looking TEST values
            signal = random.randint(-110, -75)

            download = round(
                random.uniform(10, 60),
                2
            )

            upload = round(
                random.uniform(3, 20),
                2
            )

            latency = round(
                random.uniform(25, 100),
                2
            )

            packet_loss = round(
                random.uniform(0, 5),
                2
            )

            network_type = random.choice(
                network_types
            )

            device = random.choice(
                devices
            )

            rows.append([
                timestamp.strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
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


# -----------------------------------------
# Write CSV file
# -----------------------------------------

with open(
    OUTPUT_FILE,
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.writer(file)

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

    writer.writerows(rows)


print()
print("======================================")
print(" CAMNS SAMPLE DATA GENERATED")
print("======================================")
print()
print(f"Records created: {len(rows)}")
print(f"File: {OUTPUT_FILE}")
print()
print("IMPORTANT:")
print("This is TEST/SAMPLE data only.")
print("It must NOT be used as real research measurements.")
print()