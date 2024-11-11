import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
# Inicializar la aplicación Dash
app = dash.Dash(__name__)
server = app.server
# Cargar los datos
df = pd.read_csv('/Users/inessaavedra/Library/CloudStorage/OneDrive-UniversidadPontificiaComillas/2MITBA/Visualizacion/Netflix/netflix-report/CONTENT_INTERACTION/ViewingActivity.csv')

# Convertir 'Start Time' a datetime y 'Duration' a timedelta para facilitar el análisis
df['Start Time'] = pd.to_datetime(df['Start Time'])
df['Duration'] = pd.to_timedelta(df['Duration'])

# Crear una columna 'Week' que indique la semana del año de cada visualización
df['Week'] = df['Start Time'].dt.isocalendar().week

# Agregar una columna para categorizar en 'Serie' o 'Película' (simplificado)
df['Category'] = df['Title'].apply(lambda x: 'Serie' if 'Season' in x or 'Episode' in x else 'Película')



# Layout de la aplicación
app.layout = html.Div([
    html.H1("Análisis de Actividad de Visualización en Netflix", style={'color': '#E50914'}),

    # Dropdown para seleccionar perfil
    html.Label("Selecciona un perfil", style={'color': '#333'}),
    dcc.Dropdown(
        id='profile-dropdown',
        options=[{'label': profile, 'value': profile} for profile in df['Profile Name'].unique()],
        value=df['Profile Name'].unique()[0],  # Selección por defecto del primer perfil
        style={'color': 'black'}
    ),

    # Contador de visualizaciones para el perfil seleccionado
    html.Div([
        html.H3("Número total de visualizaciones para el perfil seleccionado:", style={'color': '#333'}),
        html.H2(id='views-count', style={'color': '#E50914'})  # Estilo en rojo para resaltar el número
    ], style={'textAlign': 'center', 'margin': '20px'}),

    # Gráfico de duración de visualización agregada por semana
    dcc.Graph(id='duration-time-graph'),

    # Gráfico de los top 10 series
    dcc.Graph(id='top-series-bar'),

    # Gráfico de los top 10 películas
    dcc.Graph(id='top-movies-bar'),

    # Histograma de horarios de visualización
    dcc.Graph(id='time-histogram')
], style={'backgroundColor': '#F9F9F9'})  # Fondo claro

# Callback para actualizar el contador de visualizaciones para el perfil seleccionado
@app.callback(
    Output('views-count', 'children'),
    Input('profile-dropdown', 'value')
)
def update_views_count(selected_profile):
    # Filtrar los datos para el perfil seleccionado y contar las visualizaciones
    filtered_df = df[df['Profile Name'] == selected_profile]
    views_count = filtered_df.shape[0]
    
    # Devolver el número de visualizaciones
    return f"{views_count} visualizaciones"

# Callback para actualizar el gráfico de duración de visualización agregada por semana
@app.callback(
    Output('duration-time-graph', 'figure'),
    Input('profile-dropdown', 'value')
)
def update_duration_graph(selected_profile):
    # Filtrar los datos para el perfil seleccionado
    filtered_df = df[df['Profile Name'] == selected_profile]
    
    # Agrupar la duración total de visualización por semana y convertir a horas
    weekly_duration = filtered_df.resample('W', on='Start Time')['Duration'].sum().reset_index()
    weekly_duration['Duration_hours'] = weekly_duration['Duration'].dt.total_seconds() / 3600  # Convertir a horas
    
    # Crear el gráfico de líneas con colores personalizados
    fig = px.line(weekly_duration, x='Start Time', y='Duration_hours', title='Duración de Visualización Agregada por Semana (Horas)')
    fig.update_yaxes(title_text="Horas")
    fig.update_traces(line=dict(color='#E50914'))  # Línea en rojo
    fig.update_layout(plot_bgcolor='#F9F9F9', paper_bgcolor='#F9F9F9', font_color='#333')
    return fig

# Callback para actualizar el gráfico de los top 10 series
@app.callback(
    Output('top-series-bar', 'figure'),
    Input('profile-dropdown', 'value')
)
def update_top_series(selected_profile):
    filtered_df = df[(df['Profile Name'] == selected_profile) & (df['Category'] == 'Serie')]
    top_series = filtered_df['Title'].value_counts().head(10).reset_index()
    top_series.columns = ['Title', 'Count']
    fig = px.bar(top_series, x='Count', y='Title', orientation='h', title='Top 10 Series Más Vistas', color_discrete_sequence=['#E50914'])
    fig.update_layout(plot_bgcolor='#F9F9F9', paper_bgcolor='#F9F9F9', font_color='#333')
    return fig

# Callback para actualizar el gráfico de los top 10 películas
@app.callback(
    Output('top-movies-bar', 'figure'),
    Input('profile-dropdown', 'value')
)
def update_top_movies(selected_profile):
    filtered_df = df[(df['Profile Name'] == selected_profile) & (df['Category'] == 'Película')]
    top_movies = filtered_df['Title'].value_counts().head(10).reset_index()
    top_movies.columns = ['Title', 'Count']
    fig = px.bar(top_movies, x='Count', y='Title', orientation='h', title='Top 10 Películas Más Vistas', color_discrete_sequence=['#E50914'])
    fig.update_layout(plot_bgcolor='#F9F9F9', paper_bgcolor='#F9F9F9', font_color='#333')
    return fig

# Callback para actualizar el histograma de horarios de visualización
@app.callback(
    Output('time-histogram', 'figure'),
    Input('profile-dropdown', 'value')
)
def update_time_histogram(selected_profile):
    filtered_df = df[df['Profile Name'] == selected_profile]
    filtered_df['Hour'] = filtered_df['Start Time'].dt.hour  # Extraer la hora
    fig = px.histogram(filtered_df, x='Hour', nbins=24, title='Distribución Horaria de Visualización', color_discrete_sequence=['#E50914'])
    fig.update_layout(plot_bgcolor='#F9F9F9', paper_bgcolor='#F9F9F9', font_color='#333')
    return fig

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)
