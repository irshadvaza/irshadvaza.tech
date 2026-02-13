# 🏥 Hospital Domain – Healthcare Revenue Cycle Management (RCM)

---

# 1️⃣ Introduction to Revenue Cycle Management (RCM)

**Revenue Cycle Management (RCM)** is the complete financial process hospitals use to manage revenue —  
from the moment a patient schedules an appointment until the provider (hospital or doctor) receives full payment.

> RCM ensures hospitals get paid correctly and on time, while maintaining quality patient care.

**Key objectives of RCM:**
- Ensure timely cash collection  
- Reduce denials and delays  
- Minimize bad debt  
- Optimize operational efficiency  

---

# 2️⃣ Step-by-Step RCM Process

## 2.1 Patient Appointment & Registration

The revenue cycle begins **before treatment**.

**Activities:**
- Appointment scheduling  
- Patient demographic collection  
- Insurance verification and eligibility  
- Co-pay or deductible calculation  

**Example:**  
- Treatment cost = $1,000  
- Insurance covers 80%  
- Patient co-pay = 20% → $200  

This ensures proper payment tracking from day one.

---

## 2.2 Services Provided

After registration, the hospital provides medical services:

- Doctor consultation  
- Lab tests  
- Radiology  
- Surgery  
- Medications  

All services are recorded in:
- **EHR (Electronic Health Record)**  
- **HIS (Hospital Information System)**  

Correct coding (ICD / CPT) ensures accurate billing.

---

## 2.3 Medical Coding & Billing

**Steps:**
1. Convert services to billable codes  
2. Generate invoice  
3. Submit claim to insurance (or bill patient for self-pay)  

Accurate coding reduces denials and speeds up payment.

---

## 2.4 Claim Review by Insurance

Insurance evaluates claims:

| Status             | Meaning |
|------------------|---------|
| Approved          | Full payment |
| Partially Approved | Partial payment |
| Denied            | Claim rejected |

---

## 2.5 Payment Posting & Follow-up

- Insurance payment received → posted to system  
- Patient balance collected → posted  
- Follow-up on pending payments or denied claims  

---

## 2.6 Reporting & Performance Monitoring

Key monitoring includes:
- AR aging  
- Denial rate  
- Collection efficiency  
- Cash flow trends  

---

## 2.7 End-to-End RCM Flow Diagram

```
+--------------------+
| Patient Appointment |
+---------+----------+
          |
          v
+---------------------------+
| Registration & Insurance  |
+-----------+---------------+
            |
            v
+------------------+
| Services Provided |
+---------+--------+
          |
          v
+----------------+
| Medical Coding  |
+--------+-------+
         |
         v
+----------------+
| Claim Generation|
+--------+-------+
         |
         v
+------------------+
| Insurance Review |
+---+-----+--------+
    |     |
    v     v
Approved Partially Approved / Denied
    |     |
    v     v
Payment  Patient Balance / Rework Claim
    |     |
    v     v
+----------------+
| Payment Posting |
+--------+-------+
         |
         v
+-----------------------------+
| AR Reporting & KPI Tracking |
+-----------------------------+
```

---

flowchart TD
    A[Service Delivered] --> B[Invoice Generated]
    B --> C[Claim Sent to Insurance Company]
    C --> D[Insurance Decision]
    D -->|Approved| E[Insurance Payment]
    D -->|Partial/Denied| F[Patient Balance]
    F --> G[Payment Posting]
    G --> H[AR Aging Track]



# 3️⃣ Accounts Receivable (AR)

**Accounts Receivable (AR)** = Money owed to hospital for services already provided.

**Example:**  
- Treatment = $2,000  
- Insurance paid = $1,500  
- Patient owes = $500 → AR until collected

---

## 3.1 Objective of AR Team

- Bring cash into the hospital  
- Reduce collection period  
- Minimize bad debt  
- Follow up on denied claims  

---

## 3.2 AR Aging Concept

| Days Outstanding | Collection Probability |
|------------------|-----------------------|
| 0–30 Days | 93% |
| 31–60 Days | 85% |
| 61–90 Days | 73% |
| >90 Days | High risk of bad debt |

> The older the receivable, the lower the probability of collection.

---

## 3.3 AR Flow Diagram

```
+-----------------+
| Service Delivered|
+--------+--------+
         |
         v
+-----------------+
| Invoice Generated|
+--------+--------+
         |
         v
+-------------------+
| Claim Sent to     |
| Insurance Company |
+--------+----------+
         |
         v
+----------------------+
| Insurance Decision   |
+----+-------+---------+
     |       |
  Approved Partial/Denied
     |       |
     v       v
Insurance  Patient Balance
 Payment        |
     |         v
     +----> Payment Posting
                |
                v
        +----------------+
        | AR Aging Track |
        +----------------+
```

---

## 3.4 AR KPIs

### Days in AR
```
Days in AR = Total AR / Average Daily Revenue
```
**Example:**  
- Total AR = $900,000  
- Avg Daily Revenue = $30,000 → Days in AR = 30 days  
**Benchmark:** 30–40 days

### AR > 90 Days %
```
AR > 90 Days % = (AR > 90 days / Total AR) * 100
```
Lower is better.

### Denial Rate
```
Denied Claims / Total Claims
```
Target: <5%

### Net Collection Rate
```
Actual Collected / Total Eligible Amount
```
Target: >95%

---

# 4️⃣ Accounts Payable (AP)

**Accounts Payable (AP)** = Money the hospital owes to others.

**Examples:**  
- Supplier invoices  
- Staff salaries  
- Utility bills  

---

## 4.1 AP Flow Diagram

```
+------------------+
| Hospital Purchases|
+--------+---------+
         |
         v
+-----------------+
| Supplier Invoice |
+--------+--------+
         |
         v
+------------------+
| Invoice Verification |
+--------+----------+
         |
         v
+-----------------+
| Payment Approval |
+--------+--------+
         |
         v
+-----------------+
| Payment Made    |
+--------+--------+
         |
         v
+-----------------+
| AP Reporting    |
+-----------------+
```

---

# 5️⃣ Why Patient Payments Are Risky

1. **High Deductibles:** Patients delay until deductible is met  
2. **Low Insurance Coverage:** Higher out-of-pocket → higher risk  
3. **Private Clinics:** Partial advance + weak collection policies  
4. **Dental / Cosmetic Treatments:** Often fully self-pay → high default risk  

---

# 6️⃣ Data Engineering Perspective (RCM Analytics)

```
+-------------------------+
| Hospital Source Systems |
| (HIS / EHR / Billing)  |
+------------+------------+
             |
             v
+-------------------------+
| Azure Data Factory (ADF)|
+------------+------------+
             |
             v
+-------------------------+
| Azure Data Lake         |
| Bronze Layer            |
+------------+------------+
             |
             v
+-------------------------+
| Azure Databricks        |
| Transformations         |
+------------+------------+
             |
             v
+-------------------------+
| Silver Layer            |
+------------+------------+
             |
             v
+-------------------------+
| Gold Layer / RCM KPIs   |
+------------+------------+
             |
             v
+-------------------------+
| Power BI / Fabric       |
| Dashboards              |
+-------------------------+
```

---

# 📌 Summary

**Revenue Cycle Management** is the financial backbone of a hospital:

- Ensures stable cash flow  
- Supports financial sustainability  
- Enables high-quality patient care  

**Core pillars:**  
- **Accounts Receivable:** Money to collect  
- **Accounts Payable:** Money to pay  

> Healthy AR and optimized AP = Financially healthy hospital

