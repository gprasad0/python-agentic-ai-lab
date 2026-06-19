## Inserting a Proposal into SQLite

The following code inserts a new proposal record into the `proposals` table.

```python
cursor.execute(
    """
    INSERT INTO proposals
    (
        prospect_name,
        company_name,
        prospect_url,
        status
    )
    VALUES (?, ?, ?, ?)
    """,
    (
        prospect_name,
        company_name,
        prospect_url,
        "CREATED",
    ),
)
```

### How It Works

#### 1. INSERT INTO

```sql
INSERT INTO proposals
```

Specifies that a new row should be added to the `proposals` table.

#### 2. Column List

```sql
(
    prospect_name,
    company_name,
    prospect_url,
    status
)
```

Defines which columns will receive values.

#### 3. Parameter Placeholders

```sql
VALUES (?, ?, ?, ?)
```

The `?` symbols are parameter placeholders used by SQLite.

Using placeholders:

- Prevents SQL injection attacks
- Separates SQL logic from user data
- Allows SQLite to safely escape values

#### 4. Parameter Values

```python
(
    prospect_name,
    company_name,
    prospect_url,
    "CREATED",
)
```

These values are mapped to the placeholders in order:

| Placeholder | Value         |
| ----------- | ------------- |
| 1st `?`     | prospect_name |
| 2nd `?`     | company_name  |
| 3rd `?`     | prospect_url  |
| 4th `?`     | CREATED       |

Example:

```python
prospect_name = "John Doe"
company_name = "Acme Corp"
prospect_url = "https://acme.com"
```

Results in:

```sql
INSERT INTO proposals
(
    prospect_name,
    company_name,
    prospect_url,
    status
)
VALUES
(
    'John Doe',
    'Acme Corp',
    'https://acme.com',
    'CREATED'
)
```

#### 5. Commit Changes

After executing the insert, the transaction must be committed:

```python
conn.commit()
```

This persists the new record to the SQLite database.

#### 6. Retrieve Generated ID

```python
proposal_id = cursor.lastrowid
```

Returns the auto-generated primary key of the newly inserted proposal.

Example:

```python
proposal_id = 1
```

#### 7. Close Connection

```python
conn.close()
```

Releases the database connection and associated resources.

### Complete Flow

```text
Open Database Connection
        ↓
Create Cursor
        ↓
Execute INSERT Statement
        ↓
Generate Proposal ID
        ↓
Commit Transaction
        ↓
Close Connection
        ↓
Return Proposal ID
```
