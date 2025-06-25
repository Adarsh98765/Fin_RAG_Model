import re
import plotly.graph_objects as go

def parse_summary(summary_text: str) -> dict:
    """
    Extracts metrics from the plain text summary and returns a dict:
    { "Metric Name": "Value (str)", ... }
    """
    pattern = r"Metric:\s*(.*?)\s*Period:.*?Value:\s*(.*?)\s*Notes:"
    matches = re.findall(pattern, summary_text, re.DOTALL)

    metrics = {}
    for name, value in matches:
        cleaned_value = value.replace("₹", "").replace(",", "").strip()
        metrics[name.strip()] = cleaned_value
    return metrics

def generate_comparison_chart(summary1: str, summary2: str, label1: str = "Company A", label2: str = "Company B"):
    """
    Takes two plain-text summaries and generates a side-by-side bar chart for all common metrics.
    """
    data1 = parse_summary(summary1)
    data2 = parse_summary(summary2)

    common_metrics = set(data1.keys()) & set(data2.keys())
    common_metrics = sorted(list(common_metrics))  # consistent order

    values1 = [try_convert_to_float(data1[m]) for m in common_metrics]
    values2 = [try_convert_to_float(data2[m]) for m in common_metrics]

    fig = go.Figure()
    fig.add_trace(go.Bar(x=common_metrics, y=values1, name=label1))
    fig.add_trace(go.Bar(x=common_metrics, y=values2, name=label2))

    fig.update_layout(
        title="Financial Comparison",
        xaxis_title="Metric",
        yaxis_title="Value",
        barmode='group'
    )

    return fig

def try_convert_to_float(value: str):
    try:
        return float(re.findall(r"[-+]?\d*\.\d+|\d+", value)[0])
    except:
        return None  # Could not convert
