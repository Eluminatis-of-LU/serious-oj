"""Contest temp user management model."""
import csv
import io
import re
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


def make_slug(text):
    """Convert text to email-safe slug."""
    # Convert to lowercase and remove special characters
    text = text.lower()
    # Replace spaces and special chars with underscore
    text = re.sub(r'[^a-z0-9]+', '_', text)
    # Remove leading/trailing underscores
    text = text.strip('_')
    # Collapse multiple underscores
    text = re.sub(r'_+', '_', text)
    return text


def generate_username(contest_title, display_name):
    """Generate username from contest title acronym and display name.
    
    Format: slug(contest_title_acronym) + slug(display_name)
    """
    # Get acronym from contest title (first letter of each word)
    words = contest_title.split()
    acronym = ''.join(word[0] for word in words if word).lower()
    
    # Make email-safe slugs
    acronym_slug = make_slug(acronym)
    name_slug = make_slug(display_name)
    
    # Combine with underscore
    username = f"{acronym_slug}_{name_slug}"
    
    return username


def generate_email(username):
    """Generate email from username."""
    return f"{username}@serious-oj.com"


@argmethod.wrap
async def add(domain_id: str, tid: objectid.ObjectId, contest_title: str, display_name: str, owner_uid: int = None):
    """Add a temp user for a contest with auto-generated username, email, and password."""
    coll = db.coll('contest.temp_user')
    temp_user_id = objectid.ObjectId()
    
    # Generate username from contest title and display name
    uname = generate_username(contest_title, display_name)
    
    # Generate email
    email = generate_email(uname)
    
    # Generate password immediately
    password = generate_password()
    
    doc = {
        '_id': temp_user_id,
        'domain_id': domain_id,
        'tid': tid,
        'uname': uname,
        'display_name': display_name,
        'email': email,
        'password': password,
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


def get_multi(domain_id: str, tid: objectid.ObjectId, skip: int = 0, limit: int = 50):
    """Get multiple temp users for a contest with pagination."""
    coll = db.coll('contest.temp_user')
    return coll.find({'domain_id': domain_id, 'tid': tid}).skip(skip).limit(limit)


@argmethod.wrap
async def get_count(domain_id: str, tid: objectid.ObjectId):
    """Get count of temp users for a contest."""
    coll = db.coll('contest.temp_user')
    return await coll.find({'domain_id': domain_id, 'tid': tid}).count()


@argmethod.wrap
async def regenerate_password(domain_id: str, tid: objectid.ObjectId, temp_user_id: objectid.ObjectId):
    """Regenerate password for a temp user."""
    password = generate_password()
    await edit(domain_id, tid, temp_user_id, password=password)
    return password


@argmethod.wrap
async def sync_all_to_real_users(domain_id: str, tid: objectid.ObjectId, regip: str = ''):
    """Sync all unsynced temp users to real user table.
    
    For each temp user:
    - If synced_uid exists, update existing user with temp_user=True
    - Else create new user with temp_user=True and store uid back
    - Mark user as contest attendee
    """
    from vj4.model.adaptor import contest as contest_model
    
    results = []
    errors = []
    
    async for temp_user_doc in get_multi(domain_id, tid):
        if temp_user_doc.get('synced', False):
            continue  # Skip already synced users
        
        try:
            temp_user_id = temp_user_doc['_id']
            uname = temp_user_doc.get('uname')
            email = temp_user_doc.get('email')
            password = temp_user_doc.get('password')
            synced_uid = temp_user_doc.get('synced_uid')
            
            if not password or not email or not uname:
                errors.append(f"{temp_user_doc.get('display_name', 'Unknown')}: Missing credentials")
                continue
            
            # Check if user should be updated or created
            if synced_uid:
                # Update existing user
                try:
                    udoc = await user.get_by_uid(synced_uid)
                    if udoc:
                        # Mark as temp user
                        await user.set_by_uid(synced_uid, temp_user=True)
                        uid = synced_uid
                    else:
                        # UID doesn't exist, create new user
                        uid = await user.add(uname, password, email, regip)
                        await user.set_by_uid(uid, temp_user=True)
                except Exception as e:
                    errors.append(f"{temp_user_doc.get('display_name', uname)}: {str(e)}")
                    continue
            else:
                # Create new user
                try:
                    uid = await user.add(uname, password, email, regip)
                    await user.set_by_uid(uid, temp_user=True)
                except Exception as e:
                    errors.append(f"{temp_user_doc.get('display_name', uname)}: {str(e)}")
                    continue
            
            # Mark as synced in temp_user table
            await edit(domain_id, tid, temp_user_id, synced=True, synced_uid=uid)
            
            # Add as contest attendee
            try:
                await contest_model.attend(domain_id, document.TYPE_CONTEST, tid, uid)
            except error.ContestAlreadyAttendedError:
                pass  # Already attended, that's fine
            
            results.append({
                'temp_user_id': temp_user_id,
                'uid': uid,
                'uname': uname,
                'display_name': temp_user_doc.get('display_name', '')
            })
            
        except Exception as e:
            errors.append(f"{temp_user_doc.get('display_name', 'Unknown')}: {str(e)}")
    
    return results, errors


@argmethod.wrap
async def delete_with_user(domain_id: str, tid: objectid.ObjectId, temp_user_id: objectid.ObjectId):
    """Delete temp user and associated real user and attendance if synced."""
    # Get temp user info
    temp_user_doc = await get(domain_id, tid, temp_user_id)
    if not temp_user_doc:
        return False
    
    synced_uid = temp_user_doc.get('synced_uid')
    
    # Delete from temp_user table
    await delete(domain_id, tid, temp_user_id)
    
    # If synced, delete user and attendance
    if synced_uid and temp_user_doc.get('synced', False):
        try:
            # Delete attendance (status document)
            coll = db.coll('document.status')
            await coll.delete_one({
                'domain_id': domain_id,
                'doc_type': document.TYPE_CONTEST,
                'doc_id': tid,
                'uid': synced_uid
            })
        except:
            pass  # Status might not exist
        
        try:
            # Delete user - mark as deleted or remove (depending on system design)
            # For safety, we'll just mark the user as temp_user=False
            await user.set_by_uid(synced_uid, temp_user=False)
        except:
            pass  # User might not exist
    
    return True


@argmethod.wrap
async def sync_to_real_user(domain_id: str, tid: objectid.ObjectId, temp_user_id: objectid.ObjectId, 
                           uid: int, regip: str = ''):
    """Sync a temp user to the real user table using already generated password and email."""
    temp_user_doc = await get(domain_id, tid, temp_user_id)
    if not temp_user_doc:
        raise error.DocumentNotFoundError(domain_id, document.TYPE_CONTEST, temp_user_id)
    
    if temp_user_doc.get('synced', False):
        raise error.ValidationError('temp_user', 'Already synced')
    
    # Use the already generated password and email
    password = temp_user_doc.get('password')
    email = temp_user_doc.get('email')
    uname = temp_user_doc.get('uname')
    
    if not password or not email:
        raise error.ValidationError('temp_user', 'Missing password or email')
    
    # Add the user to the real user table
    await user.add(uid, uname, password, email, regip)
    
    # Mark as synced
    await edit(domain_id, tid, temp_user_id, synced=True, synced_uid=uid)
    
    return password


@argmethod.wrap
async def import_from_csv(domain_id: str, tid: objectid.ObjectId, contest_title: str, csv_content: str, owner_uid: int):
    """Import temp users from CSV content.
    
    CSV format: display_name (required)
    """
    reader = csv.DictReader(io.StringIO(csv_content))
    imported_count = 0
    errors = []
    
    for row_num, row in enumerate(reader, start=2):  # Start from 2 (1 is header)
        display_name = row.get('display_name', '').strip()
        
        if not display_name:
            errors.append(f"Row {row_num}: Missing display name")
            continue
        
        try:
            await add(domain_id, tid, contest_title, display_name, owner_uid)
            imported_count += 1
        except Exception as e:
            errors.append(f"Row {row_num} ({display_name}): {str(e)}")
    
    return imported_count, errors


@argmethod.wrap
async def export_to_csv(domain_id: str, tid: objectid.ObjectId):
    """Export temp users to CSV content with passwords."""
    output = io.StringIO()
    
    fieldnames = ['display_name', 'username', 'email', 'password', 'synced', 'synced_uid']
    
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    
    async for temp_user in get_multi(domain_id, tid):
        row = {
            'display_name': temp_user.get('display_name', ''),
            'username': temp_user.get('uname', ''),
            'email': temp_user.get('email', ''),
            'password': temp_user.get('password', ''),
            'synced': 'Yes' if temp_user.get('synced', False) else 'No',
            'synced_uid': temp_user.get('synced_uid', '') or '',
        }
        
        writer.writerow(row)
    
    return output.getvalue()


@argmethod.wrap
async def ensure_indexes():
    """Ensure indexes for contest temp users."""
    coll = db.coll('contest.temp_user')
    await coll.create_index([('domain_id', 1), ('tid', 1)])
    await coll.create_index([('domain_id', 1), ('tid', 1), ('uname', 1)], unique=True)
