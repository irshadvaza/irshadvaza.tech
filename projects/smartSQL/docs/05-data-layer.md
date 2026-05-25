# Data Layer

[← RAG Deep Dive](./04-rag.md) · [Setup Guide →](./06-setup.md)

---

## Two data backends

SmartSQL supports two execution backends with identical interfaces — swap between them by changing one import line.

| Backend | File | Use case |
|---------|------|----------|
| **DuckDB + Parquet** | `db_handler_parquet.py` | Local files, Mac/Windows dev, no Java |
| **Azure SQL** | `db_handler.py` | Production cloud database |

Both return a `pd.DataFrame` from `run_query(sql)`. `mainui.py` works with either unchanged.

---

## DuckDB — local parquet queries

### What is DuckDB?

DuckDB is an in-process SQL database engine — a 30 MB pip install with no Java, no server, no configuration. It starts in milliseconds and runs SQL directly on parquet files using columnar projection (reads only the columns your query touches).

```
PySpark (original)                 DuckDB (new)
──────────────────                 ────────────
pip install pyspark   30 MB        pip install duckdb    30 MB
+ Java JDK            500 MB+
+ JAVA_HOME setup
+ SparkSession boot   15-30 sec    connection open       <1 sec
```

### The same SQL, different wrapper

```python
# Original PySpark
spark = SparkSession.builder.getOrCreate()
df = spark.read.format("parquet").load(path)
df.createOrReplaceTempView("taxi_trips")
result = spark.sql("SELECT COUNT(*) FROM taxi_trips")

# DuckDB replacement
conn = duckdb.connect(":memory:")
conn.execute(f"CREATE VIEW taxi_trips AS SELECT * FROM read_parquet('{path}')")
result = conn.execute("SELECT COUNT(*) FROM taxi_trips").df()
```

The SQL inside the quotes is identical. Only the Python wrapper changed.

### Columnar projection — why DuckDB is fast on large files

Parquet stores data in columns. If you have a 10 GB file with 50 columns and run:

```sql
SELECT fare_amount, COUNT(*) FROM taxi_trips GROUP BY fare_amount
```

DuckDB reads **only the `fare_amount` column** — approximately 2% of the file. A 10 GB file with a focused query responds in seconds.

### Security in `db_handler_parquet.py`

**Path validation:**
```python
def _validate_parquet_path(path: str) -> Path:
    resolved = Path(path).resolve(strict=True)  # raises if not found
    # resolve() follows symlinks — prevents symlinks pointing outside allowed dirs
    if not resolved.is_file():
        raise ValueError(f"Not a file: {path}")
    if resolved.suffix.lower() not in (".parquet", ".parq"):
        raise ValueError(f"Only .parquet files supported.")
    if not os.access(resolved, os.R_OK):
        raise ValueError(f"Permission denied: {resolved}")
    return resolved
```

`Path.resolve(strict=True)` catches directory traversal attacks (`../../etc/passwd`). The resolved absolute path is the real disk location — symlinks are followed and evaluated.

**DuckDB-specific SQL validation:**
```python
# Block reading arbitrary files directly in SQL
if "READ_PARQUET(" in sql.upper() or "READ_CSV(" in sql.upper():
    if TABLE_NAME.upper() not in sql.upper():
        raise ValueError("Query attempts to read an unauthorised file.")
```

DuckDB can read arbitrary files via `read_parquet('/any/path')`. This check blocks SQL that tries to access files other than the registered view.

---

## Azure SQL — production cloud database

### Connection pool (SQLAlchemy)

Opening a TCP connection to Azure SQL takes 200–500 ms. A connection pool pre-opens connections and reuses them across requests:

```python
engine = create_engine(
    connection_url,
    poolclass=QueuePool,
    pool_size=10,           # keep 10 connections open
    max_overflow=5,         # allow 5 extra under load
    pool_timeout=30,        # wait up to 30s for a connection
    pool_recycle=1800,      # replace connections every 30 min
    pool_pre_ping=True,     # test health before use
)
```

`pool_pre_ping=True` tests each connection with a lightweight query before use. If Azure SQL dropped an idle connection, the pool detects it and opens a fresh one transparently.

`pool_recycle=1800` prevents connections from being used for more than 30 minutes — Azure SQL silently drops connections idle for ~30 minutes, and this ensures the pool never serves a stale connection.

### Read-only connection string

```python
conn_str = (
    f"DRIVER={{{SQL_DRIVER}}};"
    f"SERVER={SQL_SERVER};DATABASE={SQL_DATABASE};"
    f"UID={SQL_USER};PWD={SQL_PASSWORD};"
    "Encrypt=yes;"                      # TLS encryption in transit
    "TrustServerCertificate=no;"        # validate server certificate
    f"Connection Timeout={QUERY_TIMEOUT};"
    "ApplicationIntent=ReadOnly;"       # route to read replica if available
)
```

`ApplicationIntent=ReadOnly` has two effects:
1. Tells Azure SQL this is a read-only workload — it can route to a secondary read replica, reducing load on the primary
2. Documents the intent clearly — a defence-in-depth signal alongside the SQL validation layer

### Parameterised execution

SQL is executed via `SQLAlchemy text()` which uses parameterised queries internally — treating the SQL as a code structure rather than a string, preventing second-order SQL injection:

```python
with engine.connect() as conn:
    conn.execute(text("SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED"))
    result = conn.execute(text(sql))
```

`READ UNCOMMITTED` reduces locking — acceptable for analytical read queries where exact consistency within a millisecond is not required.

---

## Row cap and timeout

Both backends enforce these limits:

```python
MAX_ROWS_RETURNED = 5000    # configurable via .env MAX_ROWS
QUERY_TIMEOUT_SEC = 30      # configurable via .env QUERY_TIMEOUT_SECONDS
```

**Row cap implementation (DuckDB):**
```python
if "LIMIT" not in sql.upper():
    safe_sql = f"SELECT * FROM ({sql}) AS _capped LIMIT {MAX_ROWS_RETURNED + 1}"
else:
    safe_sql = sql

df = conn.execute(safe_sql).df()

if len(df) > MAX_ROWS_RETURNED:
    df = df.iloc[:MAX_ROWS_RETURNED]
    df.attrs["capped"] = True          # flag for UI warning
```

Fetching `MAX + 1` rows then slicing allows detection of the cap without a separate COUNT query.

---

## Audit logging

Every query execution writes a structured log entry:

```
2025-07-14 09:23:41 [INFO] smartsql.db —
AUDIT | success=True | duration_ms=143.2 | rows=47 | sql_hash=a3f8c12e4b9d0127
```

**Fields:**
- `success` — True if query completed without error
- `duration_ms` — execution time in milliseconds
- `rows` — number of rows returned
- `sql_hash` — first 16 hex chars of SHA-256 hash of the SQL text

The SQL is stored as a hash — never as raw text. This allows incident correlation (you can identify which query caused an issue) without storing potentially sensitive query content in logs.

**CSV download events** are also logged:
```
AUDIT | download | rows=47 | session_query_count=3
```

---

## Schema helper

Both backends implement `get_schema()`, which `llm_parquet.py` calls at startup to inject real column names into the system prompt:

```python
def get_schema() -> pd.DataFrame:
    conn = _get_connection()
    df   = conn.execute(f"DESCRIBE {TABLE_NAME}").df()
    conn.close()
    return df[["column_name", "column_type"]]
```

**Output example:**
```
column_name                  column_type
VendorID                     BIGINT
tpep_pickup_datetime         TIMESTAMP
tpep_dropoff_datetime        TIMESTAMP
passenger_count              DOUBLE
trip_distance                DOUBLE
fare_amount                  DOUBLE
tip_amount                   DOUBLE
payment_type                 BIGINT
```

This is displayed in the Streamlit sidebar so users know exactly what to ask about.

---

## Switching between backends

`mainui.py` imports from whichever handler you configure:

```python
# For parquet / DuckDB:
from db_handler_parquet import run_query, get_schema, get_row_count

# For Azure SQL:
from db_handler import run_query
```

The `run_query(sql)` signature is identical in both — `mainui.py` does not need any changes.

---

[← RAG Deep Dive](./04-rag.md) · [Setup Guide →](./06-setup.md)
