import pandas as pd
from datetime import datetime, timedelta
from os import getenv
from pathlib import Path


LOG_FILE = Path(getenv("LOG_FILE_PATH", "logs/dhcpd.log"))
PROCESSED_MACS_FILE = Path(getenv("PROCESSED_MACS_FILE", "data/MACs.csv"))
FRESH_LIMIT_MINUTES = float(getenv("LOG_FILE_PATH", 60))


def read_processed_macs(processed_macs_file: Path) -> set[str]:
    try:
        macs = pd.read_csv(processed_macs_file)
        return set(macs["MACAddress"].tolist())
    except Exception:
        return set()


def extract_new_macs(
    log_file: Path, processed_macs_file: Path, fresh_minutes: float
) -> list[str]:
    new_macs = []
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
                new_macs.append(mac)
    return new_macs
