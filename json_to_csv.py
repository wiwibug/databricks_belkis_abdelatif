import json
import csv
import re

input_file = "./url/url.json"
output_file = "./url/csv_url.csv"

# Capture le texte entre \x1b[49m et le prochain \x1b
pattern = re.compile(r"\x1b\[49m(.*?)\x1b", re.DOTALL)

def extract_url_from_line(line: str) -> str:
    if not line:
        return ""
    m = pattern.search(line)
    return m.group(1).strip() if m else ""

with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f, delimiter=",")
    writer.writerow(["url", "status_code"])

    for item in data.get("processed", []):
        raw_line = item.get("line", "")
        url = extract_url_from_line(raw_line)
        writer.writerow([url, item.get("status_code", "")])

print(f"CSV généré: {output_file}")
