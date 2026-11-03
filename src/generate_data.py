import os
import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()

def generate_sales_csv(num_rows=50000, filename="data/raw/transactions_raw.csv"):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    products = [
        ("Laptop Gamer", 1200.00, "USD"),
        ("Mouse Inalámbrico", 25.50, "USD"),
        ("Teclado Mecánico", 75.00, "USD"),
        ("Monitor 24''", 220.00, "USD"),
        ("Auriculares Bluetooth", 45.00, "USD"),
        ("Silla Ergonómica", 300.00, "USD")
    ]
    
    print(f"Generando {num_rows} registros de transacciones...")
    
    with open(filename, mode="w", encoding="utf-8") as f:
        f.write("transaction_id,date,customer_email,product_name,quantity,unit_price,currency,store_location\n")
        
        start_date = datetime.now() - timedelta(days=30)
        
        for i in range(1, num_rows + 1):
            t_id = f"TXN-{i:07d}"
            t_date = (start_date + timedelta(seconds=random.randint(0, 2592000))).strftime("%Y-%m-%d %H:%M:%S")
            
            # Introducir algunos nulos o anomalías a propósito para probar el ETL
            customer_email = "" if random.random() < 0.02 else fake.email()
            
            product, price, currency = random.choice(products)
            quantity = random.randint(1, 5)
            
            if random.random() < 0.01:
                quantity = -1  # Dato corrupto o negativo para probar la limpieza
                
            location = random.choice(["Buenos Aires", "Córdoba", "Rosario", "Mendoza", "Puerto Madryn"])
            
            f.write(f"{t_id},{t_date},{customer_email},{product},{quantity},{price},{currency},{location}\n")
            
    print(f"¡Archivo generado con éxito en '{filename}'!")

if __name__ == "__main__":
    generate_sales_csv(num_rows=50000)