import collections
import datetime
import functools
import itertools

from vj4 import constant
from vj4.util import version

# Permissions.
PERM_NONE = 0

# Domain settings.
PERM_VIEW = 1 << 0
PERM_EDIT_PERM = 1 << 1
PERM_MOD_BADGE = 1 << 2
PERM_EDIT_DESCRIPTION = 1 << 3

# Problem and Record.
PERM_CREATE_PROBLEM = 1 << 4
PERM_EDIT_PROBLEM = 1 << 5
PERM_EDIT_PROBLEM_SELF = 1 << 6
PERM_VIEW_PROBLEM = 1 << 7
PERM_VIEW_PROBLEM_HIDDEN = 1 << 8
PERM_SUBMIT_PROBLEM = 1 << 9
PERM_READ_PROBLEM_DATA = 1 << 10
PERM_READ_PROBLEM_DATA_SELF = 1 << 11
PERM_READ_RECORD_CODE = 1 << 12
PERM_REJUDGE_PROBLEM = 1 << 13
PERM_REJUDGE = 1 << 14

# Problem Solution.
PERM_VIEW_PROBLEM_SOLUTION = 1 << 15
PERM_CREATE_PROBLEM_SOLUTION = 1 << 16
PERM_VOTE_PROBLEM_SOLUTION = 1 << 17
PERM_EDIT_PROBLEM_SOLUTION = 1 << 18
PERM_EDIT_PROBLEM_SOLUTION_SELF = 1 << 19
PERM_DELETE_PROBLEM_SOLUTION = 1 << 20
PERM_DELETE_PROBLEM_SOLUTION_SELF = 1 << 21
PERM_REPLY_PROBLEM_SOLUTION = 1 << 22
PERM_EDIT_PROBLEM_SOLUTION_REPLY = 1 << 23
PERM_EDIT_PROBLEM_SOLUTION_REPLY_SELF = 1 << 24
PERM_DELETE_PROBLEM_SOLUTION_REPLY = 1 << 25
PERM_DELETE_PROBLEM_SOLUTION_REPLY_SELF = 1 << 26

# Discussion.
PERM_VIEW_DISCUSSION = 1 << 27
PERM_CREATE_DISCUSSION = 1 << 28
PERM_HIGHLIGHT_DISCUSSION = 1 << 29
PERM_EDIT_DISCUSSION = 1 << 30
PERM_EDIT_DISCUSSION_SELF = 1 << 31
PERM_DELETE_DISCUSSION = 1 << 32
PERM_DELETE_DISCUSSION_SELF = 1 << 33
PERM_REPLY_DISCUSSION = 1 << 34
PERM_EDIT_DISCUSSION_REPLY = 1 << 35
PERM_EDIT_DISCUSSION_REPLY_SELF = 1 << 36
PERM_EDIT_DISCUSSION_REPLY_SELF_DISCUSSION = 1 << 37
PERM_DELETE_DISCUSSION_REPLY = 1 << 38
PERM_DELETE_DISCUSSION_REPLY_SELF = 1 << 39
PERM_DELETE_DISCUSSION_REPLY_SELF_DISCUSSION = 1 << 40

# Contest.
PERM_VIEW_CONTEST = 1 << 41
PERM_VIEW_CONTEST_SCOREBOARD = 1 << 42
PERM_VIEW_CONTEST_HIDDEN_SCOREBOARD = 1 << 43
PERM_CREATE_CONTEST = 1 << 44
PERM_ATTEND_CONTEST = 1 << 45
PERM_EDIT_CONTEST = 1 << 50
PERM_EDIT_CONTEST_SELF = 1 << 51
PERM_SUBMIT_PROBLEM_CONTEST = 1 << 61

# Homework.
PERM_VIEW_HOMEWORK = 1 << 52
PERM_VIEW_HOMEWORK_SCOREBOARD = 1 << 53
PERM_VIEW_HOMEWORK_HIDDEN_SCOREBOARD = 1 << 54
PERM_CREATE_HOMEWORK = 1 << 55
PERM_ATTEND_HOMEWORK = 1 << 56
PERM_EDIT_HOMEWORK = 1 << 57
PERM_EDIT_HOMEWORK_SELF = 1 << 58

# Training.
PERM_VIEW_TRAINING = 1 << 46
PERM_CREATE_TRAINING = 1 << 47
PERM_EDIT_TRAINING = 1 << 48
PERM_EDIT_TRAINING_SELF = 1 << 49

# Ranking.
PERM_VIEW_RANKING = 1 << 59

# Rating.
PERM_PROCESS_RATING = 1 << 60

PERM_ALL = -1

Permission = collections.namedtuple('Permission',
                                    ['family', 'key', 'desc'])

PERMS = [
    Permission('perm_general', PERM_VIEW, 'View this domain'),
    Permission('perm_general', PERM_EDIT_PERM, 'Edit permissions of a role'),
    Permission('perm_general', PERM_MOD_BADGE, 'Show MOD badge'),
    Permission('perm_general', PERM_EDIT_DESCRIPTION,
               'Edit description of this domain'),
    Permission('perm_problem', PERM_CREATE_PROBLEM, 'Create problems'),
    Permission('perm_problem', PERM_EDIT_PROBLEM, 'Edit problems'),
    Permission('perm_problem', PERM_EDIT_PROBLEM_SELF, 'Edit own problems'),
    Permission('perm_problem', PERM_VIEW_PROBLEM, 'View problems'),
    Permission('perm_problem', PERM_VIEW_PROBLEM_HIDDEN,
               'View hidden problems'),
    Permission('perm_problem', PERM_SUBMIT_PROBLEM, 'Submit problem'),
    Permission('perm_problem', PERM_READ_PROBLEM_DATA, 'Read data of problem'),
    Permission('perm_problem', PERM_READ_PROBLEM_DATA_SELF,
               'Read data of own problems'),
    Permission('perm_record', PERM_READ_RECORD_CODE, 'Read record codes'),
    Permission('perm_record', PERM_REJUDGE_PROBLEM, 'Rejudge problems'),
    Permission('perm_record', PERM_REJUDGE, 'Rejudge records'),
    Permission('perm_problem_solution', PERM_VIEW_PROBLEM_SOLUTION,
               'View problem solutions'),
    Permission('perm_problem_solution', PERM_CREATE_PROBLEM_SOLUTION,
               'Create problem solutions'),
    Permission('perm_problem_solution', PERM_VOTE_PROBLEM_SOLUTION,
               'Vote problem solutions'),
    Permission('perm_problem_solution', PERM_EDIT_PROBLEM_SOLUTION,
               'Edit problem solutions'),
    Permission('perm_problem_solution',
               PERM_EDIT_PROBLEM_SOLUTION_SELF, 'Edit own problem solutions'),
    Permission('perm_problem_solution', PERM_DELETE_PROBLEM_SOLUTION,
               'Delete problem solutions'),
    Permission('perm_problem_solution', PERM_DELETE_PROBLEM_SOLUTION_SELF,
               'Delete own problem solutions'),
    Permission('perm_problem_solution', PERM_REPLY_PROBLEM_SOLUTION,
               'Reply problem solutions'),
    Permission('perm_problem_solution', PERM_EDIT_PROBLEM_SOLUTION_REPLY,
               'Edit problem solution replies'),
    Permission('perm_problem_solution', PERM_EDIT_PROBLEM_SOLUTION_REPLY_SELF,
               'Edit own problem solution replies'),
    Permission('perm_problem_solution', PERM_DELETE_PROBLEM_SOLUTION_REPLY,
               'Delete problem solution replies'),
    Permission('perm_problem_solution', PERM_DELETE_PROBLEM_SOLUTION_REPLY_SELF,
               'Delete own problem solution replies'),
    Permission('perm_discussion', PERM_VIEW_DISCUSSION, 'View discussions'),
    Permission('perm_discussion', PERM_CREATE_DISCUSSION,
               'Create discussions'),
    Permission('perm_discussion', PERM_HIGHLIGHT_DISCUSSION,
               'Highlight discussions'),
    Permission('perm_discussion', PERM_EDIT_DISCUSSION, 'Edit discussions'),
    Permission('perm_discussion', PERM_EDIT_DISCUSSION_SELF,
               'Edit own discussions'),
    Permission('perm_discussion', PERM_DELETE_DISCUSSION,
               'Delete discussions'),
    Permission('perm_discussion', PERM_DELETE_DISCUSSION_SELF,
               'Delete own discussions'),
    Permission('perm_discussion', PERM_REPLY_DISCUSSION, 'Reply discussions'),
    Permission('perm_discussion', PERM_EDIT_DISCUSSION_REPLY,
               'Edit discussion replies'),
    Permission('perm_discussion', PERM_EDIT_DISCUSSION_REPLY_SELF,
               'Edit own discussion replies'),
    Permission('perm_discussion', PERM_EDIT_DISCUSSION_REPLY_SELF_DISCUSSION,
               'Edit discussion replies of own discussion'),
    Permission('perm_discussion', PERM_DELETE_DISCUSSION_REPLY,
               'Delete discussion replies'),
    Permission('perm_discussion', PERM_DELETE_DISCUSSION_REPLY_SELF,
               'Delete own discussion replies'),
    Permission('perm_discussion', PERM_DELETE_DISCUSSION_REPLY_SELF_DISCUSSION,
               'Delete discussion replies of own discussion'),
    Permission('perm_contest', PERM_VIEW_CONTEST, 'View contests'),
    Permission('perm_contest', PERM_VIEW_CONTEST_SCOREBOARD,
               'View contest scoreboard'),
    Permission('perm_contest', PERM_VIEW_CONTEST_HIDDEN_SCOREBOARD,
               'View hidden contest submission status and scoreboard'),
    Permission('perm_contest', PERM_CREATE_CONTEST, 'Create contests'),
    Permission('perm_contest', PERM_ATTEND_CONTEST, 'Attend contests'),
    Permission('perm_contest', PERM_EDIT_CONTEST, 'Edit any contests'),
    Permission('perm_contest', PERM_EDIT_CONTEST_SELF, 'Edit own contests'),
    Permission('perm_homework', PERM_VIEW_HOMEWORK, 'View homework'),
    Permission('perm_homework', PERM_VIEW_HOMEWORK_SCOREBOARD,
               'View homework scoreboard'),
    Permission('perm_homework', PERM_VIEW_HOMEWORK_HIDDEN_SCOREBOARD,
               'View hidden homework submission status and scoreboard'),
    Permission('perm_homework', PERM_CREATE_HOMEWORK, 'Create homework'),
    Permission('perm_homework', PERM_ATTEND_HOMEWORK, 'Claim homework'),
    Permission('perm_homework', PERM_EDIT_HOMEWORK, 'Edit any homework'),
    Permission('perm_homework', PERM_EDIT_HOMEWORK_SELF, 'Edit own homework'),
    Permission('perm_training', PERM_VIEW_TRAINING, 'View training plans'),
    Permission('perm_training', PERM_CREATE_TRAINING, 'Create training plans'),
    Permission('perm_training', PERM_EDIT_TRAINING, 'Edit training plans'),
    Permission('perm_training', PERM_EDIT_TRAINING_SELF,
               'Edit own training plans'),
    Permission('perm_ranking', PERM_VIEW_RANKING, 'View ranking'),
    Permission('perm_rating', PERM_PROCESS_RATING, 'Process rating'),
]

PERMS_BY_FAMILY = collections.OrderedDict(
    (f, list(g)) for f, g in itertools.groupby(PERMS, key=lambda p: p.family))
PERMS_BY_KEY = collections.OrderedDict(zip((s.key for s in PERMS), PERMS))

# Privileges.
PRIV_NONE = 0
PRIV_SET_PRIV = 1 << 0
PRIV_SET_PERM = 1 << 1
PRIV_USER_PROFILE = 1 << 2
PRIV_REGISTER_USER = 1 << 3
PRIV_READ_PROBLEM_DATA = 1 << 4
PRIV_READ_PRETEST_DATA = 1 << 5
PRIV_READ_PRETEST_DATA_SELF = 1 << 6
PRIV_READ_RECORD_CODE = 1 << 7
PRIV_VIEW_HIDDEN_RECORD = 1 << 8
PRIV_WRITE_RECORD = 1 << 9
PRIV_CREATE_DOMAIN = 1 << 10
PRIV_VIEW_ALL_DOMAIN = 1 << 11
PRIV_MANAGE_ALL_DOMAIN = 1 << 12
PRIV_REJUDGE = 1 << 13
PRIV_VIEW_USER_SECRET = 1 << 14
PRIV_VIEW_JUDGE_STATISTICS = 1 << 15
PRIV_CREATE_FILE = 1 << 16
PRIV_UNLIMITED_QUOTA = 1 << 17
PRIV_DELETE_FILE = 1 << 18
PRIV_DELETE_FILE_SELF = 1 << 19
PRIV_MAKE_ANNOUNCEMENT = 1 << 20
PRIV_ALL = -1

DEFAULT_PRIV = PRIV_USER_PROFILE | PRIV_DELETE_FILE_SELF
JUDGE_PRIV = (PRIV_USER_PROFILE
              | PRIV_VIEW_ALL_DOMAIN
              | PRIV_READ_PROBLEM_DATA
              | PRIV_READ_PRETEST_DATA
              | PRIV_READ_RECORD_CODE
              | PRIV_WRITE_RECORD)

# Domains.
DOMAIN_ID_SYSTEM = 'system'
BASIC_PERMISSIONS = (
    PERM_VIEW |
    PERM_VIEW_PROBLEM |
    PERM_VIEW_PROBLEM_SOLUTION |
    PERM_VIEW_DISCUSSION |
    PERM_VIEW_CONTEST |
    PERM_VIEW_CONTEST_SCOREBOARD |
    PERM_VIEW_HOMEWORK |
    PERM_VIEW_HOMEWORK_SCOREBOARD |
    PERM_VIEW_TRAINING
)
DEFAULT_PERMISSIONS = (
    PERM_VIEW |
    PERM_VIEW_PROBLEM |
    PERM_EDIT_PROBLEM_SELF |
    PERM_SUBMIT_PROBLEM |
    PERM_SUBMIT_PROBLEM_CONTEST |
    PERM_READ_PROBLEM_DATA_SELF |
    PERM_VIEW_PROBLEM_SOLUTION |
    PERM_CREATE_PROBLEM_SOLUTION |
    PERM_VOTE_PROBLEM_SOLUTION |
    PERM_EDIT_PROBLEM_SOLUTION_SELF |
    PERM_DELETE_PROBLEM_SOLUTION_SELF |
    PERM_REPLY_PROBLEM_SOLUTION |
    PERM_EDIT_PROBLEM_SOLUTION_REPLY_SELF |
    PERM_DELETE_PROBLEM_SOLUTION_REPLY_SELF |
    PERM_VIEW_DISCUSSION |
    PERM_CREATE_DISCUSSION |
    PERM_EDIT_DISCUSSION_SELF |
    PERM_REPLY_DISCUSSION |
    PERM_EDIT_DISCUSSION_REPLY_SELF |
    # PERM_EDIT_DISCUSSION_REPLY_SELF_DISCUSSION |
    PERM_DELETE_DISCUSSION_REPLY_SELF |
    PERM_DELETE_DISCUSSION_REPLY_SELF_DISCUSSION |
    PERM_VIEW_CONTEST |
    PERM_VIEW_CONTEST_SCOREBOARD |
    PERM_ATTEND_CONTEST |
    PERM_EDIT_CONTEST_SELF |
    PERM_VIEW_HOMEWORK |
    PERM_VIEW_HOMEWORK_SCOREBOARD |
    PERM_ATTEND_HOMEWORK |
    PERM_EDIT_HOMEWORK_SELF |
    PERM_VIEW_TRAINING |
    PERM_CREATE_TRAINING |
    PERM_EDIT_TRAINING_SELF |
    PERM_VIEW_RANKING
)
ADMIN_PERMISSIONS = PERM_ALL

CONTRIBUTOR_PERMISSIONS = (
    PERM_VIEW |
    PERM_VIEW_PROBLEM |
    PERM_EDIT_PROBLEM_SELF |
    PERM_SUBMIT_PROBLEM |
    PERM_SUBMIT_PROBLEM_CONTEST |
    PERM_READ_PROBLEM_DATA_SELF |
    PERM_VIEW_PROBLEM_SOLUTION |
    PERM_CREATE_PROBLEM |
    PERM_CREATE_PROBLEM_SOLUTION |
    PERM_VOTE_PROBLEM_SOLUTION |
    PERM_EDIT_PROBLEM_SOLUTION_SELF |
    PERM_DELETE_PROBLEM_SOLUTION_SELF |
    PERM_REPLY_PROBLEM_SOLUTION |
    PERM_EDIT_PROBLEM_SOLUTION_REPLY_SELF |
    PERM_DELETE_PROBLEM_SOLUTION_REPLY_SELF |
    PERM_VIEW_DISCUSSION |
    PERM_CREATE_DISCUSSION |
    PERM_EDIT_DISCUSSION_SELF |
    PERM_REPLY_DISCUSSION |
    PERM_EDIT_DISCUSSION_REPLY_SELF |
    # PERM_EDIT_DISCUSSION_REPLY_SELF_DISCUSSION |
    PERM_DELETE_DISCUSSION_REPLY_SELF |
    PERM_DELETE_DISCUSSION_REPLY_SELF_DISCUSSION |
    PERM_VIEW_CONTEST |
    PERM_VIEW_CONTEST_SCOREBOARD |
    PERM_ATTEND_CONTEST |
    PERM_EDIT_CONTEST_SELF |
    PERM_VIEW_HOMEWORK |
    PERM_VIEW_HOMEWORK_SCOREBOARD |
    PERM_ATTEND_HOMEWORK |
    PERM_EDIT_HOMEWORK_SELF |
    PERM_VIEW_TRAINING |
    PERM_CREATE_TRAINING |
    PERM_EDIT_TRAINING_SELF |
    PERM_VIEW_RANKING
)

COORDINATOR_PERMISSIONS = (
    PERM_VIEW |
    PERM_VIEW_PROBLEM |
    PERM_EDIT_PROBLEM_SELF |
    PERM_SUBMIT_PROBLEM |
    PERM_SUBMIT_PROBLEM_CONTEST |
    PERM_READ_PROBLEM_DATA_SELF |
    PERM_VIEW_PROBLEM_SOLUTION |
    PERM_CREATE_PROBLEM |
    PERM_CREATE_PROBLEM_SOLUTION |
    PERM_VOTE_PROBLEM_SOLUTION |
    PERM_EDIT_PROBLEM_SOLUTION_SELF |
    PERM_DELETE_PROBLEM_SOLUTION_SELF |
    PERM_REPLY_PROBLEM_SOLUTION |
    PERM_EDIT_PROBLEM_SOLUTION_REPLY_SELF |
    PERM_DELETE_PROBLEM_SOLUTION_REPLY_SELF |
    PERM_VIEW_DISCUSSION |
    PERM_CREATE_DISCUSSION |
    PERM_EDIT_DISCUSSION_SELF |
    PERM_REPLY_DISCUSSION |
    PERM_EDIT_DISCUSSION_REPLY_SELF |
    # PERM_EDIT_DISCUSSION_REPLY_SELF_DISCUSSION |
    PERM_DELETE_DISCUSSION_REPLY_SELF |
    PERM_DELETE_DISCUSSION_REPLY_SELF_DISCUSSION |
    PERM_VIEW_CONTEST |
    PERM_VIEW_CONTEST_SCOREBOARD |
    PERM_ATTEND_CONTEST |
    PERM_CREATE_CONTEST |
    PERM_EDIT_CONTEST_SELF |
    PERM_VIEW_HOMEWORK |
    PERM_VIEW_HOMEWORK_SCOREBOARD |
    PERM_ATTEND_HOMEWORK |
    PERM_EDIT_HOMEWORK_SELF |
    PERM_VIEW_TRAINING |
    PERM_CREATE_TRAINING |
    PERM_EDIT_TRAINING_SELF |
    PERM_VIEW_RANKING
)

TEMP_USER_PERMISSIONS = (
    PERM_VIEW |
    PERM_VIEW_PROBLEM |
    PERM_SUBMIT_PROBLEM_CONTEST |
    PERM_VIEW_CONTEST |
    PERM_VIEW_CONTEST_SCOREBOARD
)

# Roles.
ROLE_ROOT = 'root'
ROLE_GUEST = 'guest'
ROLE_DEFAULT = 'default'
ROLE_MEMBER = 'member'
ROLE_ADMIN = 'admin'
ROLE_CONTRIBUTOR = 'contributor'
ROLE_COORDINATOR = 'coordinator'

BuiltinRoleDescriptor = functools.partial(
    collections.namedtuple('BuiltinRoleDescriptor',
                           ['modifiable', 'default_permission', 'description']))

# Built-in roles cannot be deleted.
BUILTIN_ROLE_DESCRIPTORS = {
    ROLE_ROOT: BuiltinRoleDescriptor(False, PERM_ALL, 'Always granted all privileges'),
    ROLE_GUEST: BuiltinRoleDescriptor(True, BASIC_PERMISSIONS, 'Valid for visitors'),
    ROLE_DEFAULT: BuiltinRoleDescriptor(True, DEFAULT_PERMISSIONS, 'Valid for registered users who are not members of the domain'),
}

DOMAIN_SYSTEM = {
    '_id': DOMAIN_ID_SYSTEM,
    'owner_uid': 0,
    'roles': {ROLE_GUEST: BASIC_PERMISSIONS,
              ROLE_DEFAULT: DEFAULT_PERMISSIONS,
              ROLE_MEMBER: DEFAULT_PERMISSIONS,
              ROLE_ADMIN: ADMIN_PERMISSIONS,
              ROLE_CONTRIBUTOR: CONTRIBUTOR_PERMISSIONS,
              ROLE_COORDINATOR: COORDINATOR_PERMISSIONS},
    'gravatar': '',
    'name': 'SeriousOJ',
    'bulletin': ''
}
DOMAINS = [DOMAIN_SYSTEM]

# Users.
UID_SYSTEM = 0
UNAME_SYSTEM = 'SeriousOJ'
USER_SYSTEM = {
    '_id': UID_SYSTEM,
    'uname': UNAME_SYSTEM,
    'uname_lower': UNAME_SYSTEM.strip().lower(),
    'mail': '',
    'mail_lower': '',
    'salt': '',
    'hash': 'vj4|',
    'gender': constant.model.USER_GENDER_OTHER,
    'regat': datetime.datetime.utcfromtimestamp(0),
    'regip': '',
    'priv': PRIV_NONE,
    'loginat': datetime.datetime.utcnow(),
    'loginip': '',
    'gravatar': ''
}
UID_GUEST = 1
UNAME_GUEST = 'Guest'
USER_GUEST = {
    '_id': UID_GUEST,
    'uname': UNAME_GUEST,
    'uname_lower': UNAME_GUEST.strip().lower(),
    'mail': '',
    'mail_lower': '',
    'salt': '',
    'hash': 'vj4|',
    'gender': constant.model.USER_GENDER_OTHER,
    'regat': datetime.datetime.utcfromtimestamp(0),
    'regip': '',
    'priv': PRIV_REGISTER_USER,
    'loginat': datetime.datetime.utcnow(),
    'loginip': '',
    'gravatar': ''
}
DOMAIN_USER_GUEST = {
    # in every domain:
    'rank': 0,
    'role': ROLE_GUEST,
    'level': 0,
    'num_submit': 0,
    'num_accept': 0
}
USERS = [USER_SYSTEM, USER_GUEST]

# Key represents level
# Value represents percent
# E.g. (10, 1) means that people whose rank is less than 1% will get Level 10
LEVELS = collections.OrderedDict([(10, 1),
                                  (9, 2),
                                  (8, 10),
                                  (7, 20),
                                  (6, 30),
                                  (5, 40),
                                  (4, 70),
                                  (3, 90),
                                  (2, 95),
                                  (1, 100)])

# Footer extra HTMLs. TODO(iceboy): remove.
FOOTER_EXTRA_HTMLS = ['© <a href="https://github.com/Eluminatis-of-LU/serious-oj">SeriousOJ</a> Forked from © 2005 - 2023 <a href="https://vijos.org/">Vijos.org</a>',
                      '<a href=https://github.com/Eluminatis-of-LU/serious-oj/commit/' + version.get()[:7] + '/>' + version.get()[:7] + '</a>']

PROBLEM_CATEGORIES = collections.OrderedDict([
    ('Beginners', ['Beginners']), 
    ('DP', [
        'LCS',
        'LIS'
    ]),
    ('Graph_Theory', ['DFS', 'BFS', 'Tree', 'Shortest_Path']),
     ('Math', ['Number_Theory', 'Probability', 'Combinatorics', 'Geometry', 'Basic_Math']),
     ('Bit_Manipulation', ['Bitmask']),
     ('Implementation', ['Simulation', 'Games', 'String_Processing',
     'Data_Structure', 'Ad_Hoc', 'Sorting', 'Brute_Force', 'Two_Pointer', 'Constructive_Algorithm']),
     ('Greedy', ['Greedy']),
     ('Data_Structure', ['Segment_Tree','Divide_and_Conquer', 'Binary_Indexed_Tree', 'Disjoint_Set',
     'Sparse_Table', 'Trie', 'Heap', 'Stack', 'Queue', 'Hash_Table', 'Binary_Search', 'Ternary_Search']),
])
PROBLEM_SUB_CATEGORIES = {}
for category, sub_categories in PROBLEM_CATEGORIES.items():
    assert ' ' not in category
    assert ',' not in category
    for sub_category in sub_categories:
        assert ' ' not in sub_category
        assert ',' not in sub_category
        assert sub_category not in PROBLEM_SUB_CATEGORIES
        PROBLEM_SUB_CATEGORIES[sub_category] = category


VNODE_MISSING = {'title': '(missing)'}
DEFAULT_VNODES = collections.OrderedDict([
    ('OJ', [
        {'pic': None, 'name': 'CodeForces'},
        {'pic': None, 'name': 'TopCoder'},
        {'pic': None, 'name': 'LightOJ'},
        {'pic': None, 'name': 'CodeChef'},
        {'pic': None, 'name': 'AtCoder'},
        {'pic': None, 'name': 'Toph'},
        {'pic': None, 'name': 'UVA'},
    ]),
    ('Language', [
        {'pic': None, 'name': 'C'},
        {'pic': None, 'name': 'C++'},
        {'pic': None, 'name': 'C#'},
        {'pic': None, 'name': 'Java'},
        {'pic': None, 'name': 'Python3'},
    ]),
    ('Notes', [
        {'pic': None, 'name': 'Editorials'},
        {'pic': None, 'name': 'Tutorials'},
    ])
])
