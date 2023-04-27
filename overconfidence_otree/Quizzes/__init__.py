from otree.api import *
import numpy as np
import pandas as pd
import random
from pathlib import Path


doc = """
Quizzes
"""

# FUNCTIONS
math = pd.read_csv(Path.cwd().joinpath('Quiz questions/Trivia - Math.csv'))
math = math.sample(frac=1)
math = math.to_numpy()

verbal = pd.read_csv(Path.cwd().joinpath('Quiz questions/Trivia - Verbal.csv'))
verbal = verbal.sample(frac=1)
verbal = verbal.to_numpy()

sports = pd.read_csv(Path.cwd().joinpath('Quiz questions/Trivia - Sports and Videogames.csv'))
sports = sports.sample(frac=1)
sports = sports.to_numpy()

science = pd.read_csv(Path.cwd().joinpath('Quiz questions/Trivia - Science and Technology.csv'))
science = science.sample(frac=1)
science = science.to_numpy()

pop = pd.read_csv(Path.cwd().joinpath('Quiz questions/Trivia - Pop Culture and Art.csv'))
pop = pop.sample(frac=1)
pop = pop.to_numpy()

us = pd.read_csv(Path.cwd().joinpath('Quiz questions/Trivia - US Geography.csv'))
us = us.sample(frac=1)
us = us.to_numpy()

# a function that takes the questions matrix and turns them into form fields
# (need to deal with the questions that have fewer than 4 options)
def make_field(topic, q_number):
    return models.StringField(
        choices=[['a', topic[q_number, 1]],
                 ['b', topic[q_number, 2]],
                 ['c', topic[q_number, 3]],
                 ['d', topic[q_number, 4]]
                 ],
        label=topic[q_number, 0],
        widget=widgets.RadioSelect,
        blank=True
    )

class C(BaseConstants):
    NAME_IN_URL = 'Quizzes'
    PLAYERS_PER_GROUP = None
    # time limit for each quiz. the form submits when time runs out
    TIME = 120
    # List of the quizz titles
    TASKS = ['Math', 'Verbal', 'Science and Technology', 'Sports and Video Games', 'US Geography', 'Pop-Culture and Art']
    NUM_ROUNDS = len(TASKS)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    topic = models.StringField()
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

    score = models.IntegerField(initial=0)

    math_belief=models.IntegerField(min=0, max=20,
                                    label='How many questions do you think you answered correctly in the Math Quiz')
    verbal_belief = models.IntegerField(min=0, max=20,
                                      label='How many questions do you think you answered correctly in the Verbal Quiz')
    pop_belief = models.IntegerField(min=0, max=20,
                                        label='How many questions do you think you answered correctly in the Pop Culture and Art Quiz')
    science_belief = models.IntegerField(min=0, max=20,
                                        label='How many questions do you think you answered correctly in the Science and Technology Quiz')
    us_belief = models.IntegerField(min=0, max=20,
                                        label='How many questions do you think you answered correctly in the US Geography Quiz')
    sports_belief = models.IntegerField(min=0, max=20,
                                        label='How many questions do you think you answered correctly in the Sports and Videogames Quiz')


# FUNCTIONS
def creating_session(subsession: Subsession):
    # randomize the order of quizzes
    if subsession.round_number == 1:
        for p in subsession.get_players():
            round_numbers = list(range(1, C.NUM_ROUNDS + 1))
            random.shuffle(round_numbers)
            task_rounds = dict(zip(C.TASKS, round_numbers))
            p.participant.task_rounds = task_rounds


#PAGES
class Instructions(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1


class Start(Page):
    @staticmethod
    def vars_for_template(player):
        # get the topic for the current round to pass for page titles
        participant = player.participant
        key_list = list(participant.task_rounds.keys())
        val_list = list(participant.task_rounds.values())
        position = val_list.index(player.round_number)
        player.topic = key_list[position]
        return dict(topic=player.topic)

class MathQuiz(Page):
    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return player.round_number == participant.task_rounds['Math']

    timeout_seconds = C.TIME
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

    @staticmethod
    def before_next_page(player, timeout_happened):
        # check which answers were correct and compute the score for the quiz

        # load the answers from the data
        correct_ans = math[:, 5]

        # get the subject's answers
        ans = [player.field_maybe_none('math0'),
               player.field_maybe_none('math1'),
               player.field_maybe_none('math2'),
               player.field_maybe_none('math3'),
               player.field_maybe_none('math4'),
               player.field_maybe_none('math5'),
               player.field_maybe_none('math6'),
               player.field_maybe_none('math7'),
               player.field_maybe_none('math8'),
               player.field_maybe_none('math9'),
               player.field_maybe_none('math10'),
               player.field_maybe_none('math11'),
               player.field_maybe_none('math12'),
               player.field_maybe_none('math13'),
               player.field_maybe_none('math14'),
               player.field_maybe_none('math15'),
               player.field_maybe_none('math16'),
               player.field_maybe_none('math17'),
               player.field_maybe_none('math18'),
               player.field_maybe_none('math19'),
               ]

        # check if they are the same
        check = [ans[i] == correct_ans[i] for i in range(len(ans))]

        # compute the score
        player.score = sum(check)
        participant = player.participant
        participant.math_score = player.score


class VerbalQuiz(Page):
    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return player.round_number == participant.task_rounds['Verbal']

    timeout_seconds = C.TIME
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

    @staticmethod
    def before_next_page(player, timeout_happened):
        correct_ans = verbal[:, 5]

        ans = [player.field_maybe_none('verbal0'),
               player.field_maybe_none('verbal1'),
               player.field_maybe_none('verbal2'),
               player.field_maybe_none('verbal3'),
               player.field_maybe_none('verbal4'),
               player.field_maybe_none('verbal5'),
               player.field_maybe_none('verbal6'),
               player.field_maybe_none('verbal7'),
               player.field_maybe_none('verbal8'),
               player.field_maybe_none('verbal9'),
               player.field_maybe_none('verbal10'),
               player.field_maybe_none('verbal11'),
               player.field_maybe_none('verbal12'),
               player.field_maybe_none('verbal13'),
               player.field_maybe_none('verbal14'),
               player.field_maybe_none('verbal15'),
               player.field_maybe_none('verbal16'),
               player.field_maybe_none('verbal17'),
               player.field_maybe_none('verbal18'),
               player.field_maybe_none('verbal19'),
               ]

        check = [ans[i] == correct_ans[i] for i in range(len(ans))]

        player.score = sum(check)
        participant = player.participant
        participant.verbal_score = player.score
        
        participant.verbal_questions = verbal[:, 0]
    

class PopQuiz(Page):
    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return player.round_number == participant.task_rounds['Pop-Culture and Art']

    timeout_seconds = C.TIME
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

    @staticmethod
    def before_next_page(player, timeout_happened):
        correct_ans = pop[:, 5]

        ans = [player.field_maybe_none('pop0'),
               player.field_maybe_none('pop1'),
               player.field_maybe_none('pop2'),
               player.field_maybe_none('pop3'),
               player.field_maybe_none('pop4'),
               player.field_maybe_none('pop5'),
               player.field_maybe_none('pop6'),
               player.field_maybe_none('pop7'),
               player.field_maybe_none('pop8'),
               player.field_maybe_none('pop9'),
               player.field_maybe_none('pop10'),
               player.field_maybe_none('pop11'),
               player.field_maybe_none('pop12'),
               player.field_maybe_none('pop13'),
               player.field_maybe_none('pop14'),
               player.field_maybe_none('pop15'),
               player.field_maybe_none('pop16'),
               player.field_maybe_none('pop17'),
               player.field_maybe_none('pop18'),
               player.field_maybe_none('pop19'),
               ]

        check = [ans[i] == correct_ans[i] for i in range(len(ans))]

        player.score = sum(check)
        participant = player.participant
        participant.pop_score = player.score

        participant.pop_questions = pop[:, 0]


class SportsQuiz(Page):
    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return player.round_number == participant.task_rounds['Sports and Video Games']

    timeout_seconds = C.TIME
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

    @staticmethod
    def before_next_page(player, timeout_happened):
        correct_ans = sports[:, 5]

        ans = [player.field_maybe_none('sports0'),
               player.field_maybe_none('sports1'),
               player.field_maybe_none('sports2'),
               player.field_maybe_none('sports3'),
               player.field_maybe_none('sports4'),
               player.field_maybe_none('sports5'),
               player.field_maybe_none('sports6'),
               player.field_maybe_none('sports7'),
               player.field_maybe_none('sports8'),
               player.field_maybe_none('sports9'),
               player.field_maybe_none('sports10'),
               player.field_maybe_none('sports11'),
               player.field_maybe_none('sports12'),
               player.field_maybe_none('sports13'),
               player.field_maybe_none('sports14'),
               player.field_maybe_none('sports15'),
               player.field_maybe_none('sports16'),
               player.field_maybe_none('sports17'),
               player.field_maybe_none('sports18'),
               player.field_maybe_none('sports19'),
               ]

        check = [ans[i] == correct_ans[i] for i in range(len(ans))]

        player.score = sum(check)
        participant = player.participant
        participant.sports_score = player.score

        participant.sports_questions = sports[:, 0]


class ScienceQuiz(Page):
    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return player.round_number == participant.task_rounds['Science and Technology']

    timeout_seconds = C.TIME
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

    @staticmethod
    def before_next_page(player, timeout_happened):
        correct_ans = science[:, 5]

        ans = [player.field_maybe_none('science0'),
               player.field_maybe_none('science1'),
               player.field_maybe_none('science2'),
               player.field_maybe_none('science3'),
               player.field_maybe_none('science4'),
               player.field_maybe_none('science5'),
               player.field_maybe_none('science6'),
               player.field_maybe_none('science7'),
               player.field_maybe_none('science8'),
               player.field_maybe_none('science9'),
               player.field_maybe_none('science10'),
               player.field_maybe_none('science11'),
               player.field_maybe_none('science12'),
               player.field_maybe_none('science13'),
               player.field_maybe_none('science14'),
               player.field_maybe_none('science15'),
               player.field_maybe_none('science16'),
               player.field_maybe_none('science17'),
               player.field_maybe_none('science18'),
               player.field_maybe_none('science19'),
               ]

        check = [ans[i] == correct_ans[i] for i in range(len(ans))]

        player.score = sum(check)
        participant = player.participant
        participant.science_score = player.score

        participant.science_questions = science[:, 0]


class USQuiz(Page):
    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return player.round_number == participant.task_rounds['US Geography']

    timeout_seconds = C.TIME
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

    @staticmethod
    def before_next_page(player, timeout_happened):
        correct_ans = us[:, 5]

        ans = [player.field_maybe_none('us0'),
               player.field_maybe_none('us1'),
               player.field_maybe_none('us2'),
               player.field_maybe_none('us3'),
               player.field_maybe_none('us4'),
               player.field_maybe_none('us5'),
               player.field_maybe_none('us6'),
               player.field_maybe_none('us7'),
               player.field_maybe_none('us8'),
               player.field_maybe_none('us9'),
               player.field_maybe_none('us10'),
               player.field_maybe_none('us11'),
               player.field_maybe_none('us12'),
               player.field_maybe_none('us13'),
               player.field_maybe_none('us14'),
               player.field_maybe_none('us15'),
               player.field_maybe_none('us16'),
               player.field_maybe_none('us17'),
               player.field_maybe_none('us18'),
               player.field_maybe_none('us19'),
               ]

        check = [ans[i] == correct_ans[i] for i in range(len(ans))]

        player.score = sum(check)
        participant = player.participant
        participant.us_score = player.score

        participant.us_questions = us[:, 0]


class Transition(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

    @staticmethod
    def vars_for_template(player):
        participant = player.participant
        random_round = random.randint(1, C.NUM_ROUNDS)
        player_in_selected_round = player.in_round(random_round)
        player.payoff = player_in_selected_round.score
        participant.part1_score = player_in_selected_round.score
        participant.part1_topic = C.TASKS[random_round - 1]


class ResultsWaitPage(WaitPage):
    pass


page_sequence = [Instructions, Start, VerbalQuiz, MathQuiz, PopQuiz, SportsQuiz, ScienceQuiz, USQuiz, Transition]
