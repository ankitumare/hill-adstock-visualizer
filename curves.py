import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd

# Load your data
media_sales_control_merged = pd.read_excel("merged_data.xlsx")
d = media_sales_control_merged[['target_tv']].copy()

# Initialize Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H2("Hill Saturation Curve: Target Spend vs Adstocked Spend"),

    html.Label("Alpha"),
    dcc.Slider(
        id='alpha-slider',
        min=0.1,
        max=5,
        step=0.1,
        value=2,
        marks={i: str(i) for i in range(1, 6)}
    ),

    html.Label("Gamma"),
    dcc.Slider(
        id='gamma-slider',
        min=1e3,
        max=1e6,
        step=1000,
        value=100000,
        marks={int(i): f"{int(i):,}" for i in range(0, 200001, 50000)}
    ),

    dcc.Graph(id='adstock-plot')
])

@app.callback(
    Output('adstock-plot', 'figure'),
    Input('alpha-slider', 'value'),
    Input('gamma-slider', 'value')
)
def update_plot(alpha, gamma):
    df = d.copy()
    # Apply Hill transformation
    df['adstocked_spend'] = df['target_tv'].apply(lambda x: (x ** alpha) / ((x ** alpha) + (gamma ** alpha)))
    # Sort for smooth curve
    df = df.sort_values(by='target_tv')

    # Create plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['target_tv'],
        y=df['adstocked_spend'],
        mode='lines+markers',
        name='Hill Transformed Spend',
        line=dict(color='green')
    ))

    fig.update_layout(
        title=f"Hill Curve — Alpha: {alpha}, Gamma: {int(gamma):,}",
        xaxis=dict(title='Target Spend'),
        yaxis=dict(title='Adstocked Spend (Normalized Response)', range=[0, 1.05]),
        height=500,
        width=900
    )

    return fig

if __name__ == '__main__':
    app.run(debug=True)
