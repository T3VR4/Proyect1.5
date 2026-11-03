import streamlit as st
import duckdb
import pandas as pd

# Configuración de la página del dashboard
st.set_page_config(page_title="Dashboard de Transacciones", page_icon="📊", layout="wide")

st.title("📊 Panel de Control y Analítica de Transacciones")
st.markdown("Visualización interactiva conectada directamente a nuestra base de datos analítica local con **DuckDB**.")

# Conexión a DuckDB
DB_PATH = "data/analytics.duckdb"

@st.cache_data
def load_data():
    if not pd.io.common.file_exists(DB_PATH):
        return None
    con = duckdb.connect(DB_PATH, read_only=True)
    df = con.execute("SELECT * FROM transactions").fetchdf()
    con.close()
    return df

df = load_data()

if df is None or df.empty:
    st.warning("⚠️ No se encontró la base de datos o está vacía. Ejecuta primero el script ETL (`python src/etl.py`).")
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