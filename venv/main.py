import time
import config
import csv
from binance.client import Client
from datetime import datetime, timedelta
from binance.exceptions import BinanceAPIException
from decimal import Decimal, ROUND_DOWN

# Crear cliente de Binance
api_key = config.api_key
api_secret = config.api_secret
client = Client(api_key, api_secret)

# Especifica el par de trading
symbol = "BTCUSDT"

# Especifica las fechas de inicio y fin (formato: "DD MM YYYY")
start_date = "15 Dec 2023"
end_date = "19 Dec 2023"

# Convierte las fechas a milisegundos desde la época
start_date = int(datetime.strptime(start_date, "%d %b %Y").timestamp() * 1000)
end_date = int(datetime.strptime(end_date, "%d %b %Y").timestamp() * 1000)

# Calcula el número de días entre las fechas de inicio y fin
num_days = (end_date - start_date) // (24 * 60 * 60 * 1000)

# Obtiene el historial de operaciones para cada día
trades = []
for i in range(num_days + 1):
    day_start = start_date + i * 24 * 60 * 60 * 1000
    day_end = day_start + 24 * 60 * 60 * 1000
    day_trades = client.get_my_trades(symbol=symbol, startTime=day_start, endTime=day_end, limit=1000)
    trades.extend(day_trades)

# Inicializa las sumas de los valores netos de compra y venta
total_buy_value = 0
total_sell_value = 0

# Inicializa los contadores de operaciones de compra y venta
buy_counter = 0
sell_counter = 0

# Inicializa las listas de operaciones de compra y venta
buy_trades = []
sell_trades = []

# Separa las operaciones de compra y venta
for trade in trades:
    # Convierte la marca de tiempo a un formato de fecha y hora
    timestamp = datetime.fromtimestamp(trade['time'] / 1000).strftime("%m-%d-%Y %H:%M:%S")
    # Formatea el precio como decimal con 7 dígitos de precisión
    price = "{:.7f}".format(float(trade['price']))
    if trade['isBuyer']:
        buy_counter += 1
        total_buy_value += float(price) * float(trade['qty'])
        buy_trades.append([trade['id'], price, trade['qty'], float(price) * float(trade['qty']), total_buy_value, buy_counter, timestamp])
    else:
        sell_counter += 1
        total_sell_value += float(price) * float(trade['qty'])
        sell_trades.append([trade['id'], price, trade['qty'], float(price) * float(trade['qty']), total_sell_value, sell_counter, timestamp])

# Escribe los datos en un archivo CSV
with open(f'{symbol}_trades.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    # Escribe los encabezados de las columnas
    writer.writerow(["ID Compras", "Precio Compra", "Cantidad Compra", "Valor Neto Compra", "Total Valor Neto Compra", "Número de Compras", "Fecha y Hora Compra", "ID Ventas", "Precio Venta", "Cantidad Venta", "Valor Neto Venta", "Total Valor Neto Venta", "Número de Ventas", "Fecha y Hora Venta"])
    # Escribe los datos de cada operación
    for i in range(max(len(buy_trades), len(sell_trades))):
        row = []
        if i < len(buy_trades):
            row.extend(buy_trades[i])
        else:
            row.extend(['', '', '', '', '', '', ''])
        if i < len(sell_trades):
            row.extend(sell_trades[i])
        else:
            row.extend(['', '', '', '', '', '', ''])
        writer.writerow(row)