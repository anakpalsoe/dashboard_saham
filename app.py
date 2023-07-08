import yfinance as yf
from dash import Dash, html, dcc, Input, Output, callback, dash_table
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
import matplotlib.pyplot as plt
import seaborn as sns


# Mengambil data transaksi saham dari Yahoo Finance
data = yf.download("TLKM.JK", start="2020-01-01", end="2023-06-22")

# Membuat data frame dari data transaksi saham
df = pd.DataFrame(data).reset_index()

df["Date"] = pd.to_datetime(df["Date"]).dt.strftime("%Y-%m-%d")
dt_melt = df[["Date", "Open", "High", "Low", "Close"]]
dt_melt = dt_melt.melt(id_vars=["Date"], var_name="market", value_name="nilai_market")

external_stylesheet = [dbc.themes.BOOTSTRAP]  # menghubungkan dengan bootstarp

app = Dash(__name__, external_stylesheets=external_stylesheet)


app.layout = dbc.Container(
    [
        dbc.Row(
            [
                html.Div(
                    "Dashboard Saham",
                    className="text-primary text-center fs-3",
                ),
                html.Hr(),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dash_table.DataTable(
                            data=df.to_dict("records"),
                            page_size=10,
                            style_table={"overflowX": "auto"},
                        )
                    ],
                    width=6,
                ),
                dbc.Col(
                    [
                        dcc.Graph(
                            figure=px.histogram(
                                df, x=df["Close"], nbins=5, title="Histogram Closed"
                            )
                        )
                    ],
                    width=6,
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.RadioItems(
                    options=dt_melt['market'].unique(),
                    value='Close',
                    id="radio-input",
                    inline=True,
                ),
                html.Hr()
            ]
        ),
        dbc.Row(
            [
                dcc.Graph(
                    figure={},
                    id="line-graph-final",
                )
            ]
        ),
        dbc.Row([
            html.Div('Deskripsi',
            className="text-primary text-center fs-3"),
            html.Hr()
        ]),
        dbc.Row([
            dbc.Col([dcc.Markdown('''
                                * ** Mean Close **:{}
                                * ** Median Close ** :{}
                                * ** Standar Deviasi Close **:{}
                                * ** Jumlah Data ** : {}
                                  '''
                                  .format(df['Close'].mean().round(2),df['Close'].median(),df['Close'].std().round(2),df['Close'].count()))],width=3),
            dbc.Col([dcc.Markdown('''
                                * ** Mean Open **:{}
                                * ** Median Open ** :{}
                                * ** Standar Deviasi Open **:{}
                                * ** Jumlah Data ** : {}
                                  '''
                                  .format(df['Open'].mean().round(2),df['Open'].median(),df['Open'].std().round(2),df['Open'].count()))],width=3),
            dbc.Col([dcc.Markdown('''
                                * ** Mean High **:{}
                                * ** Median High ** :{}
                                * ** Standar Deviasi High **:{}
                                * ** Jumlah Data ** : {}
                                  '''
                                  .format(df['High'].mean().round(2),df['High'].median(),df['High'].std().round(2),df['High'].count()))],width=3),
            dbc.Col([dcc.Markdown('''
                                * ** Mean Low **:{}
                                * ** Median Low ** :{}
                                * ** Standar Deviasi Low **:{}
                                * ** Jumlah Data ** : {}
                                  '''
                                  .format(df['Low'].mean().round(2),df['Low'].median(),df['Low'].std().round(2),df['Low'].count()))],width=3)
        ])
    ],
    fluid=True,
)


@callback(
    Output(component_id="line-graph-final", component_property="figure"),
    Input(component_id="radio-input",component_property='value'),
)

def update_data(select_market):
    filter_dt=dt_melt[dt_melt.market==select_market]

    fig=px.line(filter_dt, x='Date', y='nilai_market', hover_name='Date')



#def update_grap(market_name):
    #fig = px.line(dt_melt, x="Date", y=market_name, color='market')

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
