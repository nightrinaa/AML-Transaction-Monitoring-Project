# AML Transaction Monitoring Project

This project simulates a financial transaction monitoring system used in AML (Anti-Money Laundering).  
In this project i want to demonstrates practical knowledge of transaction monitoring, risk scoring, and detection of suspicious activity.

- OBJECTIVE -
The goal of this project is to:
- Generate synthetic customer and transaction data
- Apply AML red flags to identify suspicious behavior
- Calculate risk scores for transactions
- Demonstrate basic transaction analysis

- FEATURES -

- Synthetic customer and transaction data generation
- Rule-based risk scoring model
- AML red flag detection including:
  - High-value transactions
  - Transactions involving high-risk countries
  - Round-number transactions (possible structuring)
  - Activity near reporting thresholds
  - Rapid movement of funds
  - Mismatched customer profiles
  - Unexplained wealth
- Suspicious transaction identification
- Simple summary analytics

- AML LOGIC IMPLEMENTED -

Transactions are evaluated using multiple risk indicators. Each transaction receives a **risk score** based on:
1. High-value transactions (amounts > $10,000)  
2. High-risk countries (e.g., IR, KP, SY, AF, RU)  
3. Round amounts (e.g., 10,000, 5,000)  
4. Near-threshold activity (close to reporting threshold)  
5. Rapid fund movement (frequent transactions in short time)  
6. Mismatched customer profiles (behavior unusual for customer)  
7. Unexplained wealth (randomly flagged for simulation)  
8. Use of crypto transactions (adds extra risk)  
9. Politically Exposed Persons (PEPs)

Transactions with risk scores ≥ 60 are flagged as suspicious.

- OUTPUT -

The project generates two CSV files:

- `customers.csv` – customer dataset including:
  - `customer_id`  
  - `country`  
  - `pep` (politically exposed person)  
  - `registration_date`  
  - `unusual_wealth`  

- `transactions.csv` – transaction dataset including:
  - `transaction_id`  
  - `customer_id`  
  - `amount`  
  - `transaction_type`  
  - `channel` (online / ATM / branch)  
  - `destination_country`  
  - `timestamp`  
  - AML red flags columns (e.g., `round_amount`, `high_cash`, `near_threshold`)  
  - `risk_score`  
  - `suspicious` (True/False)  
  - `risk_level` (High/Medium/Low)  
  - `flag_reasons` (text explanation of triggered red flags)  
  - `date` (for daily analysis)

- EXAMPLE -

A transaction is flagged as suspicious if:

- Amount is high (> $10,000)  
- Destination country is high-risk  
- Multiple red flags are triggered  

- TECH STACK -

- Python 3.14  
- Pandas  

- RESULTS -
This project demonstrates:

- Rule-based AML transaction monitoring  
- Risk scoring and red flag detection  
- Identification and explanation of suspicious transactions  
- Basic data analysis skills applicable to Risk & Compliance roles
