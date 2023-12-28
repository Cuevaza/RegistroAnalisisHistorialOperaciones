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
start_date = "18 Dec 2023"
end_date = "19 Dec 2023"

# Convierte las fechas a milisegundos desde la época
start_date = int(datetime.strptime(start_date, "%d %b %Y").timestamp() * 1000)
end_date = int(datetime.strptime(end_date, "%d %b %Y").timestamp() * 1000)

# Obtiene el historial de operaciones
trades = client.get_my_trades(symbol=symbol, startTime=start_date, endTime=end_date, limit=2000)

# Inicializa las sumas de los valores netos de compra y venta
total_buy_value = 0
total_sell_value = 0

# Inicializa los contadores de operaciones de compra y venta
buy_counter = 0
sell_counter = 0

# Escribe los datos en un archivo CSV
with open(f'{symbol}_trades.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    # Escribe los encabezados de las columnas
    writer.writerow(["ID", "Precio Compra", "Cantidad Compra", "Valor Neto Compra", "Total Valor Neto Compra", "Número de Compras", "Fecha y Hora Compra", "Es el Mejor Precio de Compra?", "Precio Venta", "Cantidad Venta", "Valor Neto Venta", "Total Valor Neto Venta", "Número de Ventas", "Fecha y Hora Venta", "Es el Mejor Precio de Venta?"])
    # Escribe los datos de cada operación
    for trade in trades:
        # Convierte la marca de tiempo a un formato de fecha y hora
        timestamp = datetime.fromtimestamp(trade['time'] / 1000).strftime("%m-%d-%Y %H:%M:%S")
        # Formatea el precio como decimal con 7 dígitos de precisión
        price = "{:.7f}".format(float(trade['price']))
        if trade['isBuyer']:
            buy_counter += 1
            total_buy_value += float(price) * float(trade['qty'])
            writer.writerow([trade['id'], price, trade['qty'], float(price) * float(trade['qty']), total_buy_value, buy_counter, timestamp, trade['isBestMatch'], '', '', '', '', '', ''])
        else:
            sell_counter += 1
            total_sell_value += float(price) * float(trade['qty'])
            writer.writerow([trade['id'], '', '', '', '', '', '', price, trade['qty'], float(price) * float(trade['qty']), total_sell_value, sell_counter, timestamp, trade['isBestMatch']])