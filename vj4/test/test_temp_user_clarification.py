"""Test that temp users can use the clarification system.

This test validates permission constants directly to ensure temp users
have the necessary clarification permissions without requiring full
database setup.
"""
import unittest


class TempUserClarificationPermissionsTest(unittest.TestCase):
    """Test that temp users have the necessary permissions for clarifications."""
    
    @classmethod
    def setUpClass(cls):
        """Import builtin module once for all tests."""
        # Import here to avoid issues when test discovery runs
        try:
            from vj4.model import builtin
            cls.builtin = builtin
        except ImportError:
            cls.builtin = None
    
    def setUp(self):
        """Skip tests if builtin module can't be imported."""
        if self.builtin is None:
            self.skipTest("Cannot import vj4.model.builtin - dependencies not available")
    
    def test_temp_user_has_view_clarification_permission(self):
        """Verify temp users can view clarifications."""
        self.assertTrue(
            self.builtin.TEMP_USER_PERMISSIONS & self.builtin.PERM_VIEW_CLARIFICATION,
            "TEMP_USER_PERMISSIONS should include PERM_VIEW_CLARIFICATION"
        )
    
    def test_temp_user_has_create_clarification_permission(self):
        """Verify temp users can create clarification questions."""
        self.assertTrue(
            self.builtin.TEMP_USER_PERMISSIONS & self.builtin.PERM_CREATE_CLARIFICATION,
            "TEMP_USER_PERMISSIONS should include PERM_CREATE_CLARIFICATION"
        )
    
    def test_temp_user_has_edit_own_clarification_permission(self):
        """Verify temp users can edit their own clarification questions."""
        self.assertTrue(
            self.builtin.TEMP_USER_PERMISSIONS & self.builtin.PERM_EDIT_CLARIFICATION_SELF,
            "TEMP_USER_PERMISSIONS should include PERM_EDIT_CLARIFICATION_SELF"
        )
    
    def test_temp_user_has_delete_own_clarification_permission(self):
        """Verify temp users can delete their own clarification questions."""
        self.assertTrue(
            self.builtin.TEMP_USER_PERMISSIONS & self.builtin.PERM_DELETE_CLARIFICATION_SELF,
            "TEMP_USER_PERMISSIONS should include PERM_DELETE_CLARIFICATION_SELF"
        )
    
    def test_temp_user_does_not_have_answer_clarification_permission(self):
        """Verify temp users cannot answer clarification questions (moderator-only)."""
        self.assertFalse(
            self.builtin.TEMP_USER_PERMISSIONS & self.builtin.PERM_ANSWER_CLARIFICATION,
            "TEMP_USER_PERMISSIONS should NOT include PERM_ANSWER_CLARIFICATION"
        )
    
    def test_temp_user_does_not_have_edit_any_clarification_permission(self):
        """Verify temp users cannot edit other users' clarification questions."""
        self.assertFalse(
            self.builtin.TEMP_USER_PERMISSIONS & self.builtin.PERM_EDIT_CLARIFICATION,
            "TEMP_USER_PERMISSIONS should NOT include PERM_EDIT_CLARIFICATION"
        )
    
    def test_temp_user_does_not_have_delete_any_clarification_permission(self):
        """Verify temp users cannot delete other users' clarification questions."""
        self.assertFalse(
            self.builtin.TEMP_USER_PERMISSIONS & self.builtin.PERM_DELETE_CLARIFICATION,
            "TEMP_USER_PERMISSIONS should NOT include PERM_DELETE_CLARIFICATION"
        )
    
    def test_temp_user_has_basic_contest_permissions(self):
        """Verify temp users still have basic contest permissions."""
        # View contest
        self.assertTrue(
            self.builtin.TEMP_USER_PERMISSIONS & self.builtin.PERM_VIEW_CONTEST,
            "TEMP_USER_PERMISSIONS should include PERM_VIEW_CONTEST"
        )
        # Submit to contest
        self.assertTrue(
            self.builtin.TEMP_USER_PERMISSIONS & self.builtin.PERM_SUBMIT_PROBLEM_CONTEST,
            "TEMP_USER_PERMISSIONS should include PERM_SUBMIT_PROBLEM_CONTEST"
        )
        # View scoreboard
        self.assertTrue(
            self.builtin.TEMP_USER_PERMISSIONS & self.builtin.PERM_VIEW_CONTEST_SCOREBOARD,
            "TEMP_USER_PERMISSIONS should include PERM_VIEW_CONTEST_SCOREBOARD"
        )


if __name__ == '__main__':
    unittest.main()
