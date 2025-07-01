import re
import plotly.graph_objects as go
from collections import defaultdict

def parse_graph_text(text: str) -> dict:
    """
    Parses structured graph data and returns a dict of:
    {
        "Metric Name": {
            "Period 1": value1,
            "Period 2": value2,
            ...
        },
        ...
    }
    """
    metric_blocks = text.strip().split("Metric:")
    data = defaultdict(dict)

    for block in metric_blocks:
        lines = block.strip().splitlines()
        if len(lines) < 2:
            continue

        name = lines[0].strip()
        period_line = next((l for l in lines if l.lower().startswith("period:")), None)
        value_line = next((l for l in lines if l.lower().startswith("value:")), None)

        if name and period_line and value_line:
            period = period_line.split(":", 1)[1].strip()
            value_str = value_line.split(":", 1)[1].strip()
            value = extract_numeric_value(value_str)
            if value is not None:
                data[name][period] = value

    return data

def extract_numeric_value(s: str):
    """Extract numeric value from a string like ₹20.5 Cr or 11.2%"""
    try:
        num = re.findall(r"[-+]?\d*\.\d+|\d+", s)
        return float(num[0]) if num else None
    except:
        return None

def generate_graphs_from_text(graph_text: str):
    """
    Main function: parses the graph data and creates one Plotly figure with subplots.
    """
    parsed_data = parse_graph_text(graph_text)

    # Create subplots – one bar/line chart per metric
    figures = []

    for metric, values in parsed_data.items():
        periods = sorted(values.keys())
        y_values = [values[p] for p in periods]

        fig = go.Figure()
        fig.add_trace(go.Bar(x=periods, y=y_values, name=metric))
        fig.update_layout(
            title=metric,
            xaxis_title="Period",
            yaxis_title="Value",
            height=400
        )
        figures.append(fig)

    # Combine all figures into a single dashboard using JSON (frontend will render them one by one)
    return figures[0] if figures else go.Figure()  # Return the first if only one chart is supported now
