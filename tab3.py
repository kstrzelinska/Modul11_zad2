from dash import dcc, html
import plotly.graph_objects as go
import pandas as pd

def render_tab(df):
    # Dodanie kolumny z numerem dnia tygodnia i nazwą dnia tygodnia
    df['weekday_num'] = df['tran_date'].dt.weekday
    df['weekday'] = df['weekday_num'].map({
        0: 'Poniedziałek', 1: 'Wtorek', 2: 'Środa', 
        3: 'Czwartek', 4: 'Piątek', 5: 'Sobota', 6: 'Niedziela'
    })

    # Grupowanie danych dla heatmapy
    grouped = df[df['total_amt'] > 0].groupby(['Store_type', 'weekday_num'])['total_amt'].sum().unstack(fill_value=0)

    # Sortowanie kolumn według numeru dnia tygodnia
    grouped = grouped.sort_index(axis=1)

    # Tworzenie heatmapy
    fig = go.Figure()

    fig.add_trace(go.Heatmap(
        x=[{0: 'Poniedziałek', 1: 'Wtorek', 2: 'Środa', 
            3: 'Czwartek', 4: 'Piątek', 5: 'Sobota', 6: 'Niedziela'}[i] for i in grouped.columns],  # Oś X to dni tygodnia w poprawnej kolejności
        y=grouped.index,    # Oś Y to typy sklepów
        z=grouped.values,   # Z to wartości sprzedaży
        colorscale='Blues',  # Skala kolorów
        colorbar=dict(title="Sprzedaż")  # Dodanie legendy kolorów
    ))

    fig.update_layout(
        title="Sprzedaż według typu sklepu i dnia tygodnia",
        xaxis_title="Dzień tygodnia",
        yaxis_title="Typ sklepu",
        yaxis=dict(tickmode="linear"),
        margin=dict(t=40, b=40, l=40, r=40)  # Dostosowanie marginesów
    )

    # Budowa layoutu dla zakładki
    layout = html.Div([
        html.H1('Kanały sprzedaży', style={'text-align': 'center'}),

        # Komponent heatmapy
        html.Div([
            html.Div([dcc.Graph(id='hm-store-type', figure=fig)], style={'width': '50%'}),
            html.Div([
                dcc.Dropdown(
                    id='store_dropdown',
                    options=[{'label': Store_type, 'value': Store_type} for Store_type in df['Store_type'].unique()],
                    value=df['Store_type'].unique()[0],  # Domyślna wartość
                    style={'width': '100%'}
                ),
                dcc.Graph(id='barh-store-type')
            ], style={'width': '50%'})
        ], style={'display': 'flex'}),

        html.Div(id='temp-out')  # Komponent na dane tymczasowe lub inne informacje
    ])

    return layout
