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
        self.contest_title = 'Spring Programming Contest'
        self.owner_uid = 1
    
    def test_generate_username(self):
        """Test username generation from contest title and display name."""
        username = contest_temp_user.generate_username('Spring Programming Contest', 'John Doe')
        self.assertEqual(username, 'spc_john_doe')
        
        # Test with special characters
        username = contest_temp_user.generate_username('Test Contest', 'Alice O\'Brien')
        self.assertEqual(username, 'tc_alice_o_brien')
        
        # Test with numbers
        username = contest_temp_user.generate_username('Contest 2024', 'User123')
        self.assertEqual(username, 'c_user123')
    
    def test_generate_email(self):
        """Test email generation from username."""
        email = contest_temp_user.generate_email('spc_john_doe')
        self.assertEqual(email, 'spc_john_doe@serious-oj.com')
    
    def test_add_temp_user(self):
        """Test adding a temp user with auto-generated username and password."""
        temp_user_id = wait(contest_temp_user.add(
            self.domain_id, self.tid, self.contest_title, 'John Doe', self.owner_uid
        ))
        self.assertIsInstance(temp_user_id, objectid.ObjectId)
        
        # Verify the user was added with generated fields
        temp_user = wait(contest_temp_user.get(self.domain_id, self.tid, temp_user_id))
        self.assertIsNotNone(temp_user)
        self.assertEqual(temp_user['display_name'], 'John Doe')
        self.assertEqual(temp_user['uname'], 'spc_john_doe')
        self.assertEqual(temp_user['email'], 'spc_john_doe@serious-oj.com')
        self.assertIn('password', temp_user)
        self.assertTrue(len(temp_user['password']) > 0)
        self.assertFalse(temp_user.get('synced', False))
    
    def test_edit_temp_user(self):
        """Test editing a temp user's display name."""
        temp_user_id = wait(contest_temp_user.add(
            self.domain_id, self.tid, self.contest_title, 'John Doe', self.owner_uid
        ))
        
        # Edit the display name
        wait(contest_temp_user.edit(
            self.domain_id, self.tid, temp_user_id, display_name='Jane Smith'
        ))
        
        # Verify the edit
        temp_user = wait(contest_temp_user.get(self.domain_id, self.tid, temp_user_id))
        self.assertEqual(temp_user['display_name'], 'Jane Smith')
        # Username should remain unchanged
        self.assertEqual(temp_user['uname'], 'spc_john_doe')
    
    def test_regenerate_password(self):
        """Test regenerating password for a temp user."""
        temp_user_id = wait(contest_temp_user.add(
            self.domain_id, self.tid, self.contest_title, 'John Doe', self.owner_uid
        ))
        
        # Get original password
        temp_user = wait(contest_temp_user.get(self.domain_id, self.tid, temp_user_id))
        original_password = temp_user['password']
        
        # Regenerate password
        new_password = wait(contest_temp_user.regenerate_password(
            self.domain_id, self.tid, temp_user_id
        ))
        
        # Verify password changed
        self.assertNotEqual(new_password, original_password)
        temp_user = wait(contest_temp_user.get(self.domain_id, self.tid, temp_user_id))
        self.assertEqual(temp_user['password'], new_password)
    
    def test_delete_temp_user(self):
        """Test deleting a temp user."""
        temp_user_id = wait(contest_temp_user.add(
            self.domain_id, self.tid, self.contest_title, 'John Doe', self.owner_uid
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
        wait(contest_temp_user.add(self.domain_id, self.tid, self.contest_title, 'User 1', self.owner_uid))
        wait(contest_temp_user.add(self.domain_id, self.tid, self.contest_title, 'User 2', self.owner_uid))
        wait(contest_temp_user.add(self.domain_id, self.tid, self.contest_title, 'User 3', self.owner_uid))
        
        # Get all temp users
        temp_users = []
        async def collect_users():
            async for temp_user in contest_temp_user.get_multi(self.domain_id, self.tid):
                temp_users.append(temp_user)
        
        wait(collect_users())
        
        self.assertEqual(len(temp_users), 3)
        display_names = [tu['display_name'] for tu in temp_users]
        self.assertIn('User 1', display_names)
        self.assertIn('User 2', display_names)
        self.assertIn('User 3', display_names)
    
    def test_import_from_csv(self):
        """Test importing temp users from CSV."""
        csv_content = """display_name
John Doe
Jane Smith
Alice Johnson"""
        
        imported_count, errors = wait(contest_temp_user.import_from_csv(
            self.domain_id, self.tid, self.contest_title, csv_content, self.owner_uid
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
        # Verify each has generated username, email, and password
        for temp_user in temp_users:
            self.assertIn('uname', temp_user)
            self.assertIn('email', temp_user)
            self.assertIn('password', temp_user)
            self.assertTrue('@serious-oj.com' in temp_user['email'])
    
    def test_export_to_csv(self):
        """Test exporting temp users to CSV with passwords."""
        # Add some temp users
        wait(contest_temp_user.add(self.domain_id, self.tid, self.contest_title, 'User 1', self.owner_uid))
        wait(contest_temp_user.add(self.domain_id, self.tid, self.contest_title, 'User 2', self.owner_uid))
        
        # Export to CSV
        csv_content = wait(contest_temp_user.export_to_csv(self.domain_id, self.tid))
        
        self.assertIsInstance(csv_content, str)
        # Check headers
        self.assertIn('display_name', csv_content)
        self.assertIn('username', csv_content)
        self.assertIn('email', csv_content)
        self.assertIn('password', csv_content)
        # Check data
        self.assertIn('User 1', csv_content)
        self.assertIn('User 2', csv_content)
        self.assertIn('@serious-oj.com', csv_content)
    
    def test_password_generation(self):
        """Test password generation."""
        password = contest_temp_user.generate_password()
        self.assertIsInstance(password, str)
        self.assertEqual(len(password), 8)
        
        # Test custom length
        password = contest_temp_user.generate_password(12)
        self.assertEqual(len(password), 12)


if __name__ == '__main__':
    unittest.main()
