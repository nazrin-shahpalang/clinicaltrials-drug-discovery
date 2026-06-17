import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# Data Loading
BASE_DIR = Path(__file__).parent.parent
df = pd.read_csv(BASE_DIR / "data" / "raw" / "clinical_trials_data.csv")

DISEASE_AREAS = sorted(df["disease_area"].unique())
PHASES = sorted(df["phase"].dropna().unique())
YEARS = sorted([int(y) for y in df["start_year"].unique()])

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY],
                title="ClinicalTrials AI Drug Discovery")
server = app.server

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("ClinicalTrials.gov — AI Drug Discovery Trends",
                    className="mb-1", style={"color": "#1a5276"}),
            html.P("2,000 clinical trials (2013–2024) | Python · Plotly Dash · scikit-learn · R"),
            html.Hr()
        ])
    ], className="mt-3"),

    dbc.Row([
        dbc.Col([
            html.Label("Disease Area", className="fw-bold"),
            dcc.Dropdown(id="disease-filter",
                options=[{"label": "All", "value": "All"}] +
                        [{"label": d, "value": d} for d in DISEASE_AREAS],
                value="All", clearable=False)
        ], md=4),
        dbc.Col([
            html.Label("Phase", className="fw-bold"),
            dcc.Dropdown(id="phase-filter",
                options=[{"label": "All", "value": "All"}] +
                        [{"label": p, "value": p} for p in PHASES],
                value="All", clearable=False)
        ], md=4),
        dbc.Col([
            html.Label("Year Range", className="fw-bold"),
            dcc.RangeSlider(id="year-slider",
                min=2013, max=2024, step=1, value=[2013, 2024],
                marks={int(y): str(y) for y in YEARS[::2]},
                tooltip={"placement": "bottom"})
        ], md=4),
    ], className="mb-3 p-3 bg-light rounded"),

    dbc.Row(id="kpi-row", className="mb-4 g-3"),

    dbc.Row([
        dbc.Col(dcc.Graph(id="trend-chart"), md=8),
        dbc.Col(dcc.Graph(id="disease-pie"), md=4),
    ], className="mb-4"),

    dbc.Row([
        dbc.Col(dcc.Graph(id="ai-growth-chart"), md=6),
        dbc.Col(dcc.Graph(id="phase-bar"), md=6),
    ], className="mb-4"),

    dbc.Row([
        dbc.Col(dcc.Graph(id="sponsor-chart"), md=6),
        dbc.Col(dcc.Graph(id="enrollment-chart"), md=6),
    ], className="mb-4"),

    dbc.Row([
        dbc.Col([
            html.Hr(),
            html.P("Nazrin Shahpalangova · Rhine-Waal University of Applied Sciences · Germany",
                   className="text-muted text-center")
        ])
    ])
], fluid=True)


def filter_df(disease, phase, year_range):
    mask = (df["start_year"] >= year_range[0]) & (df["start_year"] <= year_range[1])
    if disease != "All":
        mask &= df["disease_area"] == disease
    if phase != "All":
        mask &= df["phase"] == phase
    return df[mask]


@callback(
    Output("kpi-row", "children"),
    Output("trend-chart", "figure"),
    Output("disease-pie", "figure"),
    Output("ai-growth-chart", "figure"),
    Output("phase-bar", "figure"),
    Output("sponsor-chart", "figure"),
    Output("enrollment-chart", "figure"),
    Input("disease-filter", "value"),
    Input("phase-filter", "value"),
    Input("year-slider", "value"),
)
def update_dashboard(disease, phase, year_range):
    dff = filter_df(disease, phase, year_range)

    kpi_cards = dbc.Row([
        dbc.Col(dbc.Card(dbc.CardBody([
            html.H3(f"{len(dff):,}", style={"color": "#1a5276"}),
            html.P("Total Trials", className="text-muted mb-0")])), md=3),
        dbc.Col(dbc.Card(dbc.CardBody([
            html.H3(str(dff["disease_area"].nunique()), style={"color": "#117a65"}),
            html.P("Disease Areas", className="text-muted mb-0")])), md=3),
        dbc.Col(dbc.Card(dbc.CardBody([
            html.H3(f"{dff['ai_designed'].mean():.1%}", style={"color": "#784212"}),
            html.P("AI-Designed", className="text-muted mb-0")])), md=3),
        dbc.Col(dbc.Card(dbc.CardBody([
            html.H3(f"{int(dff['enrollment'].median()):,}", style={"color": "#6c3483"}),
            html.P("Median Enrollment", className="text-muted mb-0")])), md=3),
    ], className="g-3").children

    trend = dff.groupby("start_year").size().reset_index(name="count")
    fig_trend = px.area(trend, x="start_year", y="count",
                        title="Trial Volume Over Time",
                        template="plotly_white")

    fig_pie = px.pie(dff["disease_area"].value_counts().reset_index(),
                     names="disease_area", values="count",
                     title="Trials by Disease Area",
                     template="plotly_white", hole=0.35)

    ai_yr = dff.groupby("start_year").agg(
        total=("nct_id", "count"), ai_count=("ai_designed", "sum")).reset_index()
    fig_ai = go.Figure()
    fig_ai.add_trace(go.Bar(x=ai_yr["start_year"], y=ai_yr["total"]-ai_yr["ai_count"],
                            name="Conventional", marker_color="#4a90d9"))
    fig_ai.add_trace(go.Bar(x=ai_yr["start_year"], y=ai_yr["ai_count"],
                            name="AI-Designed", marker_color="#e74c3c"))
    fig_ai.update_layout(barmode="stack", title="AI vs Conventional Trials",
                         template="plotly_white")

    phase_counts = dff["phase"].value_counts().reset_index()
    phase_counts.columns = ["phase", "count"]
    fig_phase = px.bar(phase_counts, x="phase", y="count",
                       title="Phase Distribution", template="plotly_white",
                       color="count", color_continuous_scale="Blues")
    fig_phase.update_layout(coloraxis_showscale=False)

    top_sponsors = dff["lead_sponsor"].value_counts().head(10).reset_index()
    top_sponsors.columns = ["sponsor", "count"]
    fig_sponsors = px.bar(top_sponsors, x="count", y="sponsor", orientation="h",
                          title="Top 10 Sponsors", template="plotly_white",
                          color="count", color_continuous_scale="Teal")
    fig_sponsors.update_layout(coloraxis_showscale=False)

    fig_enroll = px.box(dff[dff["enrollment"] < 10000], x="phase", y="enrollment",
                        title="Enrollment by Phase", template="plotly_white",
                        color="phase")
    fig_enroll.update_layout(showlegend=False)

    return kpi_cards, fig_trend, fig_pie, fig_ai, fig_phase, fig_sponsors, fig_enroll


if __name__ == "__main__":
    import os
port = int(os.environ.get("PORT", 8050))
app.run(host="0.0.0.0", port=port, debug=False)
