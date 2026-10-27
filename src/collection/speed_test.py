import platform
import re
import subprocess
import speedtest


def measure_packet_loss(host="8.8.8.8", count=10):
    """Measure packet loss using the laptop's ping command."""

    if platform.system().lower() == "windows":
        command = ["ping", "-n", str(count), host]
    else:
        command = ["ping", "-c", str(count), host]

    try:
        completed = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=30
        )

        output = completed.stdout + completed.stderr

        # Windows output
        match = re.search(r"Lost\s*=\s*(\d+)", output, re.IGNORECASE)
        if match:
            lost = int(match.group(1))
            return round((lost / count) * 100, 2)

        # Linux/macOS output
        match = re.search(
            r"(\d+(?:\.\d+)?)%\s*packet loss",
            output,
            re.IGNORECASE
        )
        if match:
            return round(float(match.group(1)), 2)

    except Exception:
        pass

    return None


def run_speed_test():
    """Test the Internet connection currently used by this laptop."""

    st = speedtest.Speedtest()
    st.get_best_server()

    latency_ms = st.results.ping
    download_mbps = st.download() / 1_000_000
    upload_mbps = st.upload() / 1_000_000

    packet_loss = measure_packet_loss()

    if packet_loss is None:
        packet_loss = 0.0

    return {
        "download_mbps": round(download_mbps, 2),
        "upload_mbps": round(upload_mbps, 2),
        "latency_ms": round(latency_ms, 2),
        "packet_loss_percent": round(packet_loss, 2)
    }


if __name__ == "__main__":
    print("Running speed test...")

    result = run_speed_test()

    print(f"Download    : {result['download_mbps']} Mbps")
    print(f"Upload      : {result['upload_mbps']} Mbps")
    print(f"Latency     : {result['latency_ms']} ms")
    print(f"Packet Loss : {result['packet_loss_percent']} %")
