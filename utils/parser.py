import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path


def read_processed_macs(processed_macs_file: Path) -> set[str]:
    """
    Reads the processed MAC addresses from a CSV file.

    The function attempts to read the CSV file and extract the "MACAddress" column,
    returning a set of MAC addresses. If the file cannot be read, it returns an empty set.

    Args:
        processed_macs_file (Path): Path to the CSV file containing processed MAC addresses.

    Returns:
        set[str]: A set of processed MAC addresses.
    """

    try:
        macs = pd.read_csv(processed_macs_file)
        return set(macs["MACAddress"].tolist())
    except Exception:
        return set()


def extract_new_macs(
    log_file: Path, processed_macs_file: Path, fresh_minutes: float
) -> list[str]:
    """
    Extracts new MAC addresses from a log file that are not in the processed MACs file
    and are within the freshness limit.

    This function reads the log file line by line, looking for lines containing "DHCPDISCOVER".
    It extracts the timestamp and MAC address from each relevant line, checks if the MAC address
    is in the processed MACs file and is within the freshness limit, and if so, adds it to the list of new MACs.

    Args:
        log_file (Path): _description_
        processed_macs_file (Path): _description_
        fresh_minutes (float): _description_

    Returns:
            list[str]: _description_
    """

    new_macs = set()
    processed_macs = read_processed_macs(processed_macs_file)

    with open(log_file, "r", encoding="utf-8") as file:
        for line in file:
            if "DHCPDISCOVER" not in line:
                continue
            parts = line.split()
            if len(parts) < 8:
                continue

            timestamp_str = f"{parts[0]} {parts[1]} {parts[2]}"
            mac = parts[7].upper()

            try:
                log_time = datetime.strptime(timestamp_str, "%b %d %H:%M:%S")
                log_time = log_time.replace(year=datetime.now().year)
            except Exception:
                continue

            if (datetime.now() - log_time) > timedelta(minutes=fresh_minutes):
                continue

            if mac not in processed_macs:
                new_macs.add(mac)

    return list(new_macs)
