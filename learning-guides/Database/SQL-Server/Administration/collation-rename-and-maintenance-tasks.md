# Collation, Renaming, and Common Maintenance Tasks

## What is Collation?

**Collation** defines how SQL Server compares, sorts, and stores character data — including case sensitivity, accent sensitivity, and the character set/code page used.

**Why it matters:** mismatched collations between databases (e.g., in a `JOIN` across linked servers) cause the infamous error:
`Cannot resolve the collation conflict between "X" and "Y" in the equal to operation.`

```sql
-- Check current server collation
SELECT SERVERPROPERTY('Collation');

-- Check a database's collation
SELECT name, collation_name FROM sys.databases WHERE name = 'MyDatabase';

-- Change a database's collation
ALTER DATABASE MyDatabase COLLATE SQL_Latin1_General_CP1_CI_AS;
```

**Reading a collation name** — e.g. `SQL_Latin1_General_CP1_CI_AS`:

| Segment | Meaning |
|---|---|
| `Latin1_General` | Character set / language rules |
| `CP1` | Code page 1252 |
| `CI` | Case-**I**nsensitive (`AS` = Accent-Sensitive) |
| `AS` | Accent-**S**ensitive |

> ⚠️ Changing the **server-level** collation requires rebuilding all system databases and is a major operation — always test thoroughly. Changing a single database's collation is much lower risk but still requires care with existing indexes/constraints on string columns.

## Renaming Things

```sql
-- Rename a database
ALTER DATABASE OldName MODIFY NAME = NewName;
-- or the legacy procedure:
EXEC sp_renamedb 'OldName', 'NewName';

-- Rename a table
EXEC sp_rename 'OldTableName', 'NewTableName';

-- Rename a column
EXEC sp_rename 'TableName.OldColumnName', 'NewColumnName', 'COLUMN';
```

## Enabling SQL Server Agent Extended Procedures (Agent XPs)

If **SQL Server Agent** doesn't appear in Object Explorer, or the service won't start, "Agent XPs" may be disabled:

```sql
sp_configure 'show advanced options', 1;
RECONFIGURE;
GO
sp_configure 'Agent XPs', 1;
RECONFIGURE;
GO
```

This takes effect immediately — no restart required. Starting the Agent service through SSMS normally enables this automatically.

## Checking License / Installation Date

```sql
SELECT create_date AS InstallationDate
FROM sys.server_principals
WHERE sid = 0x010100000000000512000000;  -- BUILTIN\Administrators SID
```
A quick, informal way to approximate when SQL Server was first installed on a server (based on when the built-in Administrators login was created).

## Installing Service Packs / Cumulative Updates / Hotfixes

A safe rollout checklist:

1. **Test first** — install on a dev/test instance and verify all applications still work correctly.
2. **Read the release notes/readme** — check for known issues or breaking changes.
3. **Run `DBCC CHECKDB`** on all databases beforehand — never patch a database you suspect might already be corrupt.
4. **Back up all databases** (user and system) — not strictly required, but strongly recommended.
5. **Stop monitoring/antivirus agents** temporarily to avoid file-lock conflicts during install.
6. **Confirm you have administrative privileges** on the server/cluster node.
7. Apply the patch during a maintenance window; validate application connectivity afterward.

---
[⬅ Back to Administration](./README.md) | [⬅ Back to Database Home](../../README.md)
