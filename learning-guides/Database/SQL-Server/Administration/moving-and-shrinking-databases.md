# Moving Database Files & Shrinking Databases

## Moving Database Files

**Why you'd need this:** running out of disk space, migrating to faster storage, or separating data/log files onto different drives for performance and safety.

### Option 1: Detach / Attach

```sql
-- 1. Detach
USE master;
GO
EXEC sp_detach_db 'MyDatabase';
GO

-- 2. Manually move the .mdf and .ldf files to the new location (OS-level copy/move)

-- 3. Attach from the new location
USE master;
GO
EXEC sp_attach_db 'MyDatabase',
    'D:\NewLocation\MyDatabase.mdf',
    'D:\NewLocation\MyDatabase_log.ldf';
GO
```
⚠️ Take a full backup before detaching. The database is **offline** for the duration of the move.

### Option 2: SQL Server Management Studio
1. Right-click the database → **Tasks → Detach**.
2. Copy the `.mdf`/`.ldf` files to the new location.
3. Right-click **Databases → Attach**, browse to the new location, click **OK**.

### Option 3: `ALTER DATABASE ... MODIFY FILE` (no detach needed)

```sql
ALTER DATABASE MyDatabase MODIFY FILE (
    NAME = 'MyDatabase_Data',
    FILENAME = 'D:\NewLocation\MyDatabase.mdf'
);

ALTER DATABASE MyDatabase MODIFY FILE (
    NAME = 'MyDatabase_Log',
    FILENAME = 'D:\NewLocation\MyDatabase_log.ldf'
);

-- Take the database offline, physically move the files at the OS level, then bring it back online
ALTER DATABASE MyDatabase SET OFFLINE;
-- (move files here)
ALTER DATABASE MyDatabase SET ONLINE;
```

### Option 4: `RESTORE ... WITH MOVE`

```sql
RESTORE DATABASE MyDatabase
FROM DISK = 'C:\Backups\MyDatabase.bak'
WITH MOVE 'MyDatabase_Data' TO 'G:\SQLData\MyDatabase.mdf',
     MOVE 'MyDatabase_Log'  TO 'H:\SQLLog\MyDatabase_log.ldf',
     REPLACE;
```
Useful when restoring a copy of production to a server with a different drive layout.

---

## Shrinking a Database

**What it does:** reclaims unused space inside data/log files and returns it to the OS.

**Why be careful:** shrinking is generally considered a **last resort**, not routine maintenance. It:
- Causes significant **index fragmentation** (pages are physically reorganized).
- Is I/O intensive and can affect performance while running.
- Often gets undone quickly if the database just grows back to the same size (wasted effort + more fragmentation).

```sql
-- Shrink the whole database (reclaim free space in all files)
DBCC SHRINKDATABASE (MyDatabase, 10);  -- leave 10% free space

-- Shrink a specific file
DBCC SHRINKFILE (MyDatabase_Log, 2);   -- shrink to 2 MB target
```

### When Shrinking *Is* Appropriate

- After a **one-time** large deletion/archiving operation that permanently frees a lot of space.
- After switching a database to `SIMPLE` recovery temporarily to clear a runaway transaction log (see script below), then restoring the recovery model.

```sql
-- Common pattern: reclaim log space safely
ALTER DATABASE MyDatabase SET RECOVERY SIMPLE;
DBCC SHRINKFILE (MyDatabase_Log, 2);
ALTER DATABASE MyDatabase SET RECOVERY FULL;  -- restore original recovery model
-- ⚠️ Take a fresh full backup immediately after switching back to FULL,
-- since the log chain was broken.
```

> 💡 **Best practice:** instead of shrinking regularly, size your data/log files appropriately up front and let auto-growth handle occasional bursts. Routine shrinking is a symptom of poor capacity planning, not a fix for it.

## Reclaiming Space After Cleanup (Large Deletes)

Deleting millions of rows in one transaction bloats the transaction log. Batch it instead:

```sql
DECLARE @Done BIT = 0;

WHILE (@Done = 0)
BEGIN
    DELETE TOP (10000) FROM ArchiveTable WHERE ArchiveDate < '2024-01-01';

    IF @@ROWCOUNT = 0
        SET @Done = 1;

    CHECKPOINT;  -- helps truncate the log in SIMPLE recovery mode
END
```

---
[⬅ Back to Administration](./README.md) | [⬅ Back to Database Home](../../README.md)
