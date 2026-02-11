import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path


def read_bound_computers(bound_computers_csv: Path) -> set[str]:
    """
    Reads the processed MAC addresses from a CSV file.

    The function attempts to read the CSV file and extract the "MACAddress" column,
    returning a set of MAC addresses. If the file cannot be read, it returns an empty set.

    Args:
        bound_computers_csv (Path): Path to the CSV file containing MAC addresses already bound to computers.

    Returns:
        set[str]: A set of processed MAC addresses.
    """
    try:
        macs = pd.read_csv(bound_computers_csv)
        return set(macs["MACAddress"].tolist())
    except Exception:
        return set()


def extract_new_macs(
    log_file: Path, bound_computers_csv: Path, fresh_minutes: float
) -> list[str]:
    """
    Extracts new MAC addresses from a DHCP log file that are not in the bound computers CSV
    and are within the freshness limit.

    This function reads the log file line by line, looking for lines containing "DHCPDISCOVER".
    It extracts the timestamp and MAC address from each relevant line, checks if the MAC address
    is already bound to a computer and is within the freshness limit, and if so, adds it to
    the list of new MACs.

    Args:
        log_file (Path): Path to the DHCP log file containing network discovery entries.
        bound_computers_csv (Path): Path to the CSV file containing MAC addresses already bound to computers.
        fresh_minutes (float): Time limit in minutes to consider a MAC address as fresh (recently discovered).

    Returns:
        list[str]: A list of new MAC addresses found within the freshness limit that are not yet bound to computers.
    """
    new_macs = set()
    bound_computers = read_bound_computers(bound_computers_csv)

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

            if mac not in bound_computers:
                new_macs.add(mac)

    return list(new_macs)
