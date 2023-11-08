from flask import Flask, render_template, request, redirect, url_for
from bisect import bisect_left


app = Flask(__name__)
# Data
DISTANCE_RANGES = [10, 15, 30, 40, 60, 105, 150, 185]
WEIGHT_RANGES = [50, 100, 300, 400, 700, 1000, 1300, 2000, 3000, 4000, 5000, 6000, 7000, 10000, 120000, 160000, 240000]
PRICES = [
    [6.73, 8.97, 11.21, 15.14, 18.84, 21.31, 26.36, 34.76, 41.49, 47.10, 52.71, 61.68, 69.53, 86.91, 98.68, 179.42, 201.85],
    [8.97, 11.21, 14.58, 18.51, 23.33, 25.79, 30.84, 40.37, 47.10, 52.71, 58.31, 67.28, 76.26, 98.13, 112.14, 179.42, 201.85],
    [14.58, 16.82, 20.19, 25.79, 30.28, 32.52, 38.13, 48.22, 54.95, 61.68, 67.28, 77.38, 86.35, 109.34, 123.35, 224.28, 246.71],
    [19.06, 21.31, 24.67, 31.40, 35.88, 38.13, 43.73, 53.83, 60.56, 67.28, 74.01, 84.11, 93.08, 118.87, 132.33, 246.71, 302.78],
    [28.04, 30.28, 33.64, 40.37, 44.86, 48.22, 53.83, 63.92, 70.65, 78.50, 85.23, 97.56, 106.53, 132.33, 145.78, 269,14, 330.81],
    [53.83, 58.31, 61.68, 68.41, 72.89, 77.38, 85.23, 95.32, 102.05, 112.14, 124.48, 136.81, 151.39, 177.18, 190.64, 325.21, 386.88],
    [84.11, 88.59, 95.32, 102.05, 106.53, 111.02, 118.87, 128.96, 135.69, 151.39, 163.72, 176.06, 190.64, 216.43, 229.89, 364.46, 431.74],
    [201.85, 201.85, 216.43, 216.43, 216.43, 216.43, 224.28, 224.28, 224.28, 235.49, 235.49, 252.42, 252.42, 269.14, 291.56, 364.46, 432.74]
]
PUEBLOS = [
    {"nombre": "ABRERA", "km": 36},
    {"nombre": "AIGUAFREDA", "km": 64},
    {"nombre": "ELS ALAMÚS", "km": 145},
    {"nombre": "L'AMETLLA DEL VALLÈS", "km": 35},
    {"nombre": "ARENYS DE MUNT", "km": 45},
    {"nombre": "ARGENTONA", "km": 32},
    {"nombre": "BADALONA", "km": 14},
    {"nombre": "BANYOLES", "km": 121},
    {"nombre": "BARBERÀ DEL VALLÈS", "km": 17},
    {"nombre": "BELLATERRA", "km": 22},
    {"nombre": "BELLVEI", "km": 62},
    {"nombre": "BESCANÓ", "km": 93},
    {"nombre": "BIGUES I RIELLS", "km": 42},
    {"nombre": "BORDILS", "km": 126},
    {"nombre": "CABRERA DE MAR", "km": 29},
    {"nombre": "CALDES DE MONTBUI", "km": 35},
    {"nombre": "CANET DE MAR", "km": 43},
    {"nombre": "CANOVELLES", "km": 31},
    {"nombre": "CARDEDEU", "km": 36},
    {"nombre": "CASSÀ DE LA SELVA", "km": 106},
    {"nombre": "CASTELLAR DEL VALLÈS", "km": 40},
    {"nombre": "CASTELLGALÍ", "km": 61},
    {"nombre": "CALELLA", "km": 51},
    {"nombre": "CASTELLVÍ DE ROSANES", "km": 32},
    {"nombre": "CASTELLBISBAL", "km": 24},
    {"nombre": "CARDONA", "km": 99},
    {"nombre": "CELRÀ", "km": 111},
    {"nombre": "CENTELLES", "km": 61},
    {"nombre": "CERDANYOLA DEL VALLÈS", "km": 14},
    {"nombre": "CERVELLÓ", "km": 25},
    {"nombre": "CONSTANTÍ", "km": 113},
    {"nombre": "CORNELLÀ DE LLOBREGAT", "km": 9},
    {"nombre": "CORRO D'AMUNT", "km": 31},
    {"nombre": "COMAJULIANA (GIRONA)", "km": 75},
    {"nombre": "DOSRIUS", "km": 37},
    {"nombre": "EL MASNOU", "km": 17},
    {"nombre": "EL PAPIOL", "km": 19},
    {"nombre": "ESPARREGUERA", "km": 38},
    {"nombre": "ESPLUGUES DE LLOBREGAT", "km": 14},
    {"nombre": "FOGARS DE LA SELVA", "km": 79},
    {"nombre": "FIGUERES", "km": 142},
    {"nombre": "GAVÀ", "km": 18},
    {"nombre": "GELIDA", "km": 35},
    {"nombre": "GURB", "km": 78},
    {"nombre": "GRANOLLERS", "km": 31},
    {"nombre": "LA GARRIGA", "km": 42},
    {"nombre": "LA GRANADA", "km": 54},
    {"nombre": "LA LLAGOSTA", "km": 16},
    {"nombre": "LA ROCA DEL VALLÈS", "km": 32},
    {"nombre": "LES FRANQUESES DEL VALLÈS", "km": 31},
    {"nombre": "LES PRESES", "km": 116},
    {"nombre": "LLIÇÀ D'AMUNT", "km": 33},
    {"nombre": "LLIÇÀ DE VALL", "km": 31},
    {"nombre": "LLINARS DEL VALLÈS", "km": 40},
    {"nombre": "MAÇANET DE LA SELVA", "km": 82},
    {"nombre": "MALLA", "km": 67},
    {"nombre": "MANLLEU", "km": 75},
    {"nombre": "MARTORELL", "km": 24},
    {"nombre": "MATARÓ", "km": 32},
    {"nombre": "MOIÀ", "km": 62},
    {"nombre": "MOLLET DEL VALLÈS", "km": 32},
    {"nombre": "MONTMELO", "km": 38},
    {"nombre": "MONTBLANC", "km": 106},
    {"nombre": "MONTCADA I REIXAC", "km": 12},
    {"nombre": "MONTORNÈS DEL VALLÈS", "km": 25},
    {"nombre": "MOLINS DE REI", "km": 15},
    {"nombre": "OLESA DE MONTSERRAT", "km": 38},
    {"nombre": "PALAFOLLS", "km": 62},
    {"nombre": "PALAU-SOLITÀ I PLEGAMANS", "km": 43},
    {"nombre": "PALAU DE PLEGAMANS", "km": 43},
    {"nombre": "LA PALMA DE CERVELLÓ", "km": 23},
    {"nombre": "PALOL DE RECARDIT", "km": 114},
    {"nombre": "PALOL REVARDIT", "km": 114},
    {"nombre": "PARETS V", "km": 24},
    {"nombre": "PINEDA MAR", "km": 55},
    {"nombre": "POLINYA", "km": 29},
    {"nombre": "PONT D'AMENTERA", "km": 90},
    {"nombre": "PREMIA DE DAL Y MAR", "km": 23},
    {"nombre": "REUS", "km": 108},
    {"nombre": "RIPOLLET", "km": 15},
    {"nombre": "RIUDELLOTS DE LA SELVA", "km": 92},
    {"nombre": "Riells i Viabrea, Girona", "km": 70},
    {"nombre": "RUBI", "km": 21},
    {"nombre": "SABADELL", "km": 24},
    {"nombre": "SALT", "km": 104},
    {"nombre": "SANT CEBRIA DE VALLATA", "km": 50},
    {"nombre": "SANT FELIU DE GUIXOLS", "km": 109},
    {"nombre": "SANT POL DE MAR", "km": 47},
    {"nombre": "SENTMENAT", "km": 39},
    {"nombre": "SORA", "km": 98},
    {"nombre": "SOSES", "km": 170},
    {"nombre": "SANT ADRIA DE BESOS", "km": 7},
    {"nombre": "SANT ANDREU B", "km": 25},
    {"nombre": "SANT ANDREU DE LA BARCE", "km": 25},
    {"nombre": "SANT ANTONI DE VILAMAJOR", "km": 44},
    {"nombre": "SANT BOI", "km": 12},
    {"nombre": "SANT CEBRIA", "km": 50},
    {"nombre": "SANT CEBRIA DE VALLATA", "km": 50},
    {"nombre": "SANT CELONI", "km": 50},
    {"nombre": "SANT CUGAT", "km": 19},
    {"nombre": "SANTA EULALIA DE RONCADA", "km": 38},
    {"nombre": "SANT FELIU LLOBREGAT", "km": 16},
    {"nombre": "SANT FOST CAMP", "km": 23},
    {"nombre": "SANT INSCLE", "km": 49},
    {"nombre": "SANT JOAN DE LES ABANDESS", "km": 117},
    {"nombre": "SANT JOAN DESPI", "km": 11},
    {"nombre": "SANT JOAN LES FONS", "km": 147},
    {"nombre": "SANT JULIA DE VILATORTA", "km": 75},
    {"nombre": "SANT JULIA DE RAMIS", "km": 110},
    {"nombre": "SANT JUST DEVERN", "km": 12},
    {"nombre": "SANT MIQUEL DE BELENYA", "km": 62},
    {"nombre": "SANT PERE VILAM", "km": 46},
    {"nombre": "SANT POL DE MAR", "km": 47},
    {"nombre": "SANT QUIRZE", "km": 22},
    {"nombre": "SANT VICENT DL HORTS", "km": 18},
    {"nombre": "SANT VICENT DE CASTELLET", "km": 58},
    {"nombre": "SANTA COLOMA", "km": 92},
    {"nombre": "SANTA MARIA PALAU TORDERA", "km": 52},
    {"nombre": "SANTA PERPETUA DE MOGODA", "km": 24},
    {"nombre": "TARRAGONA", "km": 108},
    {"nombre": "TEIA", "km": 20},
    {"nombre": "TERRASA", "km": 32},
    {"nombre": "TONA", "km": 69},
    {"nombre": "TORDERA", "km": 65},
    {"nombre": "TORELLES DE FOIX", "km": 59},
    {"nombre": "TORELLO", "km": 83},
    {"nombre": "VALLIRANA", "km": 22},
    {"nombre": "VALLS", "km": 88},
    {"nombre": "VIC", "km": 67},
    {"nombre": "VILADECANS", "km": 16},
    {"nombre": "VILADECAVALLS", "km": 36},
    {"nombre": "VILAMALLA", "km": 133},
    {"nombre": "VILASSAR DAlT y MAR", "km": 24},
    {"nombre": "VILLALBA SASERRA", "km": 44},
    {"nombre": "VILLANOVA GECTRU", "km": 48},
]


history = []

def calculate_price_with_cubic_weight(distance, weight, metros_cubicos, is_adr):
    # Calculate the equivalent weight for cubic meters
    cubic_weight = metros_cubicos * 270

    # Use the greater of the two weights for determining the price
    final_weight = max(weight, cubic_weight)

    # Get the appropriate indices for the values
    distance_index = bisect_left(DISTANCE_RANGES, distance)
    weight_index = bisect_left(WEIGHT_RANGES, final_weight)

    used_cubic_meters = cubic_weight > weight

    # Get the base price based on the determined indices
    base_price = PRICES[distance_index][weight_index]

    # If ADR is selected, calculate the ADR cost (30% of the base price)
    adr_cost = base_price * 0.3 if is_adr else 0.0

    return base_price, used_cubic_meters, cubic_weight, adr_cost


@app.route('/', methods=['GET', 'POST'])
def index():
    price = None
    used_cubic_meters = False
    cubic_weight = None
    is_adr = False
    adr_cost = 0.0
    error_message = None

    if request.method == 'POST':
        
        distance = float(request.form.get('distancia', 0))
        weight = float(request.form.get('peso', 0))
        metros_cubicos = float(request.form.get('metros_cubicos', 0))
        is_adr = 'adr' in request.form
        if distance <= 0 or weight <= 0 or metros_cubicos <= 0:
            raise ValueError("Todos los valores deben ser positivos y mayores que cero.")
        base_price, used_cubic_meters, cubic_weight, adr_cost = calculate_price_with_cubic_weight(distance, weight, metros_cubicos, is_adr)
        history.append({
        'distance': distance,
        'weight': weight,
        'cubic_meters': metros_cubicos,
        'used_cubic_meters': used_cubic_meters,
        'price': base_price,
        'cubic_weight': cubic_weight,
        'is_adr': is_adr,
        'adr_cost': adr_cost
    })
    return render_template('index.html', price=price, history=history, error_message=error_message, pueblos=PUEBLOS)

@app.route('/clear-history', methods=['POST'])
def clear_history():
    history.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)