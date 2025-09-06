import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go

# Charger les données Anatole
file_path = "DATA/Anatole_processed_concatenated_plusEtat.parquet"
df_Anatole = pd.read_parquet(file_path)
df_Anatole['TIME'] = pd.to_datetime(df_Anatole['TIME'])  # Convertir TIME en datetime
# Liste des colonnes numériques
numeric_columns_Anatole = df_Anatole.select_dtypes(include=['float64', 'int64']).columns.tolist()
# Colonnes à afficher dans le tableau
table_columns_Anatole = ['TIME', 'str_etat']

# Charger les données Kevin
file_path2 = "DATA/processed_data_Kevin.csv"
df_Kevin = pd.read_csv(file_path2)
df_Kevin['TIME'] = pd.to_datetime(df_Kevin['TIME'])  # Convertir TIME en datetime
# Liste des colonnes numériques
numeric_columns_Kevin = df_Kevin.select_dtypes(include=['float64', 'int64']).columns.tolist()
# Colonnes à afficher dans le tableau
table_columns_Kevin = ['TIME', 'mvt_poids']


# Initialiser l'application Dash
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Visualisation des Etats de Forage"),
    
    html.Div([# Partie Anatole
        # Première colonne
        html.Div([
            html.H2("Etude faites par Anatole"),
            html.H3("Plot"),
            dcc.RangeSlider(
                id='time-range',
                min=0,
                max=len(df_Anatole)-1,
                step=1,
                marks={i: str(df_Anatole['TIME'].iloc[i]) for i in range(0, len(df_Anatole), max(1, len(df_Anatole)//5))},
                value=[0, len(df_Anatole)-1]
            ),
            html.Br(),
            dcc.Dropdown(
                id='columns-select',
                options=[{'label': col, 'value': col} for col in numeric_columns_Anatole],
                multi=True,
                placeholder="Sélectionner des colonnes à afficher"
            ),
            dcc.Graph(id='time-series-plot', style={'height': '1200px'})
        ], style={'width': '50%', 'padding': '20px'}),

        # Deuxième colonne
        html.Div([
            html.Br(),
            html.P("Pour rendre mon travail rapidement adaptable, j'ai réalisé une pipeline de traitement avec des fonctions python enchaînées pour les différentes étapes du prétraitement et du traitement dont les paramètres peuvent être facilement adaptés en fonction des retours de l'expert métier. La chaîne de traitement est la suivante:"), 
            html.P("Remplacement des valeurs négatives par 0"),
            html.P("Lissage par moyennage local"),
            html.P("Calcul de la dérivée de BPOS"),
            html.P("Classification de la variation de BPOS au cours du temps (croissant, décroissant, constant)"),
            html.P("Classification de l'état en charge ou non"),
            html.P("Classification de l'état en train de forer ou non"),
            html.P("Classification de l'état en train de pomper ou non"),
            html.P("Sont aussi présentes des opérations de:"),
            html.P("Concaténation des différents fichiers journaliers "),
            html.P("Plot de BPOS avec ses différents états"),
            html.P("Génération des description textuelles des différents états simultanés pour chaque point"),
            html.Br(),

            html.H3("États des événements"),
            dash_table.DataTable(
                id='event-table',
                columns=[{'name': col, 'id': col} for col in table_columns_Anatole],
                style_table={'overflowX': 'auto', 'height': '600px', 'overflowY': 'scroll'},
                style_cell={'textAlign': 'center'},
                page_size=100  # Limite le nombre de lignes affichées
            )
        ], style={'width': '50%', 'padding': '20px'})

    ], style={'display': 'flex'}),  # Affichage en deux colonnes côte à côte
    html.Br(),
    
    html.Div([# Partie Kevin
                # Première colonne
                html.Div([
                    html.H2("Etude faites par Kevin"),
                    html.H3("Plot"),
                    dcc.RangeSlider(
                        id='time-range2',
                        min=0,
                        max=len(df_Kevin)-1,
                        step=1,
                        marks={i: str(df_Kevin['TIME'].iloc[i]) for i in range(0, len(df_Kevin), max(1, len(df_Kevin)//5))},
                        value=[0, len(df_Kevin)-1]
                    ),
                    html.Br(),
                    dcc.Dropdown(
                        id='columns-select2',
                        options=[{'label': col, 'value': col} for col in numeric_columns_Kevin],
                        multi=True,
                        placeholder="Sélectionner des colonnes à afficher"
                    ),
                    dcc.Graph(id='time-series-plot2', style={'height': '1200px'})
                ], style={'width': '50%', 'padding': '20px'}),

                # Deuxième colonne
                html.Div([

                    html.P("J'ai effectué un lissage de mes données sur une période de 15 secondes afin d'en atténuer les variations et d'obtenir des informations plus stables. Ensuite, j'ai appliqué des conditions spécifiques pour discriminer les données en fonction de leur tendance, en créant des seuils correspondant à différents états. Par exemple, j'ai attribué des valeurs de 0, 1 et -1 à la variable 'BPOS' pour représenter les états stables, croissants et décroissants respectivement. À partir de ces informations, j'ai créé une nouvelle colonne qui permet de catégoriser les différentes phases de mouvement en fonction de la tendance et de l'état de charge. Cette colonne permet ainsi de définir si le système est en montée à vide, en montée en charge, en descente à vide, en descente en charge, stable, ou si l'état est inconnu, offrant une vue d'ensemble claire sur l'évolution des données."), 
                    html.H3("États des événements"),
                    dash_table.DataTable(
                        id='event-table2',
                        columns=[{'name': col, 'id': col} for col in table_columns_Kevin],
                        style_table={'overflowX': 'auto', 'height': '600px', 'overflowY': 'scroll'},
                        style_cell={'textAlign': 'center'},
                        page_size=10  # Limite le nombre de lignes affichées
                    )
                ], style={'width': '50%', 'padding': '20px'})

            ], style={'display': 'flex'})

])

# Partie Anatole
@app.callback(
    Output('time-series-plot', 'figure'),
    [Input('time-range', 'value'),
     Input('columns-select', 'value')]
)
def update_plot(time_range, selected_columns):
    if not selected_columns:
        return go.Figure(layout_title_text="Sélectionnez au moins une colonne")
    
    filtered_df_Anatole = df_Anatole.iloc[time_range[0]:time_range[1]+1]
    
    fig = go.Figure()
    # Ajouter chaque courbe avec TIME en Y et les valeurs sélectionnées en X
    for col in selected_columns:
        fig.add_trace(go.Scatter(
            x=filtered_df_Anatole[col],  # Les valeurs sont sur l'axe X
            y=filtered_df_Anatole['TIME'],  # Le temps est sur l'axe Y
            mode='lines', 
            name=col,
        ))

    
    return fig

@app.callback(
    Output('event-table', 'data'),
    [Input('time-range', 'value')]
)
def update_table(time_range):
    filtered_df_Anatole = df_Anatole.iloc[time_range[0]:time_range[1]+1]
    return filtered_df_Anatole.to_dict('records')


# Partie Kevin
@app.callback(
    Output('time-series-plot2', 'figure'),
    [Input('time-range2', 'value'),
     Input('columns-select2', 'value')]
)
def update_plot(time_range, selected_columns):
    if not selected_columns:
        return go.Figure(layout_title_text="Sélectionnez au moins une colonne")
    
    filtered_df_Kevin = df_Kevin.iloc[time_range[0]:time_range[1]+1]
    
    fig = go.Figure()
    # Ajouter chaque courbe avec TIME en Y et les valeurs sélectionnées en X
    for col in selected_columns:
        fig.add_trace(go.Scatter(
            x=filtered_df_Kevin[col],  # Les valeurs sont sur l'axe X
            y=filtered_df_Kevin['TIME'],  # Le temps est sur l'axe Y
            mode='lines', 
            name=col,
        ))

    
    return fig

@app.callback(
    Output('event-table2', 'data'),
    [Input('time-range2', 'value')]
)
def update_table(time_range):
    filtered_df_Kevin = df_Kevin.iloc[time_range[0]:time_range[1]+1]
    return filtered_df_Kevin.to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True)