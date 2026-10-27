import pandas as pd


def normalize_higher_better(series):
    """
    Normalize values where a higher value is better.
    Example: download speed.
    """
    min_value = series.min()
    max_value = series.max()

    if max_value == min_value:
        return pd.Series([1.0] * len(series), index=series.index)

    return (series - min_value) / (max_value - min_value)


def normalize_lower_better(series):
    """
    Normalize values where a lower value is better.
    Example: latency and packet loss.
    """
    min_value = series.min()
    max_value = series.max()

    if max_value == min_value:
        return pd.Series([1.0] * len(series), index=series.index)

    return (max_value - series) / (max_value - min_value)


def normalize_signal(series):
    """
    Normalize signal strength.

    For dBm, a value closer to 0 is generally better.
    Example:
    -80 dBm is better than -110 dBm.
    """
    min_value = series.min()
    max_value = series.max()

    if max_value == min_value:
        return pd.Series([1.0] * len(series), index=series.index)

    return (series - min_value) / (max_value - min_value)


def calculate_scores(df):
    """
    Calculate CAMNS multi-metric network score.

    Current provisional weights:
        Signal      = 30%
        Download    = 35%
        Latency     = 20%
        Packet Loss = 15%

    These weights are provisional and will be evaluated/refined
    during the research.
    """

    required_columns = [
        "operator",
        "signal_dbm",
        "download_mbps",
        "latency_ms",
        "packet_loss_percent"
    ]

    for column in required_columns:
        if column not in df.columns:
            raise ValueError(f"Missing required column: {column}")

    result = df.copy()

    # Normalize each metric
    result["signal_score"] = normalize_signal(result["signal_dbm"])

    result["download_score"] = normalize_higher_better(
        result["download_mbps"]
    )

    result["latency_score"] = normalize_lower_better(
        result["latency_ms"]
    )

    result["packet_loss_score"] = normalize_lower_better(
        result["packet_loss_percent"]
    )

    # Provisional weights
    signal_weight = 0.30
    download_weight = 0.35
    latency_weight = 0.20
    packet_loss_weight = 0.15

    # Calculate overall CAMNS score
    result["camns_score"] = (
        result["signal_score"] * signal_weight
        + result["download_score"] * download_weight
        + result["latency_score"] * latency_weight
        + result["packet_loss_score"] * packet_loss_weight
    ) * 100

    return result


def select_best_network(df):
    """
    Select the network with the highest CAMNS score.
    """

    scored_data = calculate_scores(df)

    best_index = scored_data["camns_score"].idxmax()

    best_network = scored_data.loc[best_index]

    return best_network, scored_data


if __name__ == "__main__":
    print("CAMNS Scoring Algorithm module loaded successfully.")