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
    TASKS = ['Math', 'Verbal', 'Science and Technology', 'Sports and Video Games', 'US Geography', 'Pop-Culture and Art']


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    gender = models.StringField(label='What best describes your gender identity: Male, Female, Other?',
                                choices=['Male', 'Female', 'Non-binary'])
    nationality = models.StringField(label='What is your nationality?', choices=['US National', 'non-US National'])


# FUNCTIONS


# PAGES
class Instructions(Page):
    pass

class Questionnaire(Page):
    form_model = 'player'
    form_fields = ['gender',
                   'nationality']

    @staticmethod
    def before_next_page(player, timeout_happened):
        participant = player.participant
        participant.gender = player.gender
        participant.nationality = player.nationality
        participant.major = player.major


class ResultsWaitPage(WaitPage):
    title_text = "End of Part 2"
    body_text = "Please wait while others finish Part 2 of the experiment"

    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

class Results(Page):
    @staticmethod
    def vars_for_template(player):

        participant = player.participant
        part1_pay = np.round(participant.part1_score * .2, 2)
        part2_pay = np.round(participant.part2_score * .2, 2)
        return dict( part1_topic=participant.part1_topic,
                     part1_score=participant.part1_score,
                     part2_topic=participant.part2_topic,
                     part2_score=participant.part2_score,
                     total=(participant.part2_score+participant.part1_score),
                     pay1=part1_pay,
                     pay2=part2_pay,
                     pay_tot=part2_pay+part1_pay+10,
                     payoff=participant.payoff_plus_participation_fee())


page_sequence = [Questionnaire, ResultsWaitPage, Results]
