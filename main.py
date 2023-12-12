import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import folium
from dash.dependencies import Input, Output, State

# Carregar dados do CSV
df = pd.read_csv('AGRUPAMENTO_ESTADO.csv')
df1 = pd.read_csv('GC_ESTADOS_RESUMO.csv')
df2 = pd.read_csv('RESUMO_GERAL_GC_GD.csv')

p = df2['POTÊNCIA'].sum() / 1e6
p1 = df['SISTEMAS'].sum()
p2 = df1['SISTEMAS'].sum()
n = df2['N_MOD'].sum() / 1e6
n1 = df['N_MOD'].sum() / 1e6
n2 = df1['N_MOD'].sum() / 1e6
t = df2['PESO_TOTAL'].sum() / 1e6
t1 = df['PESO_TOTAL'].sum() / 1e6
t2 = df1['PESO_TOTAL'].sum() / 1e6

# Inicializar o aplicativo Dash
app = dash.Dash(__name__)

# Opções para os menus suspensos
variaveis_disponiveis = df.select_dtypes(include=['number']).columns.tolist()
estados_disponiveis = df['ESTADO'].unique()

# Função para obter estilo padrão para as caixas
def get_box_style():
    return {
        'width': '30%',
        'padding': '20px',
        'margin': '10px',
        'border': '1px solid #ddd',
        'display': 'inline-block',
        'background-color': '#f9f9f9',  # Cor de fundo
        'border-radius': '10px',  # Borda arredondada
        'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)'  # Sombra suave
    }

# Layout do aplicativo
app.layout = html.Div([
    # Barra superior com logotipo e título
    html.Div([
        # Adicionar uma imagem como fundo
        html.Img(src='assets/fundo1.jpg',
                 style={'width': '100%', 'height': '150%', 'position': 'absolute'}),

        # Conteúdo sobre a imagem (logotipo e título)
        html.Div([
            html.Div([
                html.Img(src='assets/logo2.jpg', style={'height': '50px', 'float': 'right'}),
            ], style={'float': 'left'}),

            html.Div([
                html.H1("Dashboard - Desafios e Oportunidades na Reciclagem de Módulos Fotovoltaicos no Brasil", style={'color': 'white', 'textAlign': 'center', 'font-size': '40px'}),
            ], style={'margin': 'auto', 'width': '50%', 'textAlign': 'center'}),

        ], style={'position': 'relative', 'zIndex': 2}),

    ], style={'position': 'relative'}),

    # Linha separadora
    html.Hr(style={'margin': '30px'}),

    # Resumo Geral
    html.Div([
        html.H2("Resumo Geral GC e GD", style={'text-align': 'center'}),
        # Quadrados de informações
        html.Div([
            html.Div([
                html.H3("Potência Total instalada (GW)"),
                html.P(f"{df2['POTÊNCIA'].sum() / 1e6:.2f} GW"),
                html.H3("Número de Sistemas GD"),
                html.P(f"{df['SISTEMAS'].sum()}"),
                html.H3("Número de Sistemas GC"),
                html.P(f"{df1['SISTEMAS'].sum()}"),
            ], style=get_box_style()),

            html.Div([
                html.H3("Quantidade de Módulos Fotofoltaicos (Mi)"),
                html.P(f"{df2['N_MOD'].sum() / 1e6:.2f} Mi"),
                html.H3("Quantidade de Módulos Fotofoltaicos GD (Mi)"),
                html.P(f"{df['N_MOD'].sum() / 1e6:.2f} Mi - {(n1 / n) * 100:.2f} % "),
                html.H3("Quantidade de Módulos Fotofoltaicos GC (Mi)"),
                html.P(f"{df1['N_MOD'].sum() / 1e6:.2f} Mi - {(n2 / n) * 100:.2f} % "),
            ], style=get_box_style()),

            html.Div([
                html.H3("Peso Total de Módulos Fotofoltaicos (Mt)"),
                html.P(f"{df2['PESO_TOTAL'].sum() / 1e9:.2f} Mt"),
                html.H3("Peso Total de Módulos Fotofoltaicos (Mt)"),
                html.P(f"{df['PESO_TOTAL'].sum() / 1e9:.2f} Mt - GD - {(t1 / t) * 100:.2f} % "),
                html.H3("Peso Total de Módulos Fotofoltaicos (Mt)"),
                html.P(f"{df1['PESO_TOTAL'].sum() / 1e9:.2f} Mt - GC - {(t2 / t) * 100:.2f} %"),
            ], style=get_box_style()),

            # Div para a imagem 1
            html.Div([
                html.Img(src='assets/comp.JPG', style={'width': '60%'}),
                html.Div([
                    html.H5("Observação:"),
                    html.P("O gráfico apresentado representa a composição percentual do módulo fotovoltaico considerado nesta pesquisa. Essa composição é importante tanto para o cálculo das quantidades de materiais utilizados quanto para a análise de ciclo de vida (LCA).", style={'text-align': 'justify'}),
                ], style={'width': '30%', 'display': 'inline-block', 'margin-left': '10px', 'vertical-align': 'top', 'margin-top': '10px'}),
            ], style=get_box_style()),

            # Div para a imagem2
            html.Div([
                html.Img(src='assets/quant.JPG', style={'width': '60%'}),
                html.Div([
                    html.H5("Observação:"),
                    html.P("A faixa de potência mais abundante é de 301 a 400 W. Porém, foi considerado como módulo típico a faixa de 601 a 700 W. Isso porque os módulos dessa faixa possuem uma frequência mais elevada, embora em menor quantidade. Essa escolha mais conservadora visa mitigar as incertezas nos pesos dos módulos.", style={'text-align': 'justify'}),
                ], style={'width': '30%', 'display': 'inline-block', 'margin-left': '10px', 'vertical-align': 'top','margin-top': '10px'}),

            ], style=get_box_style()),

            # Div para a imagem 3
            html.Div([
                html.Img(src='assets/peso.JPG', style={'width': '60%'}),
                html.Div([
                    html.H5("Observação:"),
                    html.P("O gráfico apresenta o peso médio dos módulos fotovoltaicos, considerando as faixas de potência. Os dados foram extraídos de datasheets, mas apenas para módulos monofaciais, de silício multicristalino, com moldura de alumínio e vidro na parte frontal.", style={'text-align': 'justify'}),
                ], style={'width': '30%', 'display': 'inline-block', 'margin-left': '10px', 'vertical-align': 'top', 'margin-top': '10px'}),
            ], style=get_box_style()),
        ]),

        # Linha separadora
        html.Hr(style={'margin': '30px'}),

        # Título "Dados por Estado"
        html.H2("Dados por Estado", style={'text-align': 'center'}),

        # Dropdown para escolher a variável do gráfico de barras
        dcc.Dropdown(
            id='variavel-barras',
            options=[{'label': variavel, 'value': variavel} for variavel in variaveis_disponiveis],
            value='N_MOD',  # Valor padrão
            multi=False,
            style={'width': '100%'}
        ),

        # Dropdown para escolher entre GD, GC e Geral
        dcc.Dropdown(
            id='escolha-dados',
            options=[
                {'label': 'Geração Distribuída', 'value': 'GD'},
                {'label': 'Geração Centralizada', 'value': 'GC'},
                {'label': 'Geral (GD + GC)', 'value': 'GERAL'}
            ],
            value='Geral (GD + GC)',  # Valor padrão
            multi=False,
            style={'width': '100%'}
        ),

        # Dividindo o layout em duas partes iguais (50% cada)
        html.Div([
            # Div para o gráfico de barras
            html.Div([
                # Gráfico de barras
                dcc.Graph(
                    id='grafico-barras',
                ),
            ], style={'width': '50%', 'display': 'inline-block'}),

            # Div para o mapa
            html.Div([
                # Adicionando um espaço para o mapa
                html.Div(id='mapa', style={'width': '100%', 'height': '500px'}),
            ], style={'width': '50%', 'display': 'inline-block'}),
        ]),
        # Linha separadora
        html.Hr(style={'margin': '30px'})

    ]),
])

# Callback para atualizar o gráfico de barras
@app.callback(
    Output('grafico-barras', 'figure'),
    [Input('variavel-barras', 'value'),
     Input('escolha-dados', 'value')]
)
def atualizar_grafico_barras(variavel_selecionada, escolha_dados):
    if escolha_dados == 'GD':
        df_atual = df
    elif escolha_dados == 'GC':
        df_atual = df1
    else:  # 'GERAL'
        df_atual = df2

    figura = px.bar(df_atual, x='ESTADO', y=variavel_selecionada, title=f'{variavel_selecionada} por Estado',  color='ESTADO')
    return figura


# Callback para adicionar o mapa ao layout
@app.callback(
    Output('mapa', 'children'),
    [Input('variavel-barras', 'value'),
     Input('escolha-dados', 'value')]
)
def atualizar_mapa(variavel_selecionada, escolha_dados):
    if escolha_dados == 'GD':
        df_atual = df
    elif escolha_dados == 'GC':
        df_atual = df1
    else:  # 'GERAL'
        df_atual = df2

    # Criar um mapa centrado no Brasil
    m = folium.Map(location=[-15.77972, -47.92972], zoom_start=4)

    # Adicionar marcadores para cada estado com informações
    for _, row in df_atual.iterrows():
        municipio = row['ESTADO']
        latitude = row['LATITUDE']
        longitude = row['LONGITUDE']

        # Formatar as informações a serem exibidas no marcador
        popup_text = f"""<b>Sistemas GD:</b> {row['SISTEMAS']}<br>
                        <b>Potência:</b> {row['POTÊNCIA']}<br>
                        <b>Número de Módulos:</b> {row['N_MOD']}<br>
                        <b>Peso Total:</b> {row['PESO_TOTAL']}<br>
                        <b>Vidro:</b> {row['VIDRO']}<br>
                        <b>Alumínio:</b> {row['ALUMÍNIO']}<br>
                        <b>EVA:</b> {row['EVA']}<br>
                        <b>Silício:</b> {row['SILÍCIO']}<br>
                        <b>Polímero:</b> {row['POLÍMERO']}<br>
                        <b>Cabos:</b> {row['CABOS (Cu e Polimeros)']}<br>
                        <b>Condutores Internos (AL):</b> {row['CONDUTOR AL (Interno)']}<br>
                        <b>Condutores Internos (CU):</b> {row['CONDUTOR CU (Interno)']}<br>
                        <b>Chunbo e Estanho:</b> {row['CHUMBO E ESTANHO']}<br>
                        <b>Prata:</b> {row['PRATA']}<br>"""

        # Adicione um marcador ao mapa
        folium.Marker(
            location=[latitude, longitude],
            popup=folium.Popup(popup_text, max_width=300),
        ).add_to(m)

    # Converter o mapa Folium para HTML
    mapa_html = m.get_root().render()

    return [html.Iframe(srcDoc=mapa_html, width='100%', height='500px')]


# Executa o aplicativo
if __name__ == '__main__':
    app.run_server(debug=False)
