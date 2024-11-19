# Talent Types
TALENT_TYPES = [
    ('ai', 'AI Talent'),
    ('healthcare', 'Healthcare Talent'),
    ('quality', 'Quality Talent'),
    ('engineering', 'Engineering Talent'),
    ('planning', 'Planning Talent'),
    ('design', 'Design Talent'),
    ('lab', 'Lab Talent'),
    ('extra', 'Extra Talent'),
]

# For easy lookup
TALENT_DICT = dict(TALENT_TYPES)

# Team Member Roles
TEAM_ROLES = [
    ('founder', 'Team Founder'),
    ('moderator', 'Team Moderator'),
    ('member', 'Team Member')
]

TEAM_ROLES_DICT = dict(TEAM_ROLES)


# Team Settings
MAX_TEAM_SIZE = 50  # Maximum allowed team size 
DEFAULT_TEAM_SIZE = 1  # Default size when creating new team

# Notification Types
NOTIFICATION_TYPES = (
    'team_activity',
    'team_invitation',
    'team_role_change'
)


