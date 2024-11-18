import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
from netflix_genre_model import load_and_prepare_data, train_content_type_model, predict_content_type

# Inicializar la aplicación Dash
app = dash.Dash(__name__)
app.title = "Análisis de Netflix"
server = app.server

# Cargar y preparar los datos
df, le = load_and_prepare_data('/Users/inessaavedra/Desktop/miapp/app_2425/App/src/ViewingActivity.csv')

# Convertir 'Start Time' a datetime y 'Duration' a timedelta para facilitar el análisis
df['Start Time'] = pd.to_datetime(df['Start Time'])
df['Duration'] = pd.to_timedelta(df['Duration'])

# Agregar una columna para categorizar en 'Serie' o 'Película'
df['Category'] = df['Title'].apply(lambda x: 'Serie' if 'Season' in x or 'Episode' in x or 'Capítulo' in x or 'Temporada' in x else 'Película')

# Layout de la aplicación
 
app.layout = html.Div([
    # Encabezado con logo y título
    html.Div([
        html.Img(src='/assets/netflix_logo.png', style={'width': '150px', 'display': 'inline-block', 'vertical-align': 'middle'}),
        html.H1("Análisis de Preferencias en Netflix", 
                style={'color': '#E50914', 'display': 'inline-block', 'margin-left': '20px', 'vertical-align': 'middle'}),
    ], style={'textAlign': 'center', 'backgroundColor': '#141414', 'padding': '10px'}),

    # Selección de perfil
    html.Div([
        html.Label("Selecciona un perfil", style={'color': '#E5E5E5', 'fontSize': '20px'}),
        dcc.Dropdown(
            id='profile-dropdown',
            options=[{'label': profile, 'value': profile} for profile in df['Profile Name'].unique()],
            value=df['Profile Name'].unique()[0],
            style={'color': 'black', 'fontSize': '16px', 'width': '50%', 'margin': 'auto'}
        ),
    ], style={'textAlign': 'center', 'padding': '20px', 'backgroundColor': '#333'}),
    # Panel de estadísticas del perfil
    html.Div([
        html.H3("Número total de visualizaciones para el perfil seleccionado:", style={'color': '#E5E5E5'}),
        html.H2(id='views-count', style={'color': '#E50914', 'fontSize': '24px'})  # Asegúrate de que este ID esté presente
    ], style={'textAlign': 'center', 'margin': '20px'}),
    
    # Visualización del género preferido
    html.Div([
        html.H3("Género preferido previsto para este perfil:", style={'color': '#333'}),
        html.H2(id='predicted-genre', style={'color': '#E50914'})
    ], style={'textAlign': 'center', 'margin': '20px'}),


    # Gráfico de duración semanal y Top 10 Series y Películas
    html.Div([
        dcc.Graph(id='duration-time-graph', style={'backgroundColor': '#333', 'border': '1px solid #444', 'padding': '10px', 'margin-bottom': '20px'}),
        dcc.Graph(id='top-series-bar', style={'backgroundColor': '#333', 'border': '1px solid #444', 'padding': '10px', 'margin-bottom': '20px'}),
        dcc.Graph(id='top-movies-bar', style={'backgroundColor': '#333', 'border': '1px solid #444', 'padding': '10px'}),
    ], style={'margin': '20px'}),

    # Gráficos de frecuencia por día de la semana y distribución por hora del día
    html.Div([
        dcc.Graph(id='weekday-distribution', style={'width': '48%', 'display': 'inline-block', 'backgroundColor': '#333', 'border': '1px solid #444', 'padding': '10px'}),
        dcc.Graph(id='hour-distribution', style={'width': '48%', 'display': 'inline-block', 'backgroundColor': '#333', 'border': '1px solid #444', 'padding': '10px'}),
    ], style={'display': 'flex', 'justifyContent': 'space-around', 'margin': '20px'}),

], style={'backgroundColor': '#141414', 'fontFamily': 'Arial, sans-serif'})


# Callback para actualizar el contador de visualizaciones
@app.callback(
    Output('views-count', 'children'),
    Input('profile-dropdown', 'value')
)
def update_views_count(selected_profile):
    filtered_df = df[df['Profile Name'] == selected_profile]
    views_count = filtered_df.shape[0]
    return f"{views_count} visualizaciones"
@app.callback(
    Output('predicted-genre', 'children'),
    Input('profile-dropdown', 'value')
)
def update_predicted_genre(selected_profile):
    model = train_content_type_model(df, selected_profile)
    if model is None:
        return "No hay suficiente información para este perfil"
    # Hacer una predicción para el año actual
    predicted_genre = predict_content_type(model, X=pd.DataFrame([[pd.Timestamp.now().year]]), label_encoder=le)
    return f"{predicted_genre}"

# Callback para el gráfico de duración semanal
@app.callback(
    Output('duration-time-graph', 'figure'),
    Input('profile-dropdown', 'value')
)
def update_duration_graph(selected_profile):
    filtered_df = df[df['Profile Name'] == selected_profile]
    weekly_duration = filtered_df.resample('W', on='Start Time')['Duration'].sum().reset_index()
    weekly_duration['Duration_hours'] = weekly_duration['Duration'].dt.total_seconds() / 3600
    fig = px.line(weekly_duration, x='Start Time', y='Duration_hours', 
                  title='Duración de Visualización Agregada por Semana (Horas)',
                  labels={'Start Time': 'Semana', 'Duration_hours': 'Horas'},
                  color_discrete_sequence=['#E50914'])
    fig.update_yaxes(title_text="Horas")
    fig.update_layout(plot_bgcolor='#333', paper_bgcolor='#333', font_color='#E5E5E5')
    return fig

# Callback para el gráfico de top series
@app.callback(
    Output('top-series-bar', 'figure'),
    Input('profile-dropdown', 'value')
)
def update_top_series(selected_profile):
    filtered_df = df[(df['Profile Name'] == selected_profile) & (df['Category'] == 'Serie')]
    top_series = filtered_df['Title'].value_counts().head(10).reset_index()
    top_series.columns = ['Title', 'Count']
    fig = px.bar(top_series, x='Count', y='Title', orientation='h', title='Top 10 Series Más Vistas', color_discrete_sequence=['#E50914'])
    fig.update_layout(plot_bgcolor='#333', paper_bgcolor='#333', font_color='#E5E5E5')
    return fig

# Callback para el gráfico de top películas
@app.callback(
    Output('top-movies-bar', 'figure'),
    Input('profile-dropdown', 'value')
)
def update_top_movies(selected_profile):
    filtered_df = df[(df['Profile Name'] == selected_profile) & (df['Category'] == 'Película')]
    top_movies = filtered_df['Title'].value_counts().head(10).reset_index()
    top_movies.columns = ['Title', 'Count']
    fig = px.bar(top_movies, x='Count', y='Title', orientation='h', title='Top 10 Películas Más Vistas', color_discrete_sequence=['#E50914'])
    fig.update_layout(plot_bgcolor='#333', paper_bgcolor='#333', font_color='#E5E5E5')
    return fig

# Callback para el gráfico de frecuencia por día de la semana
@app.callback(
    Output('weekday-distribution', 'figure'),
    Input('profile-dropdown', 'value')
)
def update_weekday_distribution(selected_profile):
    # Crear una copia explícita del DataFrame filtrado para evitar advertencias
    filtered_df = df.loc[df['Profile Name'] == selected_profile].copy()
    
    # Modificación segura en una copia
    filtered_df['Weekday'] = filtered_df['Start Time'].dt.day_name()
    
    # Calcular la duración total de visualización por día de la semana
    weekday_duration = filtered_df.groupby('Weekday')['Duration'].sum().reindex(
        ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    ).fillna(pd.Timedelta(0))
    weekday_duration_hours = weekday_duration.apply(lambda x: x.total_seconds() / 3600)
    
    # Crear el gráfico
    fig = px.bar(weekday_duration_hours, x=weekday_duration_hours.index, y=weekday_duration_hours.values, 
                 title='Duración Total de Visualización por Día de la Semana (Horas)', labels={'y': 'Horas'},
                 color_discrete_sequence=['#E50914'])
    fig.update_layout(plot_bgcolor='#333', paper_bgcolor='#333', font_color='#E5E5E5')
    return fig
# Callback para el gráfico de distribución por hora del día
@app.callback(
    Output('hour-distribution', 'figure'),
    Input('profile-dropdown', 'value')
)
def update_hour_distribution(selected_profile):
    filtered_df = df[df['Profile Name'] == selected_profile]
    filtered_df['Hour'] = filtered_df['Start Time'].dt.hour
    fig = px.histogram(filtered_df, x='Hour', nbins=24, title='Distribución de Visualización por Hora del Día', color_discrete_sequence=['#E50914'])
    fig.update_layout(plot_bgcolor='#333', paper_bgcolor='#333', font_color='#E5E5E5')
    return fig

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)