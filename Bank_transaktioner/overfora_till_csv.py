import pandas as pd
import psycopg2
import os
from datetime import datetime



# === 1. Läs in filerna ===
base_path = r"C:\Users\Book\Bank-transaktioner\Bank_transntioner"

customers = pd.read_csv(os.path.join(base_path, "./data/customers_cleaned.csv"))
accounts = pd.read_csv(os.path.join(base_path, "./data/accounts_cleaned.csv"))
transactions = pd.read_csv(os.path.join(base_path, "./data/transactions_cleaned_trimmed.csv"))

# === 2. Rensa och konvertera ===
for df in [customers, accounts, transactions]:
    df.columns = df.columns.str.strip()

accounts['BankAccount'] = accounts['BankAccount'].astype(str).str.strip()
transactions['sender_account'] = transactions['sender_account'].astype(str).str.strip()
transactions['receiver_account'] = transactions['receiver_account'].astype(str).str.strip()
transactions['timestamp'] = pd.to_datetime(transactions['timestamp'])
transactions['amount'] = pd.to_numeric(transactions['amount'], errors='coerce')

# === 3. Valutakurser ===
exchange_rates = {
    "SEK": 1.0,
    "USD": 10.5,
    "EUR": 11.2,
    "DKK": 1.5,
    "NOK": 1.6,
    "JPY": 0.075,
    "GBP": 13.0,
    "ZAR": 0.55,
    "RMB": 1.45,
    "ZMW": 0.7
}
transactions['amount_sek'] = transactions.apply(
    lambda row: round(row['amount'] * exchange_rates.get(row['currency'], 1.0), 2),
    axis=1
)

# === 4. Anslut till PostgreSQL ===
conn = psycopg2.connect(
    dbname="grupp_arbete_sebank",
    user="postgres",
    password="Pipi-ina-18",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# === 5. Infoga kunder ===
for _, row in customers.iterrows():
    cur.execute("""
        INSERT INTO customers (personnummer, customer_name, phone, address)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (personnummer) DO NOTHING
    """, (row['Personnummer'], row['Customer'], row['Phone'], row['Address']))

# === 6. Infoga konton ===
for _, row in accounts.iterrows():
    cur.execute("""
        SELECT id FROM customers WHERE personnummer = %s
    """, (row['Personnummer'],))
    customer = cur.fetchone()
    if customer:
        customer_id = customer[0]
        cur.execute("""
            INSERT INTO accounts (bank_account, customer_id)
            VALUES (%s, %s)
            ON CONFLICT (bank_account) DO NOTHING
        """, (row['BankAccount'], customer_id))

# === 7. Skapa konto-ID-karta ===
cur.execute("SELECT id, bank_account FROM accounts")
account_id_map = {acc.strip(): id for id, acc in cur.fetchall()}

# === 8. Infoga transaktioner och missade transaktioner ===
inserted, skipped = 0, 0
for _, row in transactions.iterrows():
    sender_acc = row['sender_account']
    receiver_acc = row['receiver_account']
    sender_id = account_id_map.get(sender_acc)
    receiver_id = account_id_map.get(receiver_acc)

    if sender_id is None or receiver_id is None:
        # Lägg till i skipped_transactions med amount_sek
        amount_sek = round(row['amount'] * exchange_rates.get(row['currency'], 1.0), 2)
        cur.execute("""
            INSERT INTO skipped_transactions (
                transaction_id, timestamp, amount, currency, amount_sek,
                sender_account, receiver_account, sender_country,
                sender_municipality, receiver_country, receiver_municipality,
                transaction_type, notes
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (transaction_id) DO NOTHING
        """, (
            row['transaction_id'], row['timestamp'], row['amount'], row['currency'], amount_sek,
            sender_acc, receiver_acc, row['sender_country'],
            row['sender_municipality'], row['receiver_country'], row['receiver_municipality'],
            row['transaction_type'], row['notes']
        ))
        skipped += 1
        continue

    try:
        cur.execute("""
            INSERT INTO transactions (
                transaction_id, timestamp, amount, currency, amount_sek,
                sender_account_id, receiver_account_id, sender_country,
                sender_municipality, receiver_country, receiver_municipality,
                transaction_type, notes
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (transaction_id) DO NOTHING
        """, (
            row['transaction_id'], row['timestamp'], row['amount'], row['currency'], row['amount_sek'],
            sender_id, receiver_id, row['sender_country'],
            row['sender_municipality'], row['receiver_country'], row['receiver_municipality'],
            row['transaction_type'], row['notes']
        ))
        inserted += cur.rowcount
    except Exception as e:
        print(f" Fel vid transaktion {row['transaction_id']}: {e}")
        skipped += 1

# === 9. Avsluta ===
conn.commit()
cur.close()
conn.close()

print(f"\nTransaktioner inlagda: {inserted}")
print(f"Överhoppade pga saknade konton: {skipped}")
