import random
import uuid
from datetime import datetime, timedelta
import pandas as pd

NUM_CUSTOMERS = 100
NUM_TRANSACTIONS = 500

HIGH_RISK_COUNTRIES = ["IR","KP","SY","AF","RU"]
COUNTRIES = ["US","DE","PL","GB","FR","NL","IT","ES",
             "AE","RU","IR","SY","AF"]
TRANSACTION_TYPES = ["payment","transfer","withdrawal","crypto"]
CHANNELS = ["online","ATM","branch"]
THRESHOLD = 10000


def random_date(days=365):
    now = datetime.now()
    return now - timedelta(days=random.randint(0, days))


def generate_customers(n):
    customers = []
      for _ in range(n):
        customers.append({
            "customer_id": str(uuid.uuid4())[:8],
            "country": random.choice(COUNTRIES),
            "pep": random.random() < 0.05,
            "registration_date": random_date(1000),
            "unusual_wealth": random.random() < 0.03
        })

    return pd.DataFrame(customers)


def generate_transactions(customers, n):

    transactions = []
    ids = customers["customer_id"].tolist()

    for _ in range(n):

        amount = random.randint(50, 20000)

        transaction = {
            "transaction_id": str(uuid.uuid4())[:10],
            "customer_id": random.choice(ids),
            "amount": amount,
            "transaction_type": random.choice(TRANSACTION_TYPES),
            "channel": random.choice(CHANNELS),
            "destination_country": random.choice(COUNTRIES),
            "timestamp": random_date()
        }

        transaction["round_amount"] = amount % 1000 == 0
        transaction["high_cash"] = amount > 5000
        transaction["large_transfer"] = amount > 10000
        transaction["near_threshold"] = abs(amount - THRESHOLD) < 500
        transaction["high_risk_country"] = transaction["destination_country"] in HIGH_RISK_COUNTRIES
        transaction["rapid_movement"] = random.random() < 0.05
        transaction["mismatch_profile"] = random.random() < 0.03

        transactions.append(transaction)

    return pd.DataFrame(transactions)


def calculate_risk(row):

    score = 0

    if row["country"] in HIGH_RISK_COUNTRIES:
        score += 40

    if row["amount"] > 10000:
        score += 30
    elif row["amount"] > 3000:
        score += 15

    if row["transaction_type"] == "crypto":
        score += 20

    if row["destination_country"] in HIGH_RISK_COUNTRIES:
        score += 30

    if row["pep"]:
        score += 40

    if row["unusual_wealth"]:
        score += 25

    flags = [
        "round_amount","high_cash","large_transfer",
        "near_threshold","high_risk_country",
        "rapid_movement","mismatch_profile"
    ]

    for flag in flags:
        if row[flag]:
            score += 10

    return score


def explain_flags(row):

    reasons = []

    if row["round_amount"]:
        reasons.append("round amount")

    if row["high_cash"]:
        reasons.append("high cash")

    if row["large_transfer"]:
        reasons.append("large transfer")

    if row["near_threshold"]:
        reasons.append("near threshold")

    if row["high_risk_country"]:
        reasons.append("high risk country")

    if row["rapid_movement"]:
        reasons.append("rapid movement")

    if row["mismatch_profile"]:
        reasons.append("profile mismatch")

    return ", ".join(reasons)


def risk_category(score):
    if score >= 80:
        return "High"
    elif score >= 50:
        return "Medium"
    else:
        return "Low"


def simple_analysis(df):

    print("\n--- BASIC AML ANALYSIS ---")

    print("Total transactions:", len(df))

    print("\nSuspicious transactions:")
    print(df[df["suspicious"] == True].head())

    print("\nTop risky customers:")
    print(df.groupby("customer_id")["risk_score"].mean().sort_values(ascending=False).head())

    print("\nRisk level distribution:")
    print(df["risk_level"].value_counts())

    print("\nRed flags frequency:")

    flags = [
        "round_amount","high_cash","large_transfer",
        "near_threshold","high_risk_country",
        "rapid_movement","mismatch_profile"
    ]

    for flag in flags:
        print(flag, ":", df[flag].sum())


def main():

    customers = generate_customers(NUM_CUSTOMERS)

    transactions = generate_transactions(customers, NUM_TRANSACTIONS)

    df = transactions.merge(customers, on="customer_id")

    df["risk_score"] = df.apply(calculate_risk, axis=1)

    df["suspicious"] = df["risk_score"] >= 60

    df["flag_reasons"] = df.apply(explain_flags, axis=1)

    df["risk_level"] = df["risk_score"].apply(risk_category)

    df["date"] = pd.to_datetime(df["timestamp"]).dt.date

    customers.to_csv("customers.csv", index=False)
    df.to_csv("transactions.csv", index=False)

    print("Dataset created successfully!")

    simple_analysis(df)


if __name__ == "__main__":
    main()
