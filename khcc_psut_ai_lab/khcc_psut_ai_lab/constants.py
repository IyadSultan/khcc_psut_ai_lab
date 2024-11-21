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



   

# AI Core Tags
AI_CORE_TAGS = [
    'deep-learning',
    'machine-learning',
    'neural-networks',
    'computer-vision',
    'nlp',
    'reinforcement-learning',
    'transformers',
    'cnn',
    'rnn',
    'lstm',
    'gan',
    'transfer-learning',
    'supervised-learning',
    'unsupervised-learning',
    'bert',
    'attention-mechanism',
    'feature-engineering',
    'ensemble-methods',
    'semantic-segmentation',
    'object-detection'
]

# Healthcare Specific Tags
HEALTHCARE_TAGS = [
    'medical-imaging',
    'radiology',
    'oncology',
    'pathology',
    'clinical-trials',
    'diagnosis',
    'prognosis',
    'patient-care',
    'ehr',
    'bioinformatics',
    'genomics',
    'precision-medicine',
    'drug-discovery',
    'cancer-detection',
    'medical-diagnosis',
    'healthcare-analytics',
    'biomarkers',
    'treatment-planning',
    'disease-prediction',
    'patient-monitoring'
]

# Technical Implementation Tags
TECHNICAL_TAGS = [
    'python',
    'tensorflow',
    'pytorch',
    'keras',
    'scikit-learn',
    'opencv',
    'pandas',
    'numpy',
    'data-preprocessing',
    'data-visualization',
    'algorithm-optimization',
    'gpu-computing',
    'distributed-computing',
    'cloud-computing',
    'docker',
    'api-development',
    'web-interface',
    'database',
    'deployment',
    'real-time-processing'
]

# Data Related Tags
DATA_TAGS = [
    'data-analysis',
    'data-mining',
    'big-data',
    'data-augmentation',
    'data-cleaning',
    'data-collection',
    'data-labeling',
    'data-privacy',
    'data-security',
    'data-validation',
    'dataset-creation',
    'data-pipeline',
    'data-integration',
    'data-annotation',
    'data-quality',
    'data-governance',
    'data-standardization',
    'time-series',
    'structured-data',
    'unstructured-data'
]

# Research and Development Tags
RESEARCH_TAGS = [
    'research',
    'experimental',
    'proof-of-concept',
    'benchmark',
    'ablation-study',
    'literature-review',
    'performance-analysis',
    'comparative-study',
    'pilot-study',
    'validation-study',
    'methodology',
    'baseline',
    'state-of-the-art',
    'innovation',
    'novel-approach',
    'reproducible-research',
    'open-source',
    'collaboration',
    'interdisciplinary',
    'cross-validation'
]

# Application and Impact Tags
IMPACT_TAGS = [
    'clinical-application',
    'patient-outcome',
    'cost-reduction',
    'workflow-optimization',
    'decision-support',
    'risk-assessment',
    'quality-improvement',
    'resource-optimization',
    'screening-tool',
    'monitoring-system',
    'early-detection',
    'predictive-analytics',
    'automated-reporting',
    'clinical-workflow',
    'healthcare-access',
    'patient-safety',
    'treatment-optimization',
    'medical-research',
    'healthcare-policy',
    'public-health'
]

# Combine all tags
ALL_TAGS = (
    AI_CORE_TAGS + 
    HEALTHCARE_TAGS + 
    TECHNICAL_TAGS + 
    DATA_TAGS + 
    RESEARCH_TAGS + 
    IMPACT_TAGS
)

