from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt


def build_price_plot(points: list[tuple[str, float]], output_path: str) -> str:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    labels = [item[0] for item in points]
    values = [item[1] for item in points]

    plt.figure(figsize=(10, 4))
    plt.plot(labels, values, marker="o")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(path)
    plt.close()

    return str(path)
