import streamlit as st
import duckdb
import pandas as pd
import os
from faker import Faker
import random
from datetime import datetime, timedelta

# Configuración de la página del dashboard
st.set_page_config(page_title="Dashboard de Transacciones", page_icon="📊", layout="wide")

DB_PATH = "data/analytics.duckdb"

def generate_and_load_data():
    """Genera datos sintéticos y crea la base de datos DuckDB si no existe."""
    os.makedirs("data/raw", exist_ok=True)
    
    # Si la base de datos no existe, la creamos al vuelo
    if not os.path.exists(DB_PATH):
        fake = Faker()
        Faker.seed(42)
        random.seed(42)
        
        products = [
            {"name": "Laptop Pro 15", "price": 1200.00},
            {"name": "Wireless Mouse", "price": 25.50},
            {"name": "Mechanical Keyboard", "price": 85.00},
            {"name": "UltraWide Monitor 27", "price": 350.00},
            {"name": "USB-C Hub Multiport", "price": 45.00},
            {"name": "Noise-Cancelling Headphones", "price": 199.99}
        ]
        locations = ["Buenos Aires", "Córdoba", "Rosario", "Mendoza", "Puerto Madryn"]
        
        data = []
        # Generamos una muestra eficiente para la nube
        for i in range(1, 5001):
            prod = random.choice(products)
            qty = random.randint(1, 5)
            data.append({
                "transaction_id": f"TXN-{i:05d}",
                "date": fake.date_between(start_date='-1y', end_date='today').strftime('%Y-%m-%d'),
                "customer_email": fake.email(),
                "product_name": prod["name"],
                "quantity": qty,
                "unit_price": prod["price"],
                "total_amount": qty * prod["price"],
                "store_location": random.choice(locations)
            })
            
        df_synthetic = pd.DataFrame(data)
        
        # Conectar y guardar en DuckDB
        con = duckdb.connect(DB_PATH)
        con.execute("CREATE OR REPLACE TABLE transactions AS SELECT * FROM df_synthetic")
        con.close()

# Asegurar que los datos y la BD existen antes de cargar
generate_and_load_data()

st.title("📊 Panel de Control y Analítica de Transacciones")
st.markdown("Visualización interactiva conectada directamente a nuestra base de datos analítica con **DuckDB**.")

@st.cache_data
def load_data():
    if not os.path.exists(DB_PATH):
        return None
    con = duckdb.connect(DB_PATH, read_only=True)
    df = con.execute("SELECT * FROM transactions").fetchdf()
    con.close()
    return df

df = load_data()

if df is None or df.empty:
    st.warning("⚠️ No se encontró la base de datos o está vacía.")
else:
    # --- MÉTRICAS PRINCIPALES ---
    total_sales = df['total_amount'].sum()
    total_transactions = len(df)
    avg_ticket = df['total_amount'].mean()

    col1, col2, col3 = st.columns(3)
    col1.metric("Ventas Totales", f"${total_sales:,.2f} USD")
    col2.metric("Transacciones Exitosas", f"{total_transactions:,}")
    col3.metric("Ticket Promedio", f"${avg_ticket:,.2f} USD")

    st.markdown("---")

    # --- GRÁFICOS Y FILTROS ---
    st.subheader("Desglose Geográfico y por Producto")
    
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("##### Ventas por Ubicación de Tienda")
        sales_by_location = df.groupby('store_location')['total_amount'].sum().reset_index()
        st.bar_chart(sales_by_location.set_index('store_location'))

    with col_b:
        st.markdown("##### Ingresos por Producto")
        sales_by_product = df.groupby('product_name')['total_amount'].sum().reset_index()
        st.bar_chart(sales_by_product.set_index('product_name'))

    # --- TABLA DE DATOS RECIENTES ---
    st.markdown("---")
    st.subheader("🔍 Últimas Transacciones Registradas")
    st.dataframe(df[['transaction_id', 'date', 'customer_email', 'product_name', 'quantity', 'total_amount', 'store_location']].head(10))