"""Contest temp user management model."""
import csv
import io
import secrets
import string
from bson import objectid
from pymongo import ReturnDocument

from vj4 import db
from vj4 import error
from vj4.model import user
from vj4.model import document
from vj4.util import argmethod


def generate_password(length=8):
    """Generate a random password."""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))


@argmethod.wrap
async def add(domain_id: str, tid: objectid.ObjectId, uname: str, display_name: str = '', owner_uid: int = None):
    """Add a temp user for a contest."""
    coll = db.coll('contest.temp_user')
    temp_user_id = objectid.ObjectId()
    
    doc = {
        '_id': temp_user_id,
        'domain_id': domain_id,
        'tid': tid,
        'uname': uname,
        'display_name': display_name or uname,
        'synced': False,
        'synced_uid': None,
        'created_by': owner_uid,
    }
    
    await coll.insert_one(doc)
    return temp_user_id


@argmethod.wrap
async def get(domain_id: str, tid: objectid.ObjectId, temp_user_id: objectid.ObjectId):
    """Get a temp user by ID."""
    coll = db.coll('contest.temp_user')
    return await coll.find_one({'_id': temp_user_id, 'domain_id': domain_id, 'tid': tid})


@argmethod.wrap
async def edit(domain_id: str, tid: objectid.ObjectId, temp_user_id: objectid.ObjectId, **kwargs):
    """Edit a temp user."""
    coll = db.coll('contest.temp_user')
    doc = await coll.find_one_and_update(
        filter={'_id': temp_user_id, 'domain_id': domain_id, 'tid': tid},
        update={'$set': kwargs},
        return_document=ReturnDocument.AFTER
    )
    return doc


@argmethod.wrap
async def delete(domain_id: str, tid: objectid.ObjectId, temp_user_id: objectid.ObjectId):
    """Delete a temp user."""
    coll = db.coll('contest.temp_user')
    result = await coll.delete_one({'_id': temp_user_id, 'domain_id': domain_id, 'tid': tid})
    return result.deleted_count > 0


def get_multi(domain_id: str, tid: objectid.ObjectId):
    """Get multiple temp users for a contest."""
    coll = db.coll('contest.temp_user')
    return coll.find({'domain_id': domain_id, 'tid': tid})


@argmethod.wrap
async def sync_to_real_user(domain_id: str, tid: objectid.ObjectId, temp_user_id: objectid.ObjectId, 
                           uid: int, mail: str, regip: str = ''):
    """Sync a temp user to the real user table and generate password."""
    temp_user_doc = await get(domain_id, tid, temp_user_id)
    if not temp_user_doc:
        raise error.DocumentNotFoundError(domain_id, document.TYPE_CONTEST, temp_user_id)
    
    if temp_user_doc.get('synced', False):
        raise error.ValidationError('temp_user', 'Already synced')
    
    # Generate a random password
    password = generate_password()
    
    # Add the user to the real user table
    await user.add(uid, temp_user_doc['uname'], password, mail, regip)
    
    # Mark as synced
    await edit(domain_id, tid, temp_user_id, synced=True, synced_uid=uid, synced_password=password)
    
    return password


@argmethod.wrap
async def import_from_csv(domain_id: str, tid: objectid.ObjectId, csv_content: str, owner_uid: int):
    """Import temp users from CSV content.
    
    CSV format: uname,display_name (optional)
    """
    reader = csv.DictReader(io.StringIO(csv_content))
    imported_count = 0
    errors = []
    
    for row_num, row in enumerate(reader, start=2):  # Start from 2 (1 is header)
        uname = row.get('uname', '').strip()
        display_name = row.get('display_name', '').strip()
        
        if not uname:
            errors.append(f"Row {row_num}: Missing username")
            continue
        
        try:
            await add(domain_id, tid, uname, display_name, owner_uid)
            imported_count += 1
        except Exception as e:
            errors.append(f"Row {row_num} ({uname}): {str(e)}")
    
    return imported_count, errors


@argmethod.wrap
async def export_to_csv(domain_id: str, tid: objectid.ObjectId, include_password: bool = False):
    """Export temp users to CSV content."""
    output = io.StringIO()
    
    if include_password:
        fieldnames = ['uname', 'display_name', 'synced', 'synced_uid', 'password']
    else:
        fieldnames = ['uname', 'display_name', 'synced', 'synced_uid']
    
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    
    async for temp_user in get_multi(domain_id, tid):
        row = {
            'uname': temp_user.get('uname', ''),
            'display_name': temp_user.get('display_name', ''),
            'synced': 'Yes' if temp_user.get('synced', False) else 'No',
            'synced_uid': temp_user.get('synced_uid', '') or '',
        }
        
        if include_password:
            row['password'] = temp_user.get('synced_password', '') if temp_user.get('synced', False) else ''
        
        writer.writerow(row)
    
    return output.getvalue()


@argmethod.wrap
async def ensure_indexes():
    """Ensure indexes for contest temp users."""
    coll = db.coll('contest.temp_user')
    await coll.create_index([('domain_id', 1), ('tid', 1)])
    await coll.create_index([('domain_id', 1), ('tid', 1), ('uname', 1)], unique=True)


if __name__ == '__main__':
    argmethod.invoke_by_args()
