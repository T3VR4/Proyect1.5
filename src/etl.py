import os
import pandas as pd
import duckdb

def run_etl():
    input_file = "data/raw/transactions_raw.csv"
    db_file = "data/analytics.duckdb"
    
    print("1. Leyendo datos en bruto con Pandas...")
    df = pd.read_csv(input_file)
    print(f"   -> Filas originales leídas: {len(df)}")
    
    print("2. Limpiando y transformando datos...")
    # Eliminar registros donde el correo electrónico esté vacío o nulo
    df = df.dropna(subset=['customer_email'])
    df = df[df['customer_email'].str.strip() != ""]
    
    # Corregir o filtrar cantidades negativas (anomalías que introdujimos a propósito)
    # Las convertimos a positivas o filtramos; en este caso filtramos cantidades mayores a 0
    df = df[df['quantity'] > 0]
    
    # Crear una columna calculada de valor total de la transacción
    df['total_amount'] = df['quantity'] * df['unit_price']
    
    print(f"   -> Filas después de la limpieza: {len(df)}")
    
    print("3. Guardando datos limpios en DuckDB...")
    os.makedirs(os.path.dirname(db_file), exist_ok=True)
    
    # Conectarse a DuckDB (crea la base de datos localmente si no existe)
    con = duckdb.connect(db_file)
    
    # Cargar el DataFrame de Pandas directamente como una tabla analítica en DuckDB
    con.execute("CREATE OR REPLACE TABLE transactions AS SELECT * FROM df")
    
    # Verificar haciendo una consulta rápida de prueba
    result = con.execute("SELECT COUNT(*) AS total_rows FROM transactions").fetchone()
    print(f"   -> ¡Tabla 'transactions' creada con éxito en DuckDB! Total de registros limpios: {result[0]}")
    
    con.close()
    print("¡ETL completado exitosamente!")

if __name__ == "__main__":
    run_etl()