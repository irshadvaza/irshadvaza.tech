# DBA Daily / Weekly / Monthly Checklist

**Why have a checklist?** Most production incidents (disk full, failed backups, runaway logs, blocking) are preventable if caught early. A routine checklist turns "hope it's fine" into a repeatable, auditable process.

## 🗓️ Daily Tasks

| Task | Why |
|---|---|
| Verify last night's backups completed successfully | A silent backup failure is the #1 cause of unrecoverable data loss |
| Check SQL Server Agent job history for failures | Catch broken maintenance/ETL jobs immediately |
| Review error logs (`SQL Server Error Log`, Windows Event Log) | Spot recurring warnings before they become outages |
| Monitor disk space on data, log, and backup drives | Prevent "database out of space" outages |
| Check for long-running or blocked sessions | Identify blocking chains impacting users |
| Confirm replication/mirroring/Always On sync status | Ensure HA/DR is actually protecting you |
| Review overnight alert emails (deadlocks, severity 16+ errors) | Triage anything that needs immediate action |

```sql
-- Quick daily backup check
SELECT database_name, MAX(backup_finish_date) AS LastBackup, type
FROM msdb.dbo.backupset
GROUP BY database_name, type
ORDER BY database_name;
```

## 📆 Weekly Tasks

| Task | Why |
|---|---|
| Review index fragmentation and rebuild/reorganize as needed | Keep query performance consistent |
| Update outdated statistics | Prevent the optimizer from choosing bad execution plans |
| Run `DBCC CHECKDB` on all production databases | Catch corruption early, while recovery options are still good |
| Review slow query / top resource-consuming query reports | Proactively tune before users complain |
| Check TempDB size and configuration | TempDB contention is a common hidden bottleneck |
| Review security: new logins, permission changes, orphaned users | Close security gaps early |
| Validate a test restore of at least one backup | Confirms backups are actually usable |

## 🗓️ Monthly Tasks

| Task | Why |
|---|---|
| Review overall capacity trends (storage, CPU, memory growth) | Plan hardware/cloud scaling ahead of time |
| Patch review — check for new Cumulative Updates / Service Packs | Stay current on security and stability fixes |
| Audit login/role assignments against a "least privilege" baseline | Reduce security exposure |
| Review and archive/purge old data per retention policy | Control database growth and backup times |
| Test full disaster recovery run-book (not just a single restore) | Confidence that DR actually works end-to-end |
| Review SLA/RPO/RTO targets against actual backup/restore times | Ensure business expectations are realistic |

## A Simple Health-Check Script

```sql
-- Disk space per database file
SELECT
    DB_NAME(database_id) AS DatabaseName,
    name AS LogicalFileName,
    type_desc,
    size / 128.0 AS CurrentSizeMB,
    FILEPROPERTY(name, 'SpaceUsed') / 128.0 AS UsedSpaceMB
FROM sys.master_files
WHERE database_id > 4;   -- skip system DBs

-- Long-running queries right now
SELECT r.session_id, r.status, r.command, r.wait_type,
       r.total_elapsed_time / 1000 AS ElapsedSeconds, t.text
FROM sys.dm_exec_requests r
CROSS APPLY sys.dm_exec_sql_text(r.sql_handle) t
WHERE r.session_id > 50
ORDER BY r.total_elapsed_time DESC;
```

---
[⬅ Back to Administration](./README.md) | [⬅ Back to Database Home](../../README.md)
