from os import environ


SESSION_CONFIGS = [
    dict(
        name='Ego',
        num_demo_participants=2,
        app_sequence=['Quizzes', 'Signals', 'Questionnaire']
    ),
    dict(
        name='Stereotype',
        num_demo_participants=2,
        app_sequence=['Quizzes', 'SignalsOther', 'Questionnaire']
    )
]


# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = [
    'task_rounds',
    'verbal_score',
    'math_score',
    'science_score',
    'pop_score',
    'us_score',
    'sports_score',
    'verbal_questions',
    'math_questions',
    'science_questions',
    'pop_questions',
    'us_questions',
    'sports_questions',
    'age',
    'gender',
    'major',
    'nationality',
    'part1_score',
    'part1_topic']

SESSION_FIELDS = ['seed',
                  'w_verbal',
                  'w_math',
                  'w_pop',
                  'w_science',
                  'w_sports',
                  'w_us',
                  'outcomes_verbal',
                  'outcomes_math',
                  'outcomes_sports',
                  'outcomes_science',
                  'outcomes_pop',
                  'outcomes_us']

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ROOMS = [
    dict(
        name='cess_lab',
        display_name='cess',
    ),
]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """
"""


SECRET_KEY = '2516807391076'

INSTALLED_APPS = ['otree']



