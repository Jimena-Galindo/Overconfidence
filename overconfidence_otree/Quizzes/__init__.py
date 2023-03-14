from otree.api import *
import numpy as np
import pandas as pd
from pathlib import Path


doc = """
Quizzes
"""

# FUNCTIONS
math = pd.read_csv(Path.cwd().joinpath('Quiz questions/Trivia - Math.csv'))
math = math.to_numpy()

verbal = pd.read_csv(Path.cwd().joinpath('Quiz questions/Trivia - Verbal.csv'))
verbal = verbal.to_numpy()

sports = pd.read_csv(Path.cwd().joinpath('Quiz questions/Trivia - Sports and Videogames.csv'))
sports = sports.to_numpy()

science = pd.read_csv(Path.cwd().joinpath('Quiz questions/Trivia - Science and Technology.csv'))
science = science.to_numpy()

pop = pd.read_csv(Path.cwd().joinpath('Quiz questions/Trivia - Pop Culture and Art.csv'))
pop = pop.to_numpy()

us = pd.read_csv(Path.cwd().joinpath('Quiz questions/Trivia - u Geography.csv'))
us = us.to_numpy()


def make_field(topic, q_number):
    return models.StringField(
        choices=[['a', topic[q_number, 1]], ['b', topic[q_number, 2]], ['c', topic[q_number, 3]], ['d', topic[q_number, 4]]],
        label=topic[q_number, 0],
        widget=widgets.RadioSelect,
        blank=True
    )


class C(BaseConstants):
    NAME_IN_URL = 'Quizzes'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    math0 = make_field(math, 0)
    math1 = make_field(math, 1)
    math2 = make_field(math, 2)
    math3 = make_field(math, 3)
    math4 = make_field(math, 4)
    math5 = make_field(math, 5)
    math6 = make_field(math, 6)
    math7 = make_field(math, 7)
    math8 = make_field(math, 8)
    math9 = make_field(math, 9)
    math10 = make_field(math, 10)
    math11 = make_field(math, 11)
    math12 = make_field(math, 12)
    math13 = make_field(math, 13)
    math14 = make_field(math, 14)
    math15 = make_field(math, 15)
    math16 = make_field(math, 16)
    math17 = make_field(math, 17)
    math18 = make_field(math, 18)
    math19 = make_field(math, 19)

    verbal0 = make_field(verbal, 0)
    verbal1 = make_field(verbal, 1)
    verbal2 = make_field(verbal, 2)
    verbal3 = make_field(verbal, 3)
    verbal4 = make_field(verbal, 4)
    verbal5 = make_field(verbal, 5)
    verbal6 = make_field(verbal, 6)
    verbal7 = make_field(verbal, 7)
    verbal8 = make_field(verbal, 8)
    verbal9 = make_field(verbal, 9)
    verbal10 = make_field(verbal, 10)
    verbal11 = make_field(verbal, 11)
    verbal12 = make_field(verbal, 12)
    verbal13 = make_field(verbal, 13)
    verbal14 = make_field(verbal, 14)
    verbal15 = make_field(verbal, 15)
    verbal16 = make_field(verbal, 16)
    verbal17 = make_field(verbal, 17)
    verbal18 = make_field(verbal, 18)
    verbal19 = make_field(verbal, 19)

    pop0 = make_field(pop, 0)
    pop1 = make_field(pop, 1)
    pop2 = make_field(pop, 2)
    pop3 = make_field(pop, 3)
    pop4 = make_field(pop, 4)
    pop5 = make_field(pop, 5)
    pop6 = make_field(pop, 6)
    pop7 = make_field(pop, 7)
    pop8 = make_field(pop, 8)
    pop9 = make_field(pop, 9)
    pop10 = make_field(pop, 10)
    pop11 = make_field(pop, 11)
    pop12 = make_field(pop, 12)
    pop13 = make_field(pop, 13)
    pop14 = make_field(pop, 14)
    pop15 = make_field(pop, 15)
    pop16 = make_field(pop, 16)
    pop17 = make_field(pop, 17)
    pop18 = make_field(pop, 18)
    pop19 = make_field(pop, 19)

    us0 = make_field(us, 0)
    us1 = make_field(us, 1)
    us2 = make_field(us, 2)
    us3 = make_field(us, 3)
    us4 = make_field(us, 4)
    us5 = make_field(us, 5)
    us6 = make_field(us, 6)
    us7 = make_field(us, 7)
    us8 = make_field(us, 8)
    us9 = make_field(us, 9)
    us10 = make_field(us, 10)
    us11 = make_field(us, 11)
    us12 = make_field(us, 12)
    us13 = make_field(us, 13)
    us14 = make_field(us, 14)
    us15 = make_field(us, 15)
    us16 = make_field(us, 16)
    us17 = make_field(us, 17)
    us18 = make_field(us, 18)
    us19 = make_field(us, 19)

    science0 = make_field(science, 0)
    science1 = make_field(science, 1)
    science2 = make_field(science, 2)
    science3 = make_field(science, 3)
    science4 = make_field(science, 4)
    science5 = make_field(science, 5)
    science6 = make_field(science, 6)
    science7 = make_field(science, 7)
    science8 = make_field(science, 8)
    science9 = make_field(science, 9)
    science10 = make_field(science, 10)
    science11 = make_field(science, 11)
    science12 = make_field(science, 12)
    science13 = make_field(science, 13)
    science14 = make_field(science, 14)
    science15 = make_field(science, 15)
    science16 = make_field(science, 16)
    science17 = make_field(science, 17)
    science18 = make_field(science, 18)
    science19 = make_field(science, 19)

    sports0 = make_field(sports, 0)
    sports1 = make_field(sports, 1)
    sports2 = make_field(sports, 2)
    sports3 = make_field(sports, 3)
    sports4 = make_field(sports, 4)
    sports5 = make_field(sports, 5)
    sports6 = make_field(sports, 6)
    sports7 = make_field(sports, 7)
    sports8 = make_field(sports, 8)
    sports9 = make_field(sports, 9)
    sports10 = make_field(sports, 10)
    sports11 = make_field(sports, 11)
    sports12 = make_field(sports, 12)
    sports13 = make_field(sports, 13)
    sports14 = make_field(sports, 14)
    sports15 = make_field(sports, 15)
    sports16 = make_field(sports, 16)
    sports17 = make_field(sports, 17)
    sports18 = make_field(sports, 18)
    sports19 = make_field(sports, 19)



# PAGES
class VerbalQuiz(Page):
    form_model = 'player'
    form_fields = ['verbal0', 
                   'verbal1', 
                   'verbal2',
                   'verbal3', 
                   'verbal4', 
                   'verbal5', 
                   'verbal6', 
                   'verbal7',
                   'verbal8',
                   'verbal9',
                   'verbal10',
                   'verbal11',
                   'verbal12',
                   'verbal13',
                   'verbal14',
                   'verbal15',
                   'verbal16',
                   'verbal17',
                   'verbal18',
                   'verbal19', 
                   ]


class MathQuiz(Page):
    form_model = 'player'
    form_fields = ['math0', 
                   'math1', 
                   'math2',
                   'math3', 
                   'math4', 
                   'math5', 
                   'math6', 
                   'math7',
                   'math8',
                   'math9',
                   'math10',
                   'math11',
                   'math12',
                   'math13',
                   'math14',
                   'math15',
                   'math16',
                   'math17',
                   'math18',
                   'math19', 
                   ]
    

class PopQuiz(Page):
    form_model = 'player'
    form_fields = ['pop0', 
                   'pop1', 
                   'pop2',
                   'pop3', 
                   'pop4', 
                   'pop5', 
                   'pop6', 
                   'pop7',
                   'pop8',
                   'pop9',
                   'pop10',
                   'pop11',
                   'pop12',
                   'pop13',
                   'pop14',
                   'pop15',
                   'pop16',
                   'pop17',
                   'pop18',
                   'pop19', 
                   ]
    

class SportsQuiz(Page):
    form_model = 'player'
    form_fields = ['sports0', 
                   'sports1', 
                   'sports2',
                   'sports3', 
                   'sports4', 
                   'sports5', 
                   'sports6', 
                   'sports7',
                   'sports8',
                   'sports9',
                   'sports10',
                   'sports11',
                   'sports12',
                   'sports13',
                   'sports14',
                   'sports15',
                   'sports16',
                   'sports17',
                   'sports18',
                   'sports19', 
                   ]
    

class ScienceQuiz(Page):
    form_model = 'player'
    form_fields = ['science0', 
                   'science1', 
                   'science2',
                   'science3', 
                   'science4', 
                   'science5', 
                   'science6', 
                   'science7',
                   'science8',
                   'science9',
                   'science10',
                   'science11',
                   'science12',
                   'science13',
                   'science14',
                   'science15',
                   'science16',
                   'science17',
                   'science18',
                   'science19', 
                   ]


class USQuiz(Page):
    form_model = 'player'
    form_fields = ['us0', 
                   'us1', 
                   'us2',
                   'us3', 
                   'us4', 
                   'us5', 
                   'us6', 
                   'us7',
                   'us8',
                   'us9',
                   'us10',
                   'us11',
                   'us12',
                   'us13',
                   'us14',
                   'us15',
                   'us16',
                   'us17',
                   'us18',
                   'us19', 
                   ]


class ResultsWaitPage(WaitPage):
    pass


page_sequence = [MathQuiz, VerbalQuiz, PopQuiz, SportsQuiz, ScienceQuiz, USQuiz]
