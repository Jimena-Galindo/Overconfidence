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
    PLAYERS_PER_GROUP = 2
    TASKS = ['Math', 'Verbal', 'Science and Technology', 'Sports and Video Games', 'US Geography', 'Pop-Culture and Art']
    # number of effort/signal realizations per quizz
    N = 5
    # total number of rounds
    NUM_ROUNDS = len(TASKS)*N
    # the matrices for the DGP
    ml = np.array([[.20, .25, .40], [.07, .30, .45], [.02, .20, .50]])
    mm = np.array([[.40, .45, .65], [.30, .65, .69], [.05, .50, .80]])
    mh = np.array([[.45, .55, .75], [.35, .69, .80], [.25, .65, .98]])
    M = [ml, mm, mh]
    SEED = 3821
    T1 = 10
    T2 = 15


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    topic = models.StringField()

    math_belief = models.IntegerField()
    verbal_belief = models.IntegerField()
    pop_belief = models.IntegerField()
    science_belief = models.IntegerField()
    us_belief = models.IntegerField()
    sports_belief = models.IntegerField()

    math_pt_belief = models.IntegerField(min=0, label='Math')
    verbal_pt_belief = models.IntegerField(min=0, label='Verbal Reasoning')
    pop_pt_belief = models.IntegerField(min=0, label='Pop-Culture and Art')
    science_pt_belief = models.IntegerField(min=0, label='Science and Technology')
    us_pt_belief = models.IntegerField(min=0, label='US Geography')
    sports_pt_belief = models.IntegerField(min=0, label='Sports and Video-games')

    math_belief_self = models.IntegerField(min=0, label='Math')
    verbal_belief_self = models.IntegerField(min=0, label='Verbal Reasoning')
    pop_belief_self = models.IntegerField(min=0, label='Pop-Culture and Art')
    science_belief_self = models.IntegerField(min=0, label='Science and Technology')
    us_belief_self = models.IntegerField(min=0, label='US Geography')
    sports_belief_self = models.IntegerField(min=0, label='Sports and Video-games')

    effort = models.IntegerField(label='Choose a gamble',
                                 choices=[[0, 'A'], [1, 'B'], [2, 'C']],
                                 widget=widgets.RadioSelect, )

    signal = models.IntegerField()

    low_button = models.IntegerField(initial=0)
    mid_button = models.IntegerField(initial=0)
    high_button = models.IntegerField(initial=0)

    last_button = models.IntegerField()
    

# FUNCTIONS
def creating_session(subsession):
    subsession.group_randomly()

# PAGES
class Performance(Page):
    def is_displayed(player: Player):
        return player.round_number == 1

    form_model = 'player'
    form_fields = ['math_pt_belief',
                   'us_pt_belief',
                   'verbal_pt_belief',
                   'science_pt_belief',
                   'pop_pt_belief',
                   'sports_pt_belief',
                   'math_belief_self',
                   'us_belief_self',
                   'verbal_belief_self',
                   'science_belief_self',
                   'pop_belief_self',
                   'sports_belief_self'
                   ]

    @staticmethod
    def vars_for_template(player):
        other = player.get_others_in_group()
        other = other[0].participant
        gender = other.gender
        major = other.major
        nationality = other.nationality

        me = player.participant
        gender_self = me.gender
        major_self = me.major
        nationality_self = me.nationality

        return dict(gender=gender, major=major, nationality=nationality,
                    gender_self=gender_self, major_self=major_self, nationality_self=nationality_self)

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
        session.w_pop = random.randint(0, 2)
        session.w_us = random.randint(0, 2)

        if player.round_number == 1:
            session = player.session
            w = session.w_verbal
            m = C.M

            T = C.N

            # Generate the sequences of outcomes that subjects will see
            # true high types
            rng = np.random.default_rng(seed=C.SEED)

            # outcomes after choosing L
            outcome_H_L = rng.binomial(1, m[2][0, w], size=T)
            # outcomes after choosing M
            outcome_H_M = rng.binomial(1, m[2][1, w], size=T)
            # outcomes after choosing H
            outcome_H_H = rng.binomial(1, m[2][2, w], size=T)

            outcomes_H = np.stack((outcome_H_L, outcome_H_M, outcome_H_H))

            # true mid types
            outcome_M_H = rng.binomial(1, m[1][0, w], size=T)
            outcome_M_M = rng.binomial(1, m[1][1, w], size=T)
            outcome_M_L = rng.binomial(1, m[1][2, w], size=T)

            outcomes_M = np.stack((outcome_M_L, outcome_M_M, outcome_M_H))

            # true low types
            outcome_L_H = rng.binomial(1, m[0][0, w], size=T)
            outcome_L_M = rng.binomial(1, m[0][1, w], size=T)
            outcome_L_L = rng.binomial(1, m[0][2, w], size=T)

            outcomes_L = np.stack((outcome_L_L, outcome_L_M, outcome_L_H))

            session.outcomes_verbal = np.stack((outcomes_L, outcomes_M, outcomes_H))

            w = session.w_math
            m = C.M

            T = C.N

            # outcomes after choosing L
            outcome_H_L = rng.binomial(1, m[2][0, w], size=T)
            # outcomes after choosing M
            outcome_H_M = rng.binomial(1, m[2][1, w], size=T)
            # outcomes after choosing H
            outcome_H_H = rng.binomial(1, m[2][2, w], size=T)

            outcomes_H = np.stack((outcome_H_L, outcome_H_M, outcome_H_H))

            # true mid types
            outcome_M_H = rng.binomial(1, m[1][0, w], size=T)
            outcome_M_M = rng.binomial(1, m[1][1, w], size=T)
            outcome_M_L = rng.binomial(1, m[1][2, w], size=T)

            outcomes_M = np.stack((outcome_M_L, outcome_M_M, outcome_M_H))

            # true low types
            outcome_L_H = rng.binomial(1, m[0][0, w], size=T)
            outcome_L_M = rng.binomial(1, m[0][1, w], size=T)
            outcome_L_L = rng.binomial(1, m[0][2, w], size=T)

            outcomes_L = np.stack((outcome_L_L, outcome_L_M, outcome_L_H))

            session.outcomes_math = np.stack((outcomes_L, outcomes_M, outcomes_H))

            w = session.w_sports
            m = C.M

            T = C.N

            # Generate the sequences of outcomes that subjects will see
            # true high types
            rng = np.random.default_rng(seed=C.SEED)

            # outcomes after choosing L
            outcome_H_L = rng.binomial(1, m[2][0, w], size=T)
            # outcomes after choosing M
            outcome_H_M = rng.binomial(1, m[2][1, w], size=T)
            # outcomes after choosing H
            outcome_H_H = rng.binomial(1, m[2][2, w], size=T)

            outcomes_H = np.stack((outcome_H_L, outcome_H_M, outcome_H_H))

            # true mid types
            outcome_M_H = rng.binomial(1, m[1][0, w], size=T)
            outcome_M_M = rng.binomial(1, m[1][1, w], size=T)
            outcome_M_L = rng.binomial(1, m[1][2, w], size=T)

            outcomes_M = np.stack((outcome_M_L, outcome_M_M, outcome_M_H))

            # true low types
            outcome_L_H = rng.binomial(1, m[0][0, w], size=T)
            outcome_L_M = rng.binomial(1, m[0][1, w], size=T)
            outcome_L_L = rng.binomial(1, m[0][2, w], size=T)

            outcomes_L = np.stack((outcome_L_L, outcome_L_M, outcome_L_H))

            session.outcomes_sports = np.stack((outcomes_L, outcomes_M, outcomes_H))

            w = session.w_science
            m = C.M

            T = C.N

            # Generate the sequences of outcomes that subjects will see
            # true high types
            rng = np.random.default_rng(seed=C.SEED)

            # outcomes after choosing L
            outcome_H_L = rng.binomial(1, m[2][0, w], size=T)
            # outcomes after choosing M
            outcome_H_M = rng.binomial(1, m[2][1, w], size=T)
            # outcomes after choosing H
            outcome_H_H = rng.binomial(1, m[2][2, w], size=T)

            outcomes_H = np.stack((outcome_H_L, outcome_H_M, outcome_H_H))

            # true mid types
            outcome_M_H = rng.binomial(1, m[1][0, w], size=T)
            outcome_M_M = rng.binomial(1, m[1][1, w], size=T)
            outcome_M_L = rng.binomial(1, m[1][2, w], size=T)

            outcomes_M = np.stack((outcome_M_L, outcome_M_M, outcome_M_H))

            # true low types
            outcome_L_H = rng.binomial(1, m[0][0, w], size=T)
            outcome_L_M = rng.binomial(1, m[0][1, w], size=T)
            outcome_L_L = rng.binomial(1, m[0][2, w], size=T)

            outcomes_L = np.stack((outcome_L_L, outcome_L_M, outcome_L_H))

            session.outcomes_science = np.stack((outcomes_L, outcomes_M, outcomes_H))

            w = session.w_pop
            m = C.M

            T = C.N

            # Generate the sequences of outcomes that subjects will see
            # true high types
            rng = np.random.default_rng(seed=C.SEED)

            # outcomes after choosing L
            outcome_H_L = rng.binomial(1, m[2][0, w], size=T)
            # outcomes after choosing M
            outcome_H_M = rng.binomial(1, m[2][1, w], size=T)
            # outcomes after choosing H
            outcome_H_H = rng.binomial(1, m[2][2, w], size=T)

            outcomes_H = np.stack((outcome_H_L, outcome_H_M, outcome_H_H))

            # true mid types
            outcome_M_H = rng.binomial(1, m[1][0, w], size=T)
            outcome_M_M = rng.binomial(1, m[1][1, w], size=T)
            outcome_M_L = rng.binomial(1, m[1][2, w], size=T)

            outcomes_M = np.stack((outcome_M_L, outcome_M_M, outcome_M_H))

            # true low types
            outcome_L_H = rng.binomial(1, m[0][0, w], size=T)
            outcome_L_M = rng.binomial(1, m[0][1, w], size=T)
            outcome_L_L = rng.binomial(1, m[0][2, w], size=T)

            outcomes_L = np.stack((outcome_L_L, outcome_L_M, outcome_L_H))

            session.outcomes_pop = np.stack((outcomes_L, outcomes_M, outcomes_H))

            w = session.w_us
            m = C.M

            T = C.N

            # Generate the sequences of outcomes that subjects will see
            # true high types
            rng = np.random.default_rng(seed=C.SEED)

            # outcomes after choosing L
            outcome_H_L = rng.binomial(1, m[2][0, w], size=T)
            # outcomes after choosing M
            outcome_H_M = rng.binomial(1, m[2][1, w], size=T)
            # outcomes after choosing H
            outcome_H_H = rng.binomial(1, m[2][2, w], size=T)

            outcomes_H = np.stack((outcome_H_L, outcome_H_M, outcome_H_H))

            # true mid types
            outcome_M_H = rng.binomial(1, m[1][0, w], size=T)
            outcome_M_M = rng.binomial(1, m[1][1, w], size=T)
            outcome_M_L = rng.binomial(1, m[1][2, w], size=T)

            outcomes_M = np.stack((outcome_M_L, outcome_M_M, outcome_M_H))

            # true low types
            outcome_L_H = rng.binomial(1, m[0][0, w], size=T)
            outcome_L_M = rng.binomial(1, m[0][1, w], size=T)
            outcome_L_L = rng.binomial(1, m[0][2, w], size=T)

            outcomes_L = np.stack((outcome_L_L, outcome_L_M, outcome_L_H))

            session.outcomes_us = np.stack((outcomes_L, outcomes_M, outcomes_H))

            if player.math_pt_belief <= C.T1:
                player.math_belief = 0
            elif C.T1 < player.math_pt_belief <= C.T2:
                player.math_belief = 1
            elif player.math_pt_belief > C.T2:
                player.math_belief = 2

            if player.verbal_pt_belief <= C.T1:
                player.verbal_belief = 0
            elif C.T1 < player.verbal_pt_belief <= C.T2:
                player.verbal_belief = 1
            elif player.verbal_pt_belief > C.T2:
                player.verbal_belief = 2

            if player.pop_pt_belief <= C.T1:
                player.pop_belief = 0
            elif C.T1 < player.pop_pt_belief <= C.T2:
                player.pop_belief = 1
            elif player.pop_pt_belief > C.T2:
                player.pop_belief = 2

            if player.us_pt_belief <= C.T1:
                player.us_belief = 0
            elif C.T1 < player.us_pt_belief <= C.T2:
                player.us_belief = 1
            elif player.us_pt_belief > C.T2:
                player.us_belief = 2

            if player.science_pt_belief <= C.T1:
                player.science_belief = 0
            elif C.T1 < player.science_pt_belief <= C.T2:
                player.science_belief = 1
            elif player.science_pt_belief > C.T2:
                player.science_belief = 2

            if player.sports_pt_belief <= C.T1:
                player.sports_belief = 0
            elif C.T1 < player.sports_pt_belief <= C.T2:
                player.sports_belief = 1
            elif player.sports_pt_belief > C.T2:
                player.sports_belief = 2


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
        belief = player.in_round(1).verbal_belief
        point_belief = player.in_round(1).verbal_pt_belief
        return dict(topic=player.topic, belief=belief, point=point_belief)


class Verbal(Page):
    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return player.round_number > (participant.task_rounds['Verbal'] - 1) * C.N and player.round_number <= (participant.task_rounds['Verbal']) * C.N

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

        if player.round_number > (participant.task_rounds[player.topic]-1)*C.N+1:
            previous_rounds = player.in_rounds(1+(player.participant.task_rounds[player.topic]-1)*C.N, player.round_number-1)
            for p in previous_rounds:
                if p.signal == 1 and p.effort == 0:
                    succes_L += 1
                elif p.signal == 1 and p.effort == 1:
                    succes_M += 1
                elif p.signal == 1 and p.effort == 2:
                    succes_H += 1
                elif p.signal == 0 and p.effort == 0:
                    fail_L += 1
                elif p.signal == 0 and p.effort == 1:
                    fail_M += 1
                else:
                    fail_H += 1

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
        return player.round_number > (participant.task_rounds['Verbal'] - 1) * C.N and player.round_number <= (participant.task_rounds['Verbal']) * C.N

    @staticmethod
    def vars_for_template(player):
        other = player.get_others_in_group()[0]
        other = other.participant
        score = other.verbal_score
        session = player.session
        e = player.effort
        if score < C.T1:
            type = 0
        elif score >= C.T1 & score < C.T2:
            type = 1
        else:
            type = 2

        round = player.round_number - 1 - C.N*player.participant.task_rounds['Verbal']
        player.signal = int(session.outcomes_verbal[type][e, round])

        return dict(signal=player.signal, topic=player.topic)


class MathStart(Page):
    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return player.round_number == (participant.task_rounds['Math'] - 1) * C.N + 1

    @staticmethod
    def vars_for_template(player):
        player.topic = 'Math'
        belief = player.in_round(1).math_belief
        point_belief = player.in_round(1).math_pt_belief
        return dict(topic=player.topic, belief=belief, point=point_belief)


class Math(Page):
    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return player.round_number > (participant.task_rounds['Math'] - 1) * C.N and player.round_number <= (
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
                if p.signal == 1 and p.effort == 0:
                    succes_L += 1
                elif p.signal == 1 and p.effort == 1:
                    succes_M += 1
                elif p.signal == 1 and p.effort == 2:
                    succes_H += 1
                elif p.signal == 0 and p.effort == 0:
                    fail_L += 1
                elif p.signal == 0 and p.effort == 1:
                    fail_M += 1
                else:
                    fail_H += 1
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
        return player.round_number > (participant.task_rounds['Math'] - 1) * C.N and player.round_number <= (
            participant.task_rounds['Math']) * C.N

    @staticmethod
    def vars_for_template(player):
        other = player.get_others_in_group()[0]
        other = other.participant
        score = other.verbal_score
        e = player.effort
        session = player.session

        if score < C.T1:
            type = 0
        elif score >= C.T1 & score < C.T2:
            type = 1
        else:
            type = 2

        round = player.round_number - 1 - C.N*participant.task_rounds['Math']

        player.signal = int(session.outcomes_math[type][e, round])
        return dict(signal=player.signal, topic=player.topic)


class PopStart(Page):
    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return player.round_number == (participant.task_rounds['Pop-Culture and Art'] - 1) * C.N + 1

    @staticmethod
    def vars_for_template(player):
        player.topic = 'Pop-Culture and Art'
        belief = player.in_round(1).pop_belief
        point_belief = player.in_round(1).pop_pt_belief
        return dict(topic=player.topic, belief=belief, point=point_belief)


class Pop(Page):
    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return player.round_number > (participant.task_rounds['Pop-Culture and Art'] - 1) * C.N and player.round_number <= (participant.task_rounds['Pop-Culture and Art']) * C.N

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
                if p.signal == 1 and p.effort == 0:
                    succes_L += 1
                elif p.signal == 1 and p.effort == 1:
                    succes_M += 1
                elif p.signal == 1 and p.effort == 2:
                    succes_H += 1
                elif p.signal == 0 and p.effort == 0:
                    fail_L += 1
                elif p.signal == 0 and p.effort == 1:
                    fail_M += 1
                else:
                    fail_H += 1
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
        return player.round_number > (participant.task_rounds['Pop-Culture and Art'] - 1) * C.N and player.round_number <= (
            participant.task_rounds['Pop-Culture and Art']) * C.N

    @staticmethod
    def vars_for_template(player):
        other = player.get_others_in_group()[0]
        other = other.participant
        score = other.verbal_score
        session = player.session
        e = player.effort
        if score < C.T1:
            type = 0
        elif score >= C.T1 & score < C.T2:
            type = 1
        else:
            type = 2

        round = player.round_number - 1 - C.N*participant.task_rounds['Pop-Culture and Art']
        player.signal = int(session.outcomes_pop[type][e, round])
        return dict(signal=player.signal, topic=player.topic)


class ScienceStart(Page):
    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return player.round_number == (participant.task_rounds['Science and Technology'] - 1) * C.N + 1

    @staticmethod
    def vars_for_template(player):
        player.topic = 'Science and Technology'
        belief = player.in_round(1).science_belief
        point_belief = player.in_round(1).science_pt_belief
        return dict(topic=player.topic, belief=belief, point=point_belief)


class Science(Page):
    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return player.round_number > (participant.task_rounds['Science and Technology'] - 1) * C.N and player.round_number <= (
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
                if p.signal == 1 and p.effort == 0:
                    succes_L += 1
                elif p.signal == 1 and p.effort == 1:
                    succes_M += 1
                elif p.signal == 1 and p.effort == 2:
                    succes_H += 1
                elif p.signal == 0 and p.effort == 0:
                    fail_L += 1
                elif p.signal == 0 and p.effort == 1:
                    fail_M += 1
                else:
                    fail_H += 1
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
        return player.round_number > (participant.task_rounds['Science and Technology'] - 1) * C.N and player.round_number <= (
            participant.task_rounds['Science and Technology']) * C.N

    @staticmethod
    def vars_for_template(player):
        other = player.get_others_in_group()[0]
        other = other.participant
        score = other.verbal_score
        session = player.session
        e = player.effort
        if score < C.T1:
            type = 0
        elif score >= C.T1 & score < C.T2:
            type = 1
        else:
            type = 2

        round = player.round_number - 1 - C.N*participant.task_rounds['Science and Technology']
        player.signal = int(session.outcomes_science[type][e, round])
        return dict(signal=player.signal, topic=player.topic)


class SportsStart(Page):
    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return player.round_number == (participant.task_rounds['Sports and Video Games'] - 1) * C.N + 1

    @staticmethod
    def vars_for_template(player):
        player.topic = 'Sports and Video Games'
        belief = player.in_round(1).sports_belief
        point_belief = player.in_round(1).sports_pt_belief
        return dict(topic=player.topic, belief=belief, point=point_belief)


class Sports(Page):
    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return player.round_number > (participant.task_rounds['Sports and Video Games'] - 1) * C.N and player.round_number <= (
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
                if p.signal == 1 and p.effort == 0:
                    succes_L += 1
                elif p.signal == 1 and p.effort == 1:
                    succes_M += 1
                elif p.signal == 1 and p.effort == 2:
                    succes_H += 1
                elif p.signal == 0 and p.effort == 0:
                    fail_L += 1
                elif p.signal == 0 and p.effort == 1:
                    fail_M += 1
                else:
                    fail_H += 1
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
        return player.round_number > (
                    participant.task_rounds['Sports and Video Games'] - 1) * C.N and player.round_number <= (
                   participant.task_rounds['Sports and Video Games']) * C.N

    @staticmethod
    def vars_for_template(player):
        other = player.get_others_in_group()[0]
        other = other.participant
        score = other.verbal_score
        session = player.session

        e = player.effort
        if score < C.T1:
            type = 0
        elif score >= C.T1 & score < C.T2:
            type = 1
        else:
            type = 2

        round = player.round_number - 1 - C.N*participant.task_rounds['Sports and Video Games']
        player.signal = int(session.outcomes_sports[type][e, round])
        return dict(signal=player.signal, topic=player.topic)


class UsStart(Page):
    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return player.round_number == (participant.task_rounds['US Geography'] - 1) * C.N + 1

    @staticmethod
    def vars_for_template(player):
        player.topic = 'US Geography'
        belief = player.in_round(1).us_belief
        point_belief = player.in_round(1).us_pt_belief
        return dict(topic=player.topic, belief=belief, point=point_belief)


class Us(Page):
    @staticmethod
    def is_displayed(player: Player):
        participant = player.participant
        return player.round_number > (
                participant.task_rounds['US Geography'] - 1) * C.N and player.round_number <= (
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

        if player.round_number > (participant.task_rounds['US Geography'] - 1) * C.N + 1:
            previous_rounds = player.in_rounds((participant.task_rounds['US Geography'] - 1) * C.N + 1,
                                               player.round_number - 1)
            for p in previous_rounds:
                if p.signal == 1 and p.effort == 0:
                    succes_L += 1
                elif p.signal == 1 and p.effort == 1:
                    succes_M += 1
                elif p.signal == 1 and p.effort == 2:
                    succes_H += 1
                elif p.signal == 0 and p.effort == 0:
                    fail_L += 1
                elif p.signal == 0 and p.effort == 1:
                    fail_M += 1
                else:
                    fail_H += 1
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
        return player.round_number > (
                    participant.task_rounds['US Geography'] - 1) * C.N and player.round_number <= (
                   participant.task_rounds['US Geography']) * C.N

    @staticmethod
    def vars_for_template(player):
        other = player.get_others_in_group()[0]
        other = other.participant
        score = other.verbal_score
        session = player.session

        e = player.effort
        if score < C.T1:
            type = 0
        elif score >= C.T1 & score < C.T2:
            type = 1
        else:
            type = 2

        round = player.round_number - 1 - C.N*participant.task_rounds['US Geography']
        player.signal = int(session.outcomes_us[type][e, round])
        return dict(signal=player.signal, topic=player.topic)


class Results(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

    @staticmethod
    def vars_for_template(player):
        participant = player.participant
        random_round = random.randint(1, len(C.TASKS))
        task = C.TASKS[random_round-1]
        round = (participant.task_rounds[task]) * C.N

        in_task_rounds = player.in_rounds((participant.task_rounds[task] - 1) * C.N,  (
                   participant.task_rounds[task]) * C.N)

        score = 0
        for p in in_task_rounds:
            score += p.signal

        player.payoff = score

        return dict( part1_topic=participant.part1_topic,
                     part1_score=participant.part1_score,
                     part2_topic=task,
                     part2_score=score,
                     total=(score+participant.part1_score))


class ResultsWaitPage(WaitPage):
    pass


page_sequence = [Performance, MyWaitPage, Instructions,
                 VerbalStart, Verbal, VerbalFeedback,
                 MathStart, Math, MathFeedback,
                 PopStart, Pop, PopFeedback,
                 ScienceStart, Science, ScienceFeedback,
                 SportsStart, Sports, SportsFeedback,
                 UsStart, Us, UsFeedback, Results]
