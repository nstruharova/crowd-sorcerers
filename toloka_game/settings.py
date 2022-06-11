from os import environ

SESSION_CONFIGS = [

    dict(
        name='wsd_app',
        num_demo_participants=3,
        group_size=3,
        app_sequence=[
            'intro_matcher', # common intro
            'matcher',       # app that match participants into groups
            'wsd_app',       # the wsd game
            'blocker',       # participants move to this app when they're blocked
            'last'
        ]
    ),
    dict(
        name='basicq_toloka',
        language='en',
        for_toloka=True,
        num_demo_participants=1,
        app_sequence=[
            'basicq',
        ]
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=0.01, participation_fee=0.02, doc="", min_length='15 min',
    toloka_participation_fee=1,
    time_for_decision=60,
    time_for_instructions=90,
    matching_waiting_time=90,
    mturk_hit_settings=dict(
        keywords='30 seconds demographic study',
        title='30 seconds demographic study',
        description='Follow the link and answer a few simple questions.',
        frame_height=500,
        template='global/mturk_template.html',
        minutes_allotted_per_assignment=60,
        expiration_hours=7 * 24,
        qualification_requirements=[
            {
                'QualificationTypeId': "00000000000000000071",
                'Comparator': "In",
                'LocaleValues': [{'Country': "US"}, {'Country': "GB"}]
            },
        ]
        # grant_qualification_id='YOUR_QUALIFICATION_ID_HERE', # to prevent retakes
    ),
)

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = 'u%f)r#g+&1mg-0yl+q#at=l@(a7dytm9hb92+#2422vi)e#2!p'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree', 'matcher']
ROOMS = [

    dict(
        name='toloka',
        display_name='Toloka'
    ),
]
