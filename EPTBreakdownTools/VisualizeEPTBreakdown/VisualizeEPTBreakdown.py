import matplotlib.pyplot as plt
import json
import sys

def plot_events(filename: str):
    # Load JSON from a file
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)

    events = []

    # Flatten into (name, offset, duration)
    for k, v in data["at"].items():
        if isinstance(v, list):
            events.append((k, v[0], v[1]))
        elif isinstance(v, dict):
            for subk, subv in v.items():
                events.append((f"{k}:{subk}", subv[0], subv[1]))

    # Sort by offset (start time)
    events_sorted = sorted(events, key=lambda x: x[1])

    # Plot timeline with aligned offset + duration labels
    plt.figure(figsize=(14, 12))
    yticks = []
    labels = []

    # Left margin for aligned offsets
    min_start = min(e[1] for e in events_sorted)
    offset_xpos = min_start - 50

    for i, (name, start, duration) in enumerate(events_sorted):
        # Draw event bar
        plt.hlines(y=i, xmin=start, xmax=start+duration, colors="blue", linewidth=3)
        yticks.append(i)
        labels.append(name)

        # Start offset label (aligned column on left)
        plt.text(offset_xpos, i, f"{start} ms", va="center", ha="right",
                 fontsize=6, color="darkgreen")

        # Duration label (center of bar)
        if duration > 0:
            plt.text(start + duration/2, i, f"{duration} ms",
                     va="center", ha="center", fontsize=6, color="black")

    plt.yticks(yticks, labels, fontsize=6)
    plt.xlabel("Time (ms from start)")
    plt.title("Event Timeline from JSON (Aligned Offsets + Durations)")
    plt.grid(axis="x", linestyle="--", alpha=0.6)
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 VisualizeEPTBreakdown.py <filename.json>")
    else:
        plot_events(sys.argv[1])

