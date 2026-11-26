import plotly.express as px
from dash import Dash, dcc, html, Input, Output

acciones = px.data.stocks()
EMPRESAS = ["GOOG", "AAPL", "AMZN", "FB", "NFLX", "MSFT"]

app = Dash(__name__)

app.layout = html.Div([
    html.H1("Acciones de tecnología"),
    dcc.Checklist(options=EMPRESAS, value=["GOOG", "AAPL"], inline=True, id="empresas"),
    dcc.RadioItems(options=["Todo", "2018", "2019"], value="Todo", inline=True, id="periodo"),
    dcc.RadioItems(
        options=["Mejor", "Peor", "Ambos"],
        value="Ambos",
        inline=True,
        id="metrica",
    ),
    html.H3(id="resumen"),
    dcc.Graph(id="grafica"),
])

@app.callback(
    Output("grafica", "figure"),
    Output("resumen", "children"),
    Input("empresas", "value"),
    Input("periodo", "value"),
    Input("metrica", "value"),
)
def actualizar(empresas, periodo, metrica):
    if not empresas:
        return px.line(), "Marca al menos una empresa."

    datos = acciones
    if periodo != "Todo":
        datos = acciones[acciones["date"].str.startswith(periodo)]

    fig = px.line(datos, x="date", y=empresas)

    cambio = datos[empresas].iloc[-1] / datos[empresas].iloc[0] - 1
    mejor = cambio.idxmax()
    peor = cambio.idxmin()

    if metrica == "Mejor":
        texto = f"Mejor del periodo: {mejor} ({cambio[mejor]:+.0%})"
    elif metrica == "Peor":
        texto = f"Peor del periodo: {peor} ({cambio[peor]:+.0%})"
    else:
        texto = f"Mejor del periodo: {mejor} ({cambio[mejor]:+.0%}) | Peor del periodo: {peor} ({cambio[peor]:+.0%})"

    return fig, texto

if __name__ == "__main__":
    app.run(debug=True)