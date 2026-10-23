import os
from collections import defaultdict

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Project paths
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_FILE = os.path.join(PROJECT_DIR, "results", "analysis-output.txt")
GRAPHS_DIR = os.path.join(PROJECT_DIR, "graphs")

os.makedirs(GRAPHS_DIR, exist_ok=True)

# Read the Hadoop MapReduce output
data = defaultdict(dict)

with open(RESULTS_FILE, "r", encoding="utf-8") as file:
    for line in file:
        line = line.strip()

        if not line:
            continue

        try:
            category, count_text = line.rsplit(maxsplit=1)
            category_type, name = category.split(":", 1)
            count = int(count_text)
            data[category_type][name] = count
        except ValueError:
            print(f"Skipping unrecognized line: {line}")

# 1. HTTP status-code distribution
status_codes = data["STATUS"]
status_labels = sorted(status_codes.keys())
status_counts = [status_codes[code] for code in status_labels]

plt.figure(figsize=(10, 6))
bars = plt.bar(status_labels, status_counts)

plt.title("HTTP Status-Code Distribution", fontsize=16)
plt.xlabel("HTTP Status Code")
plt.ylabel("Number of Requests")
plt.grid(axis="y", linestyle="--", alpha=0.4)

for bar, count in zip(bars, status_counts):
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height(),
        f"{count:,}",
        ha="center",
        va="bottom",
        fontsize=8,
    )

plt.tight_layout()
plt.savefig(
    os.path.join(GRAPHS_DIR, "http_status_distribution.png"),
    dpi=200,
)
plt.close()

# 2. HTTP request methods
methods = data["METHOD"]
method_labels = list(methods.keys())
method_counts = [methods[method] for method in method_labels]

plt.figure(figsize=(8, 6))
bars = plt.bar(method_labels, method_counts)

plt.title("HTTP Request Methods", fontsize=16)
plt.xlabel("Request Method")
plt.ylabel("Number of Requests")
plt.grid(axis="y", linestyle="--", alpha=0.4)

for bar, count in zip(bars, method_counts):
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height(),
        f"{count:,}",
        ha="center",
        va="bottom",
    )

plt.tight_layout()
plt.savefig(
    os.path.join(GRAPHS_DIR, "request_methods.png"),
    dpi=200,
)
plt.close()

# 3. Top 10 most-requested resources
resources = data["RESOURCE"]
top_resources = sorted(
    resources.items(),
    key=lambda item: item[1],
    reverse=True,
)[:10]

resource_labels = [item[0] for item in top_resources]
resource_counts = [item[1] for item in top_resources]

plt.figure(figsize=(12, 7))
bars = plt.barh(resource_labels[::-1], resource_counts[::-1])

plt.title("Top 10 Most-Requested Resources", fontsize=16)
plt.xlabel("Number of Requests")
plt.ylabel("Resource")
plt.grid(axis="x", linestyle="--", alpha=0.4)

for bar, count in zip(bars, resource_counts[::-1]):
    plt.text(
        bar.get_width(),
        bar.get_y() + bar.get_height() / 2,
        f" {count:,}",
        va="center",
        fontsize=9,
    )

plt.tight_layout()
plt.savefig(
    os.path.join(GRAPHS_DIR, "top_10_resources.png"),
    dpi=200,
)
plt.close()

print("All three graphs were generated successfully.")
print(f"Graph directory: {GRAPHS_DIR}")
print("1. http_status_distribution.png")
print("2. request_methods.png")
print("3. top_10_resources.png")