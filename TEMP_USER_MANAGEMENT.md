# Temp User Management for Contests

## Overview

This feature allows contest organizers to manage temporary users for a contest. Temp users can be created, edited, and later synced to real user accounts with auto-generated passwords.

## Features

### 1. Create Temp Users
- Add temp users individually through the web UI
- Specify username and optional display name
- Display name defaults to username if not provided

### 2. Edit Display Names
- Update display names inline from the temp user list
- No need to recreate users when display names change

### 3. Sync to Real Users
- Convert temp users to real user accounts
- Automatically generates secure random passwords (8 characters)
- Requires providing User ID (UID) and email address
- Once synced, temp users cannot be deleted or synced again

### 4. CSV Import
- Bulk import temp users from CSV file
- Format: `uname,display_name`
- First row must be header
- Display name is optional

Example CSV:
```csv
uname,display_name
student1,John Doe
student2,Jane Smith
student3,
```

### 5. CSV Export
- Export all temp users to CSV
- Option to include generated passwords for synced users
- Uses UTF-8 with BOM for Excel compatibility

## Usage

### Accessing Temp User Management

1. Navigate to a contest detail page
2. If you have edit permissions, you'll see "Manage Temp Users" in the sidebar
3. Click to access the temp user management page

### Adding Individual Users

1. On the temp user management page, use the "Add New Temp User" form
2. Enter username (required) and display name (optional)
3. Click "Add Temp User"

### Importing from CSV

1. Click "Import from CSV" button
2. Paste or type CSV content following the format
3. Click "Import Temp Users"
4. Review import results and any errors

### Exporting Users

- Click "Export to CSV" to download basic info
- Click "Export with Passwords" to include generated passwords for synced users

### Syncing to Real Users

1. Click "Sync to Real User" button next to a temp user
2. Enter User ID (UID) and email address
3. Click "Sync & Generate Password"
4. Password will be displayed - copy it and provide to the user
5. Temp user status will update to "synced"

## Permissions

- Requires contest ownership or `PERM_EDIT_CONTEST` permission
- All operations are protected with CSRF tokens
- Only contest owners/editors can access temp user management

## Database Schema

Temp users are stored in the `contest.temp_user` collection:

```python
{
    '_id': ObjectId,
    'domain_id': str,
    'tid': ObjectId,  # Contest ID
    'uname': str,
    'display_name': str,
    'synced': bool,
    'synced_uid': int,  # Only set when synced
    'synced_password': str,  # Only set when synced
    'created_by': int  # UID of creator
}
```

## API Endpoints

- `GET /contest/{tid}/tempuser` - List temp users
- `POST /contest/{tid}/tempuser?operation=add` - Add temp user
- `POST /contest/{tid}/tempuser?operation=edit` - Edit temp user
- `POST /contest/{tid}/tempuser?operation=delete` - Delete temp user
- `POST /contest/{tid}/tempuser?operation=sync` - Sync to real user
- `GET /contest/{tid}/tempuser/import` - Import form
- `POST /contest/{tid}/tempuser/import` - Process import
- `GET /contest/{tid}/tempuser/export` - Export to CSV
- `GET /contest/{tid}/tempuser/export?include_password=true` - Export with passwords

## Security

- ✅ CodeQL security scan: 0 vulnerabilities
- ✅ CSRF protection on all POST operations
- ✅ Permission checks enforce authorization
- ✅ Secure password generation using `secrets` module
- ✅ Input validation on all user data
- ✅ Prevents duplicate syncing

## Testing

Unit tests are available in `vj4/test/test_contest_temp_user.py`:

```bash
python -m unittest vj4.test.test_contest_temp_user
```

Tests cover:
- Adding temp users
- Editing temp users
- Deleting temp users
- Getting multiple temp users
- CSV import/export
- Password generation
