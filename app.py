import dash
import dash_core_components as dcc
import dash_html_components as html
from textwrap import dedent
from numpy import mean

from regressor import predict

# public_transport_station_km, trc_sqm_2000,leisure_count_500,full_sq , sub_area,university_top_20_raion


sub_regions = ['Bibirevo', 'Nagatinskij Zaton', "Tekstil'shhiki", 'Mitino',
               'Basmannoe', 'Nizhegorodskoe', "Sokol'niki", 'Koptevo', 'Kuncevo',
               'Kosino-Uhtomskoe', 'Zapadnoe Degunino', 'Presnenskoe',
               'Lefortovo', "Mar'ino", "Kuz'minki", 'Nagornoe', "Gol'janovo",
               'Vnukovo', 'Juzhnoe Tushino', 'Severnoe Tushino',
               "Chertanovo Central'noe", 'Fili Davydkovo', 'Otradnoe',
               'Novo-Peredelkino', 'Bogorodskoe', 'Jaroslavskoe', 'Strogino',
               'Hovrino', "Moskvorech'e-Saburovo", 'Staroe Krjukovo', 'Ljublino',
               'Caricyno', 'Veshnjaki', 'Danilovskoe', 'Preobrazhenskoe',
               "Kon'kovo", 'Brateevo', 'Vostochnoe Izmajlovo', 'Vyhino-Zhulebino',
               'Donskoe', 'Novogireevo', 'Juzhnoe Butovo', 'Sokol', 'Kurkino',
               'Izmajlovo', 'Severnoe Medvedkovo', 'Rostokino',
               'Orehovo-Borisovo Severnoe', 'Ochakovo-Matveevskoe', 'Taganskoe',
               'Dmitrovskoe', 'Orehovo-Borisovo Juzhnoe', 'Teplyj Stan',
               'Babushkinskoe', 'Pokrovskoe Streshnevo', 'Obruchevskoe',
               'Filevskij Park', 'Troparevo-Nikulino', 'Severnoe Butovo',
               'Hamovniki', 'Solncevo', 'Dorogomilovo', 'Timirjazevskoe',
               'Lianozovo', 'Pechatniki', 'Krjukovo', 'Jasenevo',
               'Chertanovo Severnoe', 'Rjazanskij', 'Silino', 'Ivanovskoe',
               'Golovinskoe', 'Novokosino', 'Nagatino-Sadovniki',
               'Birjulevo Vostochnoe', 'Severnoe Izmajlovo', 'Sokolinaja Gora',
               'Vostochnoe Degunino', 'Prospekt Vernadskogo', 'Savelki',
               'Ajeroport', 'Vojkovskoe', 'Beskudnikovskoe', 'Krylatskoe',
               'Juzhnoportovoe', 'Perovo', 'Akademicheskoe', 'Horoshevo-Mnevniki',
               'Shhukino', 'Kapotnja', 'Horoshevskoe', 'Marfino',
               'Chertanovo Juzhnoe', 'Savelovskoe', 'Birjulevo Zapadnoe',
               'Nekrasovka', 'Cheremushki', 'Sviblovo', 'Alekseevskoe',
               "Krasnosel'skoe", 'Kotlovka', 'Zjuzino', 'Ostankinskoe',
               'Tverskoe', 'Losinoostrovskoe', 'Butyrskoe', 'Matushkino',
               'Metrogorodok', 'Juzhnoe Medvedkovo', 'Lomonosovskoe', 'Jakimanka',
               'Mozhajskoe', 'Levoberezhnoe', "Mar'ina Roshha", 'Gagarinskoe',
               "Zamoskvorech'e", "Altuf'evskoe", 'Ramenki', 'Zjablikovo',
               'Meshhanskoe', 'Severnoe', 'Begovoe', 'Arbat',
               'Poselenie Sosenskoe', 'Poselenie Moskovskij',
               'Poselenie Pervomajskoe', 'Poselenie Desjonovskoe',
               'Poselenie Voskresenskoe', 'Poselenie Mosrentgen',
               'Troickij okrug', 'Poselenie Shherbinka',
               'Poselenie Filimonkovskoe', 'Poselenie Vnukovskoe',
               'Poselenie Marushkinskoe', 'Poselenie Shhapovskoe',
               'Poselenie Rjazanovskoe', 'Poselenie Kokoshkino', 'Vostochnoe',
               'Poselenie Krasnopahorskoe', 'Poselenie Novofedorovskoe',
               'Poselenie Voronovskoe', 'Poselenie Klenovskoe',
               'Poselenie Rogovskoe', 'Poselenie Kievskij', 'Molzhaninovskoe',
               'Poselenie Mihajlovo-Jarcevskoe']

app = dash.Dash()

app.layout = html.Div([
    html.H1("House price prediction",
            style={'text-align': 'center'}),

    html.H3("House price prediction based on Sberbank Russian Housing Market data",
            style={'text-align': 'center'}),
    html.Div([
        dcc.Markdown(dedent("Please select the **Name of your district**"))
    ], style={'display': 'inline-block', 'width': '100%', 'margin': '1.5vh'}),
    html.Div([
        dcc.Dropdown(
            options=[{'label': name, 'value': name} for name in sub_regions],
            id='sub_region'
        )], style={'display': 'inline-block', 'width': '100%', 'margin': '1.5vh'}),

    html.Div([
        dcc.Markdown(dedent("Please input the **total area** in square meters, including _loggias,"
                            " balconies and other non-residential areas_"))
    ], style={'display': 'inline-block', 'width': '100%', 'margin': '1.5vh'}),
    html.Div([
        dcc.Input(
            placeholder='Full area',
            type='number',
            value='',
            step=1,
            id='full_area'
        )], style={'display': 'inline-block', 'width': '100%', 'margin': '1.5vh'}),

    html.Div([
        dcc.Markdown(dedent("Please set the approximate distance range from your home to nearest"
                            " **Public Transport Station** (km)"))
    ], style={'display': 'inline-block', 'width': '100%', 'margin': '1.5vh'}),
    html.Div([
        dcc.RangeSlider(
            min=0,
            max=5,
            step=0.1,
            value=[1, 3],
            marks={
                0: {'label': '0'},
                0.5: {'label': '0.5'},
                1: {'label': '1'},
                1.5: {'label': '1.5'},
                2: {'label': '2'},
                2.5: {'label': '2.5'},
                3: {'label': '3'},
                3.5: {'label': '3.5'},
                4: {'label': '4'},
                4.5: {'label': '4.5'},
                5: {'label': '5'},
            },
            id='transport_distance'
        )], style={'display': 'inline-block', 'width': '100%', 'margin': '1.5vh'}),
    html.Div([
        dcc.Markdown(dedent("Please input the approximate number of **Shopping Malls** within 2 km from your house"))
    ], style={'display': 'inline-block', 'width': '100%', 'margin': '1.5vh'}),
    html.Div([
        dcc.Input(
            placeholder='Shopping Malls within 2km',
            type='number',
            value='',
            step=1,
            id='mall_count'
        )], style={'display': 'inline-block', 'width': '100%', 'margin': '1.5vh'}),

    html.Div([
        dcc.Markdown(
            dedent("Please input the approximate number of **Leisure Facilities** within 500m from your house"))
    ], style={'display': 'inline-block', 'width': '100%', 'margin': '1.5vh'}),
    html.Div([
        dcc.Input(
            placeholder='Leisure facilities',
            type='number',
            value='',
            step=1,
            id='leisure_facilities'
        )], style={'display': 'inline-block', 'width': '100%', 'margin': '1.5vh'}),

    html.Button('Submit', id='button', style={'display': 'inline-block', 'margin': '1.5vh'}),

    html.Div(id="output"),

    html.Div([
        dcc.Markdown("Created by Henrik Sergoyan and Grigor Bezirganyan: github.com/bezirganyan/House_price_predictor")
    ])
], style={'display': 'inline-block', 'width': '120vh', 'margin-left': '35vh', 'margin-right': '35vh'})


@app.callback(dash.dependencies.Output('output', 'children'),
              [dash.dependencies.Input('button', 'n_clicks'),
               dash.dependencies.Input('sub_region', 'value'),
               dash.dependencies.Input('full_area', 'value'),
               dash.dependencies.Input('transport_distance', 'value'),
               dash.dependencies.Input('mall_count', 'value'),
               dash.dependencies.Input('leisure_facilities', 'value')])
def update_rank_plot(n_clicks, sub_region, full_area, transport_distance, mall_count, leisure_facilities):

    if n_clicks is None:
        return ""

    prediction = predict(mean(transport_distance), mall_count, leisure_facilities, full_area, sub_region)

    return dcc.Markdown(dedent("### The calculated value for your house is approximately **"
                               + str(round(prediction[0])) + " RUB**"))


app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

if __name__ == '__main__':
    app.run_server()
