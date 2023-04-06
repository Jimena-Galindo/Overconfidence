from otree.api import *
import numpy as np
import pandas as pd
import random
from pathlib import Path


doc = """
Questionnaire
"""


class C(BaseConstants):
    NAME_IN_URL = 'Questionnaire'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    gender = models.StringField(label='What best describes your gender identity: Male, Female, Other?',
                                choices=['Male', 'Female', 'Other'])
    nationality = models.StringField(label='What is your nationality?')
    major = models.StringField(label='What best describes your major?',
                               choices=['Anthropology',
                                        'Art',
                                        'Art History',
                                        'Biology ',
                                        'Biomolecular Science',
                                        'Business',
                                        'Chemistry',
                                        'Cinema',
                                        'Civil Engineering',
                                        'Classics',
                                        'Computer Science',
                                        'Data Science',
                                        'Digital Art and Design',
                                        'Digital Communications and Media',
                                        'Digital Media',
                                        'Drama',
                                        'Education Studies',
                                        'Electrical Engineering',
                                        'Economics',
                                        'English',
                                        'Environmental Studies',
                                        'European and Mediterranean Studies',
                                        'Finance',
                                        'Game Design',
                                        'Global Affairs',
                                        'Healthcare',
                                        'History',
                                        'Hotel and Tourism Management',
                                        'International Relations',
                                        'Journalism',
                                        'Language Studies',
                                        'Leadership and Management Studies',
                                        'Literature',
                                        'Management',
                                        'Marketing',
                                        'Mathematics',
                                        'Mechanical Engineering',
                                        'Medical Sciences',
                                        'Music',
                                        'Music Business',
                                        'Nutrition and Food Studies',
                                        'Other Humanities',
                                        'Other Social Sciences',
                                        'Performance',
                                        'Philosophy',
                                        'Photography',
                                        'Physics',
                                        'Politics',
                                        'Psychology',
                                        'Public Health',
                                        'Public Policy',
                                        'Real Estate',
                                        'Religious Studies',
                                        'Social and Cultural Analysis',
                                        'Social Work',
                                        'Sociology',
                                        'Sports Management',
                                        'Teaching',
                                        'Theater']
                               )


# FUNCTIONS


# PAGES
class Instructions(Page):
    pass

class Questionnaire(Page):
    form_model = 'player'
    form_fields = ['gender',
                   'nationality',
                   'major']

    @staticmethod
    def before_next_page(player, timeout_happened):
        participant = player.participant
        participant.gender = player.gender
        participant.nationality = player.nationality


class ResultsWaitPage(WaitPage):
    pass


page_sequence = [Questions, Instructions]
