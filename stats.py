from collections import defaultdict

import requests

REPO = "mitradranirban/colr-pak"
URL = f"https://api.github.com/repos/{REPO}/releases"


def normalize_name(name, version):
    # 1. Remove the version string (e.g., 0.7.0) from the filename
    # This turns 'ColrPak-Setup-0.7.0.exe' into 'ColrPak-Setup-.exe'
    version_num = version.lstrip("v")
    clean = name.replace(version_num, "")

    # 2. Remove extra dashes or dots left behind
    clean = clean.replace("--", "-").replace("..", ".").replace("-. ", " ")
    return clean.strip("-")


def get_pivot_stats():
    response = requests.get(URL)
    if response.status_code != 200:
        print("Failed to fetch data.")
        return

    releases = response.json()

    matrix = defaultdict(lambda: defaultdict(int))
    all_clean_names = set()
    versions = []

    for release in releases:
        tag = release["tag_name"]
        versions.append(tag)
        for asset in release.get("assets", []):
            # Use our normalization function
            clean_name = normalize_name(asset["name"], tag)

            all_clean_names.add(clean_name)
            matrix[tag][clean_name] += asset["download_count"]

    # Sort columns: .exe first, then .msi, then others
    sorted_cols = sorted(list(all_clean_names))

    # Print Table
    col_width = 25
    header = f"{'Version':<10} | " + " | ".join(
        [f"{c:<{col_width}}" for c in sorted_cols]
    )
    print("\n" + header)
    print("-" * len(header))

    for v in versions:
        row = f"{v:<10} | "
        cell_values = []
        for col in sorted_cols:
            val = matrix[v].get(col, 0)
            cell_values.append(f"{str(val):<{col_width}}")
        print(row + " | ".join(cell_values))


if __name__ == "__main__":
    get_pivot_stats()
