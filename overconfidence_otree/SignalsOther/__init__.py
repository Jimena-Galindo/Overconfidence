from otree.api import *
import numpy as np
import pandas as pd
import random
from pathlib import Path

doc = """
Belief Updating 
"""


class C(BaseConstants):
    NAME_IN_URL = 'GamblesOther'
    PLAYERS_PER_GROUP = None
    TASKS = ['Math', 'Verbal',
             'Science and Technology', 'Sports and Video Games', 'US Geography', 'Pop-Culture and Art']
    # number of effort/signal realizations per quizz
    N = 11
    trials = 10
    # total number of rounds
    NUM_ROUNDS = len(TASKS)*N
    # the matrices for the DGP
    ml = np.array([[.20, .25, .40], [.07, .30, .45], [.02, .20, .50]])
    mm = np.array([[.40, .45, .65], [.30, .65, .69], [.05, .50, .80]])
    mh = np.array([[.45, .55, .75], [.35, .69, .80], [.25, .65, .98]])
    M = [ml, mm, mh]
    SEED = 3452
    T1 = 6
    T2 = 16


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    topic = models.StringField()

    math_belief_self = models.IntegerField(label='',
                                           choices=[[0, 'Between 0 and ' + str(C.T1 - 1)],
                                                    [1, 'Between ' + str(C.T1) + ' and ' + str(C.T2 - 1)],
                                                    [2, str(C.T2) + ' or more']],
                                           widget=widgets.RadioSelectHorizontal)
    verbal_belief_self = models.IntegerField(label='',
                                             choices=[[0, 'Between 0 and ' + str(C.T1 - 1)],
                                                      [1, 'Between ' + str(C.T1) + ' and ' + str(C.T2 - 1)],
                                                      [2, str(C.T2) + ' or more']],
                                             widget=widgets.RadioSelectHorizontal)
    pop_belief_self = models.IntegerField(label='',
                                     choices=[[0, 'Between 0 and ' + str(C.T1 - 1)],
                                              [1, 'Between ' + str(C.T1) + ' and ' + str(C.T2 - 1)],
                                              [2, str(C.T2) + ' or more']],
                                     widget=widgets.RadioSelectHorizontal)
    science_belief_self = models.IntegerField(label='',
                                         choices=[[0, 'Between 0 and ' + str(C.T1 - 1)],
                                                  [1, 'Between ' + str(C.T1) + ' and ' + str(C.T2 - 1)],
                                                  [2, str(C.T2) + ' or more']],
                                         widget=widgets.RadioSelectHorizontal)
    us_belief_self = models.IntegerField(label='',
                                    choices=[[0, 'Between 0 and ' + str(C.T1 - 1)],
                                             [1, 'Between ' + str(C.T1) + ' and ' + str(C.T2 - 1)],
                                             [2, str(C.T2) + ' or more']],
                                    widget=widgets.RadioSelectHorizontal)
    sports_belief_self = models.IntegerField(label='Guess your score',
                                        choices=[[0, 'Between 0 and ' + str(C.T1 - 1)],
                                                 [1, 'Between ' + str(C.T1) + ' and ' + str(C.T2 - 1)],
                                                 [2, str(C.T2) + ' or more']],
                                        widget=widgets.RadioSelectHorizontal)

    math_certainty_self = models.IntegerField(label='How sure are you of your answer?',
                                              choices=[[33, 'It is a random guess'],
                                                       [50, 'There is another choice that is equally likely'],
                                                       [75, 'Somewhat sure'],
                                                       [100, 'Completely sure']])
    verbal_certainty_self = models.IntegerField(label='How sure are you of your answer?',
                                              choices=[[33, 'It is a random guess'],
                                                       [50, 'There is another choice that is equally likely'],
                                                       [75, 'Somewhat sure'],
                                                       [100, 'Completely sure']])
    pop_certainty_self = models.IntegerField(label='how sure are you of your answer?',
                                              choices=[[33, 'It is a random guess'],
                                                       [50, 'There is another choice that is equally likely'],
                                                       [75, 'Somewhat sure'],
                                                       [100, 'Completely sure']])
    science_certainty_self = models.IntegerField(label='how sure are you of your answer?',
                                              choices=[[33, 'It is a random guess'],
                                                       [50, 'There is another choice that is equally likely'],
                                                       [75, 'Somewhat sure'],
                                                       [100, 'Completely sure']])
    us_certainty_self = models.IntegerField(label='how sure are you of your answer?',
                                              choices=[[33, 'It is a random guess'],
                                                       [50, 'There is another choice that is equally likely'],
                                                       [75, 'Somewhat sure'],
                                                       [100, 'Completely sure']])
    sports_certainty_self = models.IntegerField(label='how sure are you of your answer?',
                                              choices=[[33, 'It is a random guess'],
                                                       [50, 'There is another choice that is equally likely'],
                                                       [75, 'Somewhat sure'],
                                                       [100, 'Completely sure']])

    math_belief_other = models.IntegerField(label='',
                                           choices=[[0, 'Between 0 and ' + str(C.T1 - 1)],
                                                    [1, 'Between ' + str(C.T1) + ' and ' + str(C.T2 - 1)],
                                                    [2, str(C.T2) + ' or more']],
                                           widget=widgets.RadioSelectHorizontal)
    verbal_belief_other = models.IntegerField(label='',
                                             choices=[[0, 'Between 0 and ' + str(C.T1 - 1)],
                                                      [1, 'Between ' + str(C.T1) + ' and ' + str(C.T2 - 1)],
                                                      [2, str(C.T2) + ' or more']],
                                             widget=widgets.RadioSelectHorizontal)
    pop_belief_other = models.IntegerField(label='',
                                          choices=[[0, 'Between 0 and ' + str(C.T1 - 1)],
                                                   [1, 'Between ' + str(C.T1) + ' and ' + str(C.T2 - 1)],
                                                   [2, str(C.T2) + ' or more']],
                                          widget=widgets.RadioSelectHorizontal)
    science_belief_other = models.IntegerField(label='',
                                              choices=[[0, 'Between 0 and ' + str(C.T1 - 1)],
                                                       [1, 'Between ' + str(C.T1) + ' and ' + str(C.T2 - 1)],
                                                       [2, str(C.T2) + ' or more']],
                                              widget=widgets.RadioSelectHorizontal)
    us_belief_other = models.IntegerField(label='',
                                         choices=[[0, 'Between 0 and ' + str(C.T1 - 1)],
                                                  [1, 'Between ' + str(C.T1) + ' and ' + str(C.T2 - 1)],
                                                  [2, str(C.T2) + ' or more']],
                                         widget=widgets.RadioSelectHorizontal)
    sports_belief_other = models.IntegerField(label='',
                                             choices=[[0, 'Between 0 and ' + str(C.T1 - 1)],
                                                      [1, 'Between ' + str(C.T1) + ' and ' + str(C.T2 - 1)],
                                                      [2, str(C.T2) + ' or more']],
                                             widget=widgets.RadioSelectHorizontal)

    math_certainty_other = models.IntegerField(min=0, max=100,
                                              label='From 0 to 100 how sure are you of your answer? (100 means you are completely sure and 0 means your answer was a random guess)')
    verbal_certainty_other = models.IntegerField(min=0, max=100,
                                                label='From 0 to 100 how sure are you of your answer? (100 means you are completely sure and 0 means your answer was a random guess)')
    pop_certainty_other = models.IntegerField(min=0, max=100,
                                             label='From 0 to 100 how sure are you of your answer? (100 means you are completely sure and 0 means your answer was a random guess)')
    science_certainty_other = models.IntegerField(min=0, max=100,
                                                 label='From 0 to 100 how sure are you of your answer? (100 means you are completely sure and 0 means your answer was a random guess)')
    us_certainty_other = models.IntegerField(min=0, max=100,
                                            label='From 0 to 100 how sure are you of your answer? (100 means you are completely sure and 0 means your answer was a random guess)')
    sports_certainty_other = models.IntegerField(min=0, max=100,
                                                label='From 0 to 100 how sure are you of your answer? (100 means you are completely sure and 0 means your answer was a random guess)')


    effort = models.IntegerField(label='Choose a gamble',
                                 choices=[[0, 'A'], [1, 'B'], [2, 'C']],
                                 widget=widgets.RadioSelect, )

    signal = models.IntegerField()
    fails = models.IntegerField()

    low_button = models.IntegerField(initial=0)
    mid_button = models.IntegerField(initial=0)
    high_button = models.IntegerField(initial=0)

    last_button = models.IntegerField()

    math_other = models.IntegerField()
    verbal_other = models.IntegerField()
    science_other = models.IntegerField()
    pop_other = models.IntegerField()
    us_other = models.IntegerField()
    sports_other = models.IntegerField()

    gender_other = models.StringField()
    nationality_other = models.StringField()
    

# FUNCTIONS
others = pd.read_csv(Path.cwd().joinpath('Others_data/others.csv'))


# PAGES
class Performance(Page):
    def is_displayed(player: Player):
        return player.round_number == 1

    form_model = 'player'
    form_fields = ['math_belief_self',
                   'us_belief_self',
                   'verbal_belief_self',
                   'science_belief_self',
                   'pop_belief_self',
                   'sports_belief_self',
                   'math_certainty_self',
                   'us_certainty_self',
                   'verbal_certainty_self',
                   'science_certainty_self',
                   'pop_certainty_self',
                   'sports_certainty_self',
                   'math_belief_other',
                   'us_belief_other',
                   'verbal_belief_other',
                   'science_belief_other',
                   'pop_belief_other',
                   'sports_belief_other',
                   'math_certainty_other',
                   'us_certainty_other',
                   'verbal_certainty_other',
                   'science_certainty_other',
                   'pop_certainty_other',
                   'sports_certainty_other'
                   ]

    @staticmethod
    def vars_for_template(player):
        index = random.randint(0, len(others))
        other = others.iloc[index-1]

        player.gender_other = other['participant.gender']
        player.nationality_other = other['participant.nationality']

        player.math_other = other['participant.math_score']
        player.verbal_other = other['participant.verbal_score']
        player.us_other = other['participant.us_score']
        player.pop_other = other['participant.pop_score']
        player.science_other = other['participant.science_score']
        player.sports_other = other['participant.sports_score']

        participant = player.participant

        participant.math_other = other['participant.math_score']
        participant.verbal_other = other['participant.verbal_score']
        participant.us_other = other['participant.us_score']
        participant.pop_other = other['participant.pop_score']
        participant.science_other = other['participant.science_score']
        participant.sports_other = other['participant.sports_score']


        return dict(gender=player.gender_other, nationality=player.nationality_other)

    @staticmethod
    def before_next_page(player, timeout_happened):
        session = player.session
        # set the seed for the session
        random.seed(C.SEED)
        # draw the exogenous parameter for each task. It is 0, 1 or 2.
        # These are the same for all players and are saved at the session level
        # we want them to stay the same across sessions as well which is why a seed was set in advance
        session.w_verbal = random.randint(0, 2)
        session.w_math = random.randint(0, 2)
        session.w_science = random.randint(0, 2)
        session.w_sports = random.randint(0, 2)
        session.w_us = random.randint(0, 2)
        session.w_pop = random.randint(0, 2)


        if player.round_number == 1:

            #### verbal
            session = player.session
            w = session.w_verbal
            m = C.M

            T = C.N

            # Generate the sequences of outcomes that subjects will see
            # true high types
            rng = np.random.default_rng(seed=C.SEED)

            # outcomes after choosing L
            outcome_H_L = rng.binomial(1, m[2][0, w], size=(T, C.trials))
            # outcomes after choosing M
            outcome_H_M = rng.binomial(1, m[2][1, w], size=(T, C.trials))
            # outcomes after choosing H
            outcome_H_H = rng.binomial(1, m[2][2, w], size=(T, C.trials))

            outcomes_H = np.stack((outcome_H_L, outcome_H_M, outcome_H_H))

            # true mid types
            outcome_M_L = rng.binomial(1, m[1][0, w], size=(T, C.trials))
            outcome_M_M = rng.binomial(1, m[1][1, w], size=(T, C.trials))
            outcome_M_H = rng.binomial(1, m[1][2, w], size=(T, C.trials))

            outcomes_M = np.stack((outcome_M_L, outcome_M_M, outcome_M_H))

            # true low types
            outcome_L_L = rng.binomial(1, m[0][0, w], size=(T, C.trials))
            outcome_L_M = rng.binomial(1, m[0][1, w], size=(T, C.trials))
            outcome_L_H = rng.binomial(1, m[0][2, w], size=(T, C.trials))

            outcomes_L = np.stack((outcome_L_L, outcome_L_M, outcome_L_H))

            session.outcomes_verbal = np.stack((outcomes_L, outcomes_M, outcomes_H))

            ###### math
            w = session.w_math
            m = C.M

            T = C.N
            # True high types
            # outcomes after choosing L
            outcome_H_L = rng.binomial(1, m[2][0, w], size=(T, C.trials))
            # outcomes after choosing M
            outcome_H_M = rng.binomial(1, m[2][1, w], size=(T, C.trials))
            # outcomes after choosing H
            outcome_H_H = rng.binomial(1, m[2][2, w], size=(T, C.trials))

            outcomes_H = np.stack((outcome_H_L, outcome_H_M, outcome_H_H))

            # true mid types
            outcome_M_L = rng.binomial(1, m[1][0, w], size=(T, C.trials))
            outcome_M_M = rng.binomial(1, m[1][1, w], size=(T, C.trials))
            outcome_M_H = rng.binomial(1, m[1][2, w], size=(T, C.trials))

            outcomes_M = np.stack((outcome_M_L, outcome_M_M, outcome_M_H))

            # true low types
            outcome_L_L = rng.binomial(1, m[0][0, w], size=(T, C.trials))
            outcome_L_M = rng.binomial(1, m[0][1, w], size=(T, C.trials))
            outcome_L_H = rng.binomial(1, m[0][2, w], size=(T, C.trials))

            outcomes_L = np.stack((outcome_L_L, outcome_L_M, outcome_L_H))

            session.outcomes_math = np.stack((outcomes_L, outcomes_M, outcomes_H))
            ##### sports
            w = session.w_sports
            m = C.M

            T = C.N

            # Generate the sequences of outcomes that subjects will see
            # true high types
            rng = np.random.default_rng(seed=C.SEED)

            # outcomes after choosing L
            outcome_H_L = rng.binomial(1, m[2][0, w], size=(T, C.trials))
            # outcomes after choosing M
            outcome_H_M = rng.binomial(1, m[2][1, w], size=(T, C.trials))
            # outcomes after choosing H
            outcome_H_H = rng.binomial(1, m[2][2, w], size=(T, C.trials))

            outcomes_H = np.stack((outcome_H_L, outcome_H_M, outcome_H_H))

            # true mid types
            outcome_M_L = rng.binomial(1, m[1][0, w], size=(T, C.trials))
            outcome_M_M = rng.binomial(1, m[1][1, w], size=(T, C.trials))
            outcome_M_H = rng.binomial(1, m[1][2, w], size=(T, C.trials))

            outcomes_M = np.stack((outcome_M_L, outcome_M_M, outcome_M_H))

            # true low types
            outcome_L_L = rng.binomial(1, m[0][0, w], size=(T, C.trials))
            outcome_L_M = rng.binomial(1, m[0][1, w], size=(T, C.trials))
            outcome_L_H = rng.binomial(1, m[0][2, w], size=(T, C.trials))

            outcomes_L = np.stack((outcome_L_L, outcome_L_M, outcome_L_H))

            session.outcomes_sports = np.stack((outcomes_L, outcomes_M, outcomes_H))

            ###### science
            w = session.w_science
            m = C.M

            T = C.N

            # Generate the sequences of outcomes that subjects will see
            # true high types
            rng = np.random.default_rng(seed=C.SEED)

            # outcomes after choosing L
            outcome_H_L = rng.binomial(1, m[2][0, w], size=(T, C.trials))
            # outcomes after choosing M
            outcome_H_M = rng.binomial(1, m[2][1, w], size=(T, C.trials))
            # outcomes after choosing H
            outcome_H_H = rng.binomial(1, m[2][2, w], size=(T, C.trials))

            outcomes_H = np.stack((outcome_H_L, outcome_H_M, outcome_H_H))

            # true mid types
            outcome_M_L = rng.binomial(1, m[1][0, w], size=(T, C.trials))
            outcome_M_M = rng.binomial(1, m[1][1, w], size=(T, C.trials))
            outcome_M_H = rng.binomial(1, m[1][2, w], size=(T, C.trials))

            outcomes_M = np.stack((outcome_M_L, outcome_M_M, outcome_M_H))

            # true low types
            outcome_L_L = rng.binomial(1, m[0][0, w], size=(T, C.trials))
            outcome_L_M = rng.binomial(1, m[0][1, w], size=(T, C.trials))
            outcome_L_H = rng.binomial(1, m[0][2, w], size=(T, C.trials))

            outcomes_L = np.stack((outcome_L_L, outcome_L_M, outcome_L_H))

            session.outcomes_science = np.stack((outcomes_L, outcomes_M, outcomes_H))


            ##### pop culture
            w = session.w_pop
            m = C.M

            T = C.N

            # Generate the sequences of outcomes that subjects will see
            # true high types
            rng = np.random.default_rng(seed=C.SEED)

            # outcomes after choosing L
            outcome_H_L = rng.binomial(1, m[2][0, w], size=(T, C.trials))
            # outcomes after choosing M
            outcome_H_M = rng.binomial(1, m[2][1, w], size=(T, C.trials))
            # outcomes after choosing H
            outcome_H_H = rng.binomial(1, m[2][2, w], size=(T, C.trials))

            outcomes_H = np.stack((outcome_H_L, outcome_H_M, outcome_H_H))

            # true mid types
            outcome_M_L = rng.binomial(1, m[1][0, w], size=(T, C.trials))
            outcome_M_M = rng.binomial(1, m[1][1, w], size=(T, C.trials))
            outcome_M_H = rng.binomial(1, m[1][2, w], size=(T, C.trials))

            outcomes_M = np.stack((outcome_M_L, outcome_M_M, outcome_M_H))

            # true low types
            outcome_L_L = rng.binomial(1, m[0][0, w], size=(T, C.trials))
            outcome_L_M = rng.binomial(1, m[0][1, w], size=(T, C.trials))
            outcome_L_H = rng.binomial(1, m[0][2, w], size=(T, C.trials))

            outcomes_L = np.stack((outcome_L_L, outcome_L_M, outcome_L_H))

            session.outcomes_pop = np.stack((outcomes_L, outcomes_M, outcomes_H))


            ###### US Geography
            w = session.w_us
            m = C.M

            T = C.N

            # Generate the sequences of outcomes that subjects will see
            # true high types
            rng = np.random.default_rng(seed=C.SEED)

            # outcomes after choosing L
            outcome_H_L = rng.binomial(1, m[2][0, w], size=(T, C.trials))
            # outcomes after choosing M
            outcome_H_M = rng.binomial(1, m[2][1, w], size=(T, C.trials))
            # outcomes after choosing H
            outcome_H_H = rng.binomial(1, m[2][2, w], size=(T, C.trials))

            outcomes_H = np.stack((outcome_H_L, outcome_H_M, outcome_H_H))

            # true mid types
            outcome_M_L = rng.binomial(1, m[1][0, w], size=(T, C.trials))
            outcome_M_M = rng.binomial(1, m[1][1, w], size=(T, C.trials))
            outcome_M_H = rng.binomial(1, m[1][2, w], size=(T, C.trials))

            outcomes_M = np.stack((outcome_M_L, outcome_M_M, outcome_M_H))

            # true low types
            outcome_L_L = rng.binomial(1, m[0][0, w], size=(T, C.trials))
            outcome_L_M = rng.binomial(1, m[0][1, w], size=(T, C.trials))
            outcome_L_H = rng.binomial(1, m[0][2, w], size=(T, C.trials))

            outcomes_L = np.stack((outcome_L_L, outcome_L_M, outcome_L_H))

            session.outcomes_us = np.stack((outcomes_L, outcomes_M, outcomes_H))


class MyWaitPage(WaitPage):
    title_text = "End of Part 1"
    body_text = "Please wait while others finish Part 1 of the experiment"

    @staticmethod
    def is_displayed(player):
        return player.round_number == 1


class Instructions(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1


class VerbalStart(Page):
    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return player.round_number == (participant.task_rounds['Verbal'] - 1) * C.N + 1

    @staticmethod
    def vars_for_template(player):
        player.topic = 'Verbal'
        belief_self = player.in_round(1).verbal_belief_self
        belief_other = player.in_round(1).verbal_belief_other
        return dict(topic=player.topic, self=belief_self, other=belief_other)


class Verbal(Page):
    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return (participant.task_rounds['Verbal'] - 1) * C.N < player.round_number <= (
            participant.task_rounds['Verbal']) * C.N

    form_model = 'player'
    form_fields = ['effort']

    @staticmethod
    def vars_for_template(player):
        player.topic = 'Verbal'
        participant = player.participant
        succes_L = 0
        succes_M = 0
        succes_H = 0

        fail_L = 0
        fail_M = 0
        fail_H = 0

        if player.round_number > (participant.task_rounds[player.topic] - 1) * C.N + 1:
            previous_rounds = player.in_rounds(1 + (player.participant.task_rounds[player.topic] - 1) * C.N,
                                               player.round_number - 1)
            for p in previous_rounds:
                if p.effort == 0:
                    succes_L += p.signal
                    fail_L += C.trials - p.signal
                elif p.effort == 1:
                    succes_M += p.signal
                    fail_M += C.trials - p.signal
                else:
                    succes_H += p.signal
                    fail_H += C.trials - p.signal
        else:
            previous_rounds = 0

        session = player.session
        w = session.w_verbal

        return dict(rounds=previous_rounds, sH=succes_H, sM=succes_M, sL=succes_L, fH=fail_H, fM=fail_M, fL=fail_L, w=w)

    @staticmethod
    def live_method(player: Player, data):
        if data == 0:
            player.low_button += 1
            player.last_button = 0
        elif data == 1:
            player.mid_button += 1
            player.last_button = 1
        elif data == 2:
            player.high_button += 1
            player.last_button = 2


class VerbalFeedback(Page):
    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return (participant.task_rounds['Verbal'] - 1) * C.N < player.round_number <= (
            participant.task_rounds['Verbal']) * C.N

    @staticmethod
    def vars_for_template(player):
        participant = player.participant
        score = participant.verbal_other
        player.verbal_other = score
        session = player.session
        e = player.effort
        if score < C.T1:
            t = 0
        elif score >= C.T1 & score < C.T2:
            t = 1
        else:
            t = 2

        round = player.round_number - 1 - C.N*player.participant.task_rounds['Verbal']
        signal_realiz = session.outcomes_verbal[t][e, round]
        player.signal = int(sum(signal_realiz))
        player.fails = C.trials - player.signal
        return dict(signal=player.signal,
                    topic=player.topic,
                    fails=player.fails,
                    s1=signal_realiz[0],
                    s2=signal_realiz[1],
                    s3=signal_realiz[2],
                    s4=signal_realiz[3],
                    s5=signal_realiz[4],
                    s6=signal_realiz[5],
                    s7=signal_realiz[6],
                    s8=signal_realiz[7],
                    s9=signal_realiz[8],
                    s10=signal_realiz[9], )


class MathStart(Page):
    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return player.round_number == (participant.task_rounds['Math'] - 1) * C.N + 1

    @staticmethod
    def vars_for_template(player):
        player.topic = 'Math'
        belief_self = player.in_round(1).math_belief_self
        belief_other = player.in_round(1).math_belief_other
        return dict(topic=player.topic, self=belief_self, other=belief_other)


class Math(Page):
    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return (participant.task_rounds['Math'] - 1) * C.N < player.round_number <= (
            participant.task_rounds['Math']) * C.N

    form_model = 'player'
    form_fields = ['effort']

    @staticmethod
    def vars_for_template(player):
        player.topic = 'Math'
        participant = player.participant
        succes_L = 0
        succes_M = 0
        succes_H = 0

        fail_L = 0
        fail_M = 0
        fail_H = 0

        if player.round_number > (participant.task_rounds[player.topic] - 1) * C.N + 1:
            previous_rounds = player.in_rounds(1 + (player.participant.task_rounds[player.topic] - 1) * C.N,
                                               player.round_number - 1)
            for p in previous_rounds:
                if p.effort == 0:
                    succes_L += p.signal
                    fail_L += C.trials - p.signal
                elif p.effort == 1:
                    succes_M += p.signal
                    fail_M += C.trials - p.signal
                else:
                    succes_H += p.signal
                    fail_H += C.trials - p.signal
        else:
            previous_rounds = 0

        session = player.session
        w = session.w_math

        return dict(rounds=previous_rounds, sH=succes_H, sM=succes_M, sL=succes_L, fH=fail_H, fM=fail_M, fL=fail_L, w=w)

    @staticmethod
    def live_method(player: Player, data):
        if data == 0:
            player.low_button += 1
            player.last_button = 0
        elif data == 1:
            player.mid_button += 1
            player.last_button = 1
        elif data == 2:
            player.high_button += 1
            player.last_button = 2


class MathFeedback(Page):
    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return (participant.task_rounds['Math'] - 1) * C.N < player.round_number <= (
            participant.task_rounds['Math']) * C.N

    @staticmethod
    def vars_for_template(player):

        e = player.effort
        session = player.session
        participant = player.participant
        score = participant.math_other
        player.math_other = score

        if score < C.T1:
            t = 0
        elif score >= C.T1 & score < C.T2:
            t = 1
        else:
            t = 2

        round = player.round_number - 1 - C.N*participant.task_rounds['Math']
        signal_realiz = session.outcomes_math[t][e, round]
        player.signal = int(sum(signal_realiz))
        player.fails = C.trials - player.signal
        return dict(signal=player.signal,
                    topic=player.topic,
                    fails=player.fails,
                    s1=signal_realiz[0],
                    s2=signal_realiz[1],
                    s3=signal_realiz[2],
                    s4=signal_realiz[3],
                    s5=signal_realiz[4],
                    s6=signal_realiz[5],
                    s7=signal_realiz[6],
                    s8=signal_realiz[7],
                    s9=signal_realiz[8],
                    s10=signal_realiz[9], )


class PopStart(Page):
    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return player.round_number == (participant.task_rounds['Pop-Culture and Art'] - 1) * C.N + 1

    @staticmethod
    def vars_for_template(player):
        player.topic = 'Pop-Culture and Art'
        belief_self = player.in_round(1).pop_belief_self
        belief_other = player.in_round(1).pop_belief_other
        return dict(topic=player.topic, self=belief_self, other=belief_other)


class Pop(Page):
    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return (participant.task_rounds['Pop-Culture and Art'] - 1) * C.N < player.round_number <= (
            participant.task_rounds['Pop-Culture and Art']) * C.N

    form_model = 'player'
    form_fields = ['effort']

    @staticmethod
    def vars_for_template(player):
        player.topic = 'Pop-Culture and Art'
        participant = player.participant
        succes_L = 0
        succes_M = 0
        succes_H = 0

        fail_L = 0
        fail_M = 0
        fail_H = 0

        if player.round_number > (participant.task_rounds[player.topic] - 1) * C.N + 1:
            previous_rounds = player.in_rounds(1 + (player.participant.task_rounds[player.topic] - 1) * C.N,
                                               player.round_number - 1)
            for p in previous_rounds:
                if p.effort == 0:
                    succes_L += p.signal
                    fail_L += C.trials - p.signal
                elif p.effort == 1:
                    succes_M += p.signal
                    fail_M += C.trials - p.signal
                else:
                    succes_H += p.signal
                    fail_H += C.trials - p.signal
        else:
            previous_rounds = 0

        session = player.session
        w = session.w_pop

        return dict(rounds=previous_rounds, sH=succes_H, sM=succes_M, sL=succes_L, fH=fail_H, fM=fail_M, fL=fail_L, w=w)

    @staticmethod
    def live_method(player: Player, data):
        if data == 0:
            player.low_button += 1
            player.last_button = 0
        elif data == 1:
            player.mid_button += 1
            player.last_button = 1
        elif data == 2:
            player.high_button += 1
            player.last_button = 2


class PopFeedback(Page):
    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return (participant.task_rounds['Pop-Culture and Art'] - 1) * C.N < player.round_number <= (
            participant.task_rounds['Pop-Culture and Art']) * C.N

    @staticmethod
    def vars_for_template(player):

        session = player.session
        participant = player.participant
        score = participant.pop_other
        player.pop_other = score
        e = player.effort
        if score < C.T1:
            t = 0
        elif score >= C.T1 & score < C.T2:
            t = 1
        else:
            t = 2

        round = player.round_number - 1 - C.N*participant.task_rounds['Pop-Culture and Art']
        signal_realiz = session.outcomes_pop[t][e, round]
        player.signal = int(sum(signal_realiz))
        player.fails = C.trials - player.signal
        return dict(signal=player.signal,
                    topic=player.topic,
                    fails=player.fails,
                    s1=signal_realiz[0],
                    s2=signal_realiz[1],
                    s3=signal_realiz[2],
                    s4=signal_realiz[3],
                    s5=signal_realiz[4],
                    s6=signal_realiz[5],
                    s7=signal_realiz[6],
                    s8=signal_realiz[7],
                    s9=signal_realiz[8],
                    s10=signal_realiz[9], )


class ScienceStart(Page):
    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return player.round_number == (participant.task_rounds['Science and Technology'] - 1) * C.N + 1

    @staticmethod
    def vars_for_template(player):
        player.topic = 'Science and Technology'
        belief_self = player.in_round(1).science_belief_self
        belief_other = player.in_round(1).science_belief_other
        return dict(topic=player.topic, self=belief_self, other=belief_other)


class Science(Page):
    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return (participant.task_rounds['Science and Technology'] - 1) * C.N < player.round_number <= (
            participant.task_rounds['Science and Technology']) * C.N

    form_model = 'player'
    form_fields = ['effort']

    @staticmethod
    def vars_for_template(player):
        player.topic = 'Science and Technology'
        participant = player.participant
        succes_L = 0
        succes_M = 0
        succes_H = 0

        fail_L = 0
        fail_M = 0
        fail_H = 0

        if player.round_number > (participant.task_rounds[player.topic] - 1) * C.N + 1:
            previous_rounds = player.in_rounds(1 + (player.participant.task_rounds[player.topic] - 1) * C.N,
                                               player.round_number - 1)
            for p in previous_rounds:
                if p.effort == 0:
                    succes_L += p.signal
                    fail_L += C.trials - p.signal
                elif p.effort == 1:
                    succes_M += p.signal
                    fail_M += C.trials - p.signal
                else:
                    succes_H += p.signal
                    fail_H += C.trials - p.signal
        else:
            previous_rounds = 0

        session = player.session
        w = session.w_science

        return dict(rounds=previous_rounds, sH=succes_H, sM=succes_M, sL=succes_L, fH=fail_H, fM=fail_M, fL=fail_L, w=w)

    @staticmethod
    def live_method(player: Player, data):
        if data == 0:
            player.low_button += 1
            player.last_button = 0
        elif data == 1:
            player.mid_button += 1
            player.last_button = 1
        elif data == 2:
            player.high_button += 1
            player.last_button = 2


class ScienceFeedback(Page):
    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return (participant.task_rounds['Science and Technology'] - 1) * C.N < player.round_number <= (
            participant.task_rounds['Science and Technology']) * C.N

    @staticmethod
    def vars_for_template(player):
        participant = player.participant
        score = participant.science_other
        player.science_other = score
        session = player.session
        e = player.effort
        if score < C.T1:
            t = 0
        elif score >= C.T1 & score < C.T2:
            t = 1
        else:
            t = 2

        round = player.round_number - 1 - C.N*participant.task_rounds['Science and Technology']
        signal_realiz = session.outcomes_science[t][e, round]
        player.signal = int(sum(signal_realiz))
        player.fails = C.trials - player.signal
        return dict(signal=player.signal,
                    topic=player.topic,
                    fails=player.fails,
                    s1=signal_realiz[0],
                    s2=signal_realiz[1],
                    s3=signal_realiz[2],
                    s4=signal_realiz[3],
                    s5=signal_realiz[4],
                    s6=signal_realiz[5],
                    s7=signal_realiz[6],
                    s8=signal_realiz[7],
                    s9=signal_realiz[8],
                    s10=signal_realiz[9], )


class SportsStart(Page):
    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return player.round_number == (participant.task_rounds['Sports and Video Games'] - 1) * C.N + 1

    @staticmethod
    def vars_for_template(player):
        player.topic = 'Sports and Video Games'
        belief_self = player.in_round(1).sports_belief_self
        belief_other = player.in_round(1).sports_belief_other
        return dict(topic=player.topic, self=belief_self, other=belief_other)


class Sports(Page):
    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return (participant.task_rounds['Sports and Video Games'] - 1) * C.N < player.round_number <= (
            participant.task_rounds['Sports and Video Games']) * C.N

    form_model = 'player'
    form_fields = ['effort']

    @staticmethod
    def vars_for_template(player):
        player.topic = 'Sports and Video Games'
        participant = player.participant
        succes_L = 0
        succes_M = 0
        succes_H = 0

        fail_L = 0
        fail_M = 0
        fail_H = 0

        if player.round_number > (participant.task_rounds[player.topic] - 1) * C.N + 1:
            previous_rounds = player.in_rounds(1 + (player.participant.task_rounds[player.topic] - 1) * C.N,
                                               player.round_number - 1)
            for p in previous_rounds:
                if p.effort == 0:
                    succes_L += p.signal
                    fail_L += C.trials - p.signal
                elif p.effort == 1:
                    succes_M += p.signal
                    fail_M += C.trials - p.signal
                else:
                    succes_H += p.signal
                    fail_H += C.trials - p.signal
        else:
            previous_rounds = 0

        session = player.session
        w = session.w_sports

        return dict(rounds=previous_rounds, sH=succes_H, sM=succes_M, sL=succes_L, fH=fail_H, fM=fail_M, fL=fail_L, w=w)

    @staticmethod
    def live_method(player: Player, data):
        if data == 0:
            player.low_button += 1
            player.last_button = 0
        elif data == 1:
            player.mid_button += 1
            player.last_button = 1
        elif data == 2:
            player.high_button += 1
            player.last_button = 2


class SportsFeedback(Page):
    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return (participant.task_rounds['Sports and Video Games'] - 1) * C.N < player.round_number <= (
                   participant.task_rounds['Sports and Video Games']) * C.N

    @staticmethod
    def vars_for_template(player):
        participant = player.participant
        score = participant.sports_other
        player.sports_other = score
        session = player.session

        e = player.effort
        if score < C.T1:
            t = 0
        elif score >= C.T1 & score < C.T2:
            t = 1
        else:
            t = 2

        round = player.round_number - 1 - C.N*participant.task_rounds['Sports and Video Games']
        signal_realiz = session.outcomes_sports[t][e, round]
        player.signal = int(sum(signal_realiz))
        player.fails = C.trials - player.signal
        return dict(signal=player.signal,
                    topic=player.topic,
                    fails=player.fails,
                    s1=signal_realiz[0],
                    s2=signal_realiz[1],
                    s3=signal_realiz[2],
                    s4=signal_realiz[3],
                    s5=signal_realiz[4],
                    s6=signal_realiz[5],
                    s7=signal_realiz[6],
                    s8=signal_realiz[7],
                    s9=signal_realiz[8],
                    s10=signal_realiz[9], )


class UsStart(Page):
    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return player.round_number == (participant.task_rounds['US Geography'] - 1) * C.N + 1

    @staticmethod
    def vars_for_template(player):
        player.topic = 'US Geography'
        belief_self = player.in_round(1).us_belief_self
        belief_other = player.in_round(1).us_belief_other
        return dict(topic=player.topic, self=belief_self, other=belief_other)


class Us(Page):
    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return (participant.task_rounds['US Geography'] - 1) * C.N < player.round_number <= (
                   participant.task_rounds['US Geography']) * C.N

    form_model = 'player'
    form_fields = ['effort']

    @staticmethod
    def vars_for_template(player):
        player.topic = 'US Geography'
        participant = player.participant
        succes_L = 0
        succes_M = 0
        succes_H = 0

        fail_L = 0
        fail_M = 0
        fail_H = 0

        if player.round_number > (participant.task_rounds[player.topic] - 1) * C.N + 1:
            previous_rounds = player.in_rounds(1 + (player.participant.task_rounds[player.topic] - 1) * C.N,
                                               player.round_number - 1)
            for p in previous_rounds:
                if p.effort == 0:
                    succes_L += p.signal
                    fail_L += C.trials - p.signal
                elif p.effort == 1:
                    succes_M += p.signal
                    fail_M += C.trials - p.signal
                else:
                    succes_H += p.signal
                    fail_H += C.trials - p.signal
        else:
            previous_rounds = 0

        session = player.session
        w = session.w_us

        return dict(rounds=previous_rounds, sH=succes_H, sM=succes_M, sL=succes_L, fH=fail_H, fM=fail_M, fL=fail_L, w=w)

    @staticmethod
    def live_method(player: Player, data):
        if data == 0:
            player.low_button += 1
            player.last_button = 0
        elif data == 1:
            player.mid_button += 1
            player.last_button = 1
        elif data == 2:
            player.high_button += 1
            player.last_button = 2


class UsFeedback(Page):
    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return (participant.task_rounds['US Geography'] - 1) * C.N < player.round_number <= (
                   participant.task_rounds['US Geography']) * C.N

    @staticmethod
    def vars_for_template(player):

        session = player.session
        participant = player.participant
        score = participant.us_other
        player.us_other = score
        e = player.effort
        if score < C.T1:
            t = 0
        elif score >= C.T1 & score < C.T2:
            t = 1
        else:
            t = 2

        round = player.round_number - 1 - C.N*participant.task_rounds['US Geography']
        signal_realiz = session.outcomes_us[t][e, round]
        player.signal = int(sum(signal_realiz))
        player.fails = C.trials - player.signal
        return dict(signal=player.signal,
                    topic=player.topic,
                    fails=player.fails,
                    s1=signal_realiz[0],
                    s2=signal_realiz[1],
                    s3=signal_realiz[2],
                    s4=signal_realiz[3],
                    s5=signal_realiz[4],
                    s6=signal_realiz[5],
                    s7=signal_realiz[6],
                    s8=signal_realiz[7],
                    s9=signal_realiz[8],
                    s10=signal_realiz[9], )


class Load(Page):
    timeout_seconds = 2

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

    @staticmethod
    def before_next_page(player, timeout_happened):
        participant = player.participant
        random_round = random.randint(1, len(C.TASKS))
        task = C.TASKS[random_round - 1]

        in_task_rounds = player.in_rounds((random_round - 1) * C.N, (
            random_round) * C.N)

        score = 0
        for p in in_task_rounds:
            score += p.signal

        player.payoff = score

        participant.part2_topic = task
        participant.part2_score = score


class ResultsWaitPage(WaitPage):
    pass


page_sequence = [Performance, MyWaitPage, Instructions,
                 VerbalStart, Verbal, VerbalFeedback,
                 MathStart, Math, MathFeedback,
                 PopStart, Pop, PopFeedback,
                 ScienceStart, Science, ScienceFeedback,
                 SportsStart, Sports, SportsFeedback,
                 UsStart, Us, UsFeedback, Load]
