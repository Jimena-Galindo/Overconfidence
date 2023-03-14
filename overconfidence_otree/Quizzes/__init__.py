from otree.api import *
import numpy as np

doc = """
Observe trials of a DAG and leave a comment
"""


class C(BaseConstants):
    NAME_IN_URL = 'Part1'
    PLAYERS_PER_GROUP = None
    # there must be as many rounds as there are cases in the case_list defined in the instructions page
    NUM_ROUNDS = 11
    N_trials = 27


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    notes = models.LongStringField()
    case = models.StringField()
    case_order = models.StringField()
    error = models.IntegerField(initial=0)


# FUNCTIONS
def html_table_probs(case, probs, n):
    # case should be an array of dimensions kxn. k is the number of unique trials and n is n_lights + others + sound
    # frequency should be a vector of size k with each element i equal to the number or repetitions of trial i wanted
    # the total number of trials will be sum(freq)

    draws = np.random.choice([i for i in range(len(case))], size=n, replace=True, p=probs)

    # n_lights is the number of lights excluding "others". This can be 2 (Red and Blue) or 3 (Red, Blue, Green)
    n_lights = len(case[0])

    # Create a matrix with the realizations of each row (they are already in a random order because draws is random)
    h = []
    for i in range(len(draws)):
        h.append(case[draws[i]])

    # 2 lights: Red, Blue (and Others)
    if n_lights == 4:

        # Translate the binary matrix into a html matrix
        red = []
        blue = []
        sound = []
        other = ['&#x3f'] * len(draws)

        for i in range(len(draws)):
            # red lights
            if h[i][0] == 1:
                red.append('<div class="circle_red"></div>')
            else:
                red.append('<div class="circle_red_off"></div>')

            # blue lights
            if h[i][1] == 1:
                blue.append('<div class="circle_blue"></div>')
            else:
                blue.append('<div class="circle_blue_off"></div>')

            # sound
            if h[i][3] == 1:
                sound.append('<b>&#x266A; DING &#x266A;</b>')
            else:
                sound.append('NO DING')

        html_mat = np.column_stack((red, blue, other, sound))

        # Write out the html table code
        table = '<table class="table" style="text-align: center">' \
                '<tr><th>Red Light</th><th>Blue Light</th><th>Other Lights</th><th>Sound</th></tr>'

        for i in range(len(draws)):
            table = table + '<tr style="height: 25px; font-size: 12px"><td>' + html_mat[i][0] + '</td>' \
                                                        '<td>' + html_mat[i][1] + '</td>' \
                                                        '<td>' + html_mat[i][2] + '</td>' \
                                                        '<td>' + html_mat[i][3] + '</td></tr>'

        table = table + '</table>'

    # 3 lights: Red, Blue, Green (and Others)
    if n_lights == 5:

        # Translate the binary matrix into a html matrix
        red = []
        blue = []
        green = []
        sound = []
        other = ['&#x3f'] * len(draws)

        for i in range(len(draws)):
            # red lights
            if h[i][0] == 1:
                red.append('<div class="circle_red"></div>')
            else:
                red.append('<div class="circle_red_off"></div>')

            # blue lights
            if h[i][1] == 1:
                blue.append('<div class="circle_blue"></div>')
            else:
                blue.append('<div class="circle_blue_off"></div>')

            # green lights
            if h[i][1] == 1:
                green.append('<div class="circle_green"></div>')
            else:
                green.append('<div class="circle_green_off"></div>')

            # sound
            if h[i][3] == 1:
                sound.append('<b>&#x266A; DING &#x266A;</b>')
            else:
                sound.append('NO DING')

        html_mat = np.column_stack((red, blue, green, other, sound))

        # Write out the html table code
        table = '<table class="table" style="text-align: center">' \
                '<tr><th>Red Light</th><th>Blue Light</th><th>Green Light</th><th>Other Lights</th><th>Sound</th></tr>'

        for i in range(len(draws)):
            table = table + '<tr style="height: 25px; font-size: 12px"><td>' + html_mat[i][0] + '</td>' \
                                                        '<td>' + html_mat[i][1] + '</td>' \
                                                        '<td>' + html_mat[i][2] + '</td>' \
                                                        '<td>' + html_mat[i][3] + '</td>' \
                                                        '<td>' + html_mat[i][4] + '</td></tr>'

        table = table + '</table>'

    return table, h


def html_table_freqs(case, freq):
    # case should be an array of dimensions kxn. k is the number of unique trials and n is n_lights + others + sound
    # frequency should be a vector of size k with each element i equal to the number or repetitions of trial i wanted
    # the total number of trials will be sum(freq)

    # n_lights is the number of lights excluding "others". This can be 2 (Red and Blue) or 3 (Red, Blue, Green)
    n_lights = len(case[0])

    # 2 lights: Red, Blue (and Others)
    if n_lights == 4:

        # Add the repetitions for each row
        h = np.tile(case[0], (freq[0], 1))
        for i in range(len(freq) - 1):
            a = np.tile(case[i + 1], (freq[i + 1], 1))
            h = np.vstack((h, a))

        # Shuffle the rows of html matrix with repeated trials
        np.random.shuffle(h)

        # Translate the binary matrix into a html matrix
        red = []
        blue = []
        sound = []
        other = ['&#x3f'] * sum(freq)

        for i in range(sum(freq)):
            # red lights
            if h[i][0] == 1:
                red.append('<div class="circle_red"></div>')
            else:
                red.append('<div class="circle_red_off"></div>')

            # blue lights
            if h[i][1] == 1:
                blue.append('<div class="circle_blue"></div>')
            else:
                blue.append('<div class="circle_blue_off"></div>')

            # sound
            if h[i][3] == 1:
                sound.append('&#x266A; DING &#x266A;')
            else:
                sound.append('-')

        html_mat = np.column_stack((red, blue, other, sound))

        # Write out the html table code
        table = '<table class="table" style="text-align: center; overflow-y: auto;">' \
                '<tr style="height: 5px; font-size: 10px; padding: 3px; white-space: nowrap; border-collapse: collapse;">'\
                '<th style="height: 5px; font-size: 12px; padding: 3px; white-space: nowrap; border-collapse: collapse;">Red Light</th>' \
                '<th style="height: 5px; font-size: 12px; padding: 3px; white-space: nowrap; border-collapse: collapse;">Blue Light</th>' \
                '<th style="height: 5px; font-size: 12px; padding: 3px; white-space: nowrap; border-collapse: collapse;">Other Lights</th>' \
                '<th style="height: 5px; font-size: 12px; padding: 3px; white-space: nowrap; border-collapse: collapse;">Sound</th></tr>'

        for i in range(sum(freq)):
            table = table + '<tr style="height: 5px; font-size: 12px; padding: 3px; white-space: nowrap; border-collapse: collapse; vertical-align: middle" >' \
                            '<td style="height: 5px; font-size: 12px; padding: 3px; white-space: nowrap; border-collapse: collapse;">' + html_mat[i][0] + '</td>'\
                                 '<td style="height: 5px; font-size: 12px; padding: 3px; white-space: nowrap; border-collapse: collapse;">' + html_mat[i][1] + '</td>'\
                                 '<td style="height: 5px; font-size: 12px; padding: 3px; white-space: nowrap; border-collapse: collapse;">' + html_mat[i][2] + '</td>'\
                                 '<td style="height: 5px; font-size: 12px; padding: 3px; white-space: nowrap; border-collapse: collapse;">' + html_mat[i][3] + '</td></tr>'

        table = table + '</table>'

    # 3 lights: Red, Blue, Green (and Others)
    if n_lights == 5:

        # Add the repetitions for each row
        h = np.tile(case[0], (freq[0], 1))
        for i in range(len(freq) - 1):
            a = np.tile(case[i + 1], (freq[i + 1], 1))
            h = np.vstack((h, a))

        # Shuffle the rows of html matrix with repeated trials
        np.random.shuffle(h)

        # Translate the binary matrix into a html matrix
        red = []
        blue = []
        green = []
        sound = []
        other = ['&#x3f'] * sum(freq)

        for i in range(sum(freq)):
            # red lights
            if h[i][0] == 1:
                red.append('<div class="circle_red"></div>')
            else:
                red.append('<div class="circle_red_off"></div>')

            # blue lights
            if h[i][1] == 1:
                blue.append('<div class="circle_blue"></div>')
            else:
                blue.append('<div class="circle_blue_off"></div>')

            # green lights
            if h[i][1] == 1:
                green.append('<div class="circle_green"></div>')
            else:
                green.append('<div class="circle_green_off"></div>')

            # sound
            if h[i][3] == 1:
                sound.append('&#x266A; DING &#x266A;')
            else:
                sound.append('-')

        html_mat = np.column_stack((red, blue, green, other, sound))

        # Write out the html table code
        table = '<table class="table" style="text-align: center">' \
                '<tr>' \
                '<th style="height: 5px; font-size: 12px; padding: 3px; white-space: nowrap; border-collapse: collapse;">Red Light</th>' \
                '<th style="height: 5px; font-size: 12px; padding: 3px; white-space: nowrap; border-collapse: collapse;">Blue Light</th>' \
                '<th style="height: 5px; font-size: 12px; padding: 3px; white-space: nowrap; border-collapse: collapse;">Green Light</th>' \
                '<th style="height: 5px; font-size: 12px; padding: 3px; white-space: nowrap; border-collapse: collapse;">Other Lights</th>' \
                '<th style="height: 5px; font-size: 12px; padding: 3px; white-space: nowrap; border-collapse: collapse;">Sound</th></tr>'

        for i in range(sum(freq)):
            table = table + '<tr style="vertical-align: middle;"><td style="height: 5px; font-size: 12px; padding: 3px; white-space: nowrap; border-collapse: collapse;">' + html_mat[i][0] + '</td>'\
                                 '<td style="height: 5px; font-size: 12px; padding: 3px; white-space: nowrap; border-collapse: collapse;">' + html_mat[i][1] + '</td>'\
                                 '<td style="height: 5px; font-size: 12px; padding: 3px; white-space: nowrap; border-collapse: collapse;">' + html_mat[i][2] + '</td>'\
                                 '<td style="height: 5px; font-size: 12px; padding: 3px; white-space: nowrap; border-collapse: collapse;">' + html_mat[i][3] + '</td>'\
                                 '<td style="height: 5px; font-size: 12px; padding: 3px; white-space: nowrap; border-collapse: collapse;">' + html_mat[i][4] + '</td></tr>'

        table = table + '</table>'

    return table, h


# PAGES
class Instructions(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if player.round_number == 1:
            participant = player.participant
            participant.notes = []
            participant.guesses = []
            participant.sound = []
            participant.realized_cases = []
            # The number of trials for each case is n_trials defined in the subsession variables.
            # It has to be at least 10 for stage 2 to work.

            # The columns of a case with 2 lights are Red light, Blue light, Other lights, Sound
            case1 = [[0, 0, 0, 0],
                     [0, 0, 0, 1],
                     [0, 1, 0, 0],
                     [0, 1, 0, 1],
                     [1, 1, 0, 0],
                     [1, 1, 0, 1],
                     [1, 0, 0, 0],
                     [1, 0, 0, 1]]

            # the vector freq contains the number of repetitions for each of the rows in case. The length of freq
            # should be equal to the number of rows in case.
            # the sum of freq is the number of trials that will be shown to the subject.
            freq1 = [8, 14, 1, 2, 0, 0, 1, 1]
            freq2 = [8, 5, 1, 7, 0, 2, 1, 3]
            freq3 = [9, 2, 1, 8, 0, 3, 0, 4]
            freq4 = [3, 1, 3, 1, 2, 8, 2, 7]
            freq5 = [4, 0, 4, 1, 1, 8, 1, 8]
            freq6 = [3, 1, 3, 1, 4, 14, 0, 1]
            freq7 = [6, 1, 2, 0, 2, 15, 0, 1]
            freq8 = [9, 5, 0, 2, 0, 7, 1, 3]
            freq9 = [10, 3, 0, 1, 0, 12, 0, 1]
            freq10 = [0, 0, 2, 1, 4, 15, 4, 1]
            freq11 = [1, 0, 3, 0, 2, 15, 5, 1]

            # p is the probability that the red light is on, q is the same for the blue light and e is for other lights
            # p = 1/2
            # q = 1/2
            # e = 1/4

            # the vector prob1 has the probabilities that each row of the case is realized.
            # This is for one particular DAG. If this method of generating the trials of the case wants to be used,
            # the tables should be generated with html_table_probs instead of html_table_freqs
            # prob1 = [p*(1-e), p*e, (1-p)*e*q, (1-p)*q*(1-e), (1-p)*(1-q)*e, (1-p)*(1-q)*(1-e)]

            # Both methods can handle tables with an extra light (red, blue and green)
            # The columns of a case with 3 lights are Red light, Blue light, Green light, Other lights, Sound
            # case2 = [[1, 1, 1, 1, 1],
                     # [0, 0, 0, 0, 0]]

            # p =
            # q =
            # r =
            # e =

            # prob2_5l = [1/2, 1/2]

            # freq2_5l = [15, 12]

            # bundle each case together with its frequencies and then list all bundles to be used
            # The number of rounds for each subsession must be equal to the number of bundles in this list.
            # The list will be shuffled at a participant level and that order of cases will be shown in all parts
            case_list = [[case1, freq1, '1L'],
                         [case1, freq2, '2H'],
                         [case1, freq3, '2L'],
                         [case1, freq4, '3H'],
                         [case1, freq5, '3L'],
                         [case1, freq6, '4H'],
                         [case1, freq7, '4L'],
                         [case1, freq8, '5H'],
                         [case1, freq9, '5L'],
                         [case1, freq10, '7H'],
                         [case1, freq11, '7L']]

            # shuffle the bundles of [case, freq] to determine the order in which they are shown to the participant.
            # the ordered list is saved at the participant level so participant variables should be downloaded to get it
            np.random.shuffle(case_list)
            participant.order_names = [case_list[i][-1] for i in range(len(case_list))]
            participant.cases_ordered = [case_list[i][0:2] for i in range(len(case_list))]
            player.case_order = str(participant.cases_ordered)


class Machine(Page):
    form_model = 'player'
    form_fields = ['notes']

    @staticmethod
    def vars_for_template(player: Player):
        r = player.round_number
        participant = player.participant
        # get the case corresponding to the round
        case = participant.cases_ordered[r-1]

        # get the html code for the table (this part also generates the repetitions of each row)
        evaluated = html_table_freqs(case[0], case[1])
        matrix = evaluated[1]

        # save the case matrix as a string for the player. The cases are also saves as matrices at the participant level
        player.case = str(matrix)
        participant.current_case = matrix

        return dict(table=evaluated[0], round=r)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # save all the notes at participant level to pass them to the next stage
        participant = player.participant
        all_notes = participant.notes
        all_notes.append(player.notes)
        participant.notes = all_notes
        # this saves the (last if there was an error and the page reloaded) realized cases
        # (ordered and with the repeated rows as a list of matrices)
        participant.realized_cases.append(participant.current_case)

    @staticmethod
    def error_message(player, values):
        if len(values['notes']) > 280:
            player.error = 1
            return 'Your notes are too long. Please use at most 280 characters'


class MyWaitPage(WaitPage):
    # this wait page is not necessary. It is here to get everyone up to the same point and possibly shorten the necessary
    # wait between stages 2 and 3.
    @staticmethod
    def is_displayed(player):
        return player.round_number == C.NUM_ROUNDS

    title_text = "End of Part 1"
    body_text = "You have reached the end of Part 1. " \
                "Before we move on to Part 2 we will wait for the other participants to finish Part 1"
    wait_for_all_groups = True


class ResultsWaitPage(WaitPage):
    pass


page_sequence = [Instructions, Machine]
