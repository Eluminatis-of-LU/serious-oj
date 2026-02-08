import unittest
from bson import objectid

from vj4.model import contest_temp_user
from vj4.test import base

wait = base.wait


class ContestTempUserTest(base.DatabaseTestCase):
    
    def setUp(self):
        super().setUp()
        self.domain_id = 'test_domain'
        self.tid = objectid.ObjectId()
        self.owner_uid = 1
    
    def test_add_temp_user(self):
        """Test adding a temp user."""
        temp_user_id = wait(contest_temp_user.add(
            self.domain_id, self.tid, 'testuser', 'Test User', self.owner_uid
        ))
        self.assertIsInstance(temp_user_id, objectid.ObjectId)
        
        # Verify the user was added
        temp_user = wait(contest_temp_user.get(self.domain_id, self.tid, temp_user_id))
        self.assertIsNotNone(temp_user)
        self.assertEqual(temp_user['uname'], 'testuser')
        self.assertEqual(temp_user['display_name'], 'Test User')
        self.assertFalse(temp_user.get('synced', False))
    
    def test_edit_temp_user(self):
        """Test editing a temp user."""
        temp_user_id = wait(contest_temp_user.add(
            self.domain_id, self.tid, 'testuser', 'Test User', self.owner_uid
        ))
        
        # Edit the display name
        wait(contest_temp_user.edit(
            self.domain_id, self.tid, temp_user_id, display_name='New Display Name'
        ))
        
        # Verify the edit
        temp_user = wait(contest_temp_user.get(self.domain_id, self.tid, temp_user_id))
        self.assertEqual(temp_user['display_name'], 'New Display Name')
    
    def test_delete_temp_user(self):
        """Test deleting a temp user."""
        temp_user_id = wait(contest_temp_user.add(
            self.domain_id, self.tid, 'testuser', 'Test User', self.owner_uid
        ))
        
        # Delete the user
        deleted = wait(contest_temp_user.delete(self.domain_id, self.tid, temp_user_id))
        self.assertTrue(deleted)
        
        # Verify deletion
        temp_user = wait(contest_temp_user.get(self.domain_id, self.tid, temp_user_id))
        self.assertIsNone(temp_user)
    
    def test_get_multi(self):
        """Test getting multiple temp users."""
        # Add multiple temp users
        wait(contest_temp_user.add(self.domain_id, self.tid, 'user1', 'User 1', self.owner_uid))
        wait(contest_temp_user.add(self.domain_id, self.tid, 'user2', 'User 2', self.owner_uid))
        wait(contest_temp_user.add(self.domain_id, self.tid, 'user3', 'User 3', self.owner_uid))
        
        # Get all temp users
        temp_users = []
        async def collect_users():
            async for temp_user in contest_temp_user.get_multi(self.domain_id, self.tid):
                temp_users.append(temp_user)
        
        wait(collect_users())
        
        self.assertEqual(len(temp_users), 3)
        usernames = [tu['uname'] for tu in temp_users]
        self.assertIn('user1', usernames)
        self.assertIn('user2', usernames)
        self.assertIn('user3', usernames)
    
    def test_import_from_csv(self):
        """Test importing temp users from CSV."""
        csv_content = """uname,display_name
user1,Display Name 1
user2,Display Name 2
user3,"""
        
        imported_count, errors = wait(contest_temp_user.import_from_csv(
            self.domain_id, self.tid, csv_content, self.owner_uid
        ))
        
        self.assertEqual(imported_count, 3)
        self.assertEqual(len(errors), 0)
        
        # Verify the imported users
        temp_users = []
        async def collect_users():
            async for temp_user in contest_temp_user.get_multi(self.domain_id, self.tid):
                temp_users.append(temp_user)
        
        wait(collect_users())
        
        self.assertEqual(len(temp_users), 3)
    
    def test_export_to_csv(self):
        """Test exporting temp users to CSV."""
        # Add some temp users
        wait(contest_temp_user.add(self.domain_id, self.tid, 'user1', 'User 1', self.owner_uid))
        wait(contest_temp_user.add(self.domain_id, self.tid, 'user2', 'User 2', self.owner_uid))
        
        # Export to CSV
        csv_content = wait(contest_temp_user.export_to_csv(self.domain_id, self.tid, False))
        
        self.assertIsInstance(csv_content, str)
        self.assertIn('uname', csv_content)
        self.assertIn('display_name', csv_content)
        self.assertIn('user1', csv_content)
        self.assertIn('user2', csv_content)
    
    def test_generate_password(self):
        """Test password generation."""
        password = contest_temp_user.generate_password()
        self.assertIsInstance(password, str)
        self.assertEqual(len(password), 8)
        
        # Test custom length
        password = contest_temp_user.generate_password(12)
        self.assertEqual(len(password), 12)


if __name__ == '__main__':
    unittest.main()
