from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)
from wsd_app import dataset
from os import environ
import random

doc = """
Word Sense Disambiguation game
"""


class Constants(BaseConstants):
    name_in_url = 'wsd'
    players_per_group = 3
    num_others = players_per_group - 1
    num_rounds = int(environ.get('WSD_ROUNDS', 3))
    instructions_template = 'wsd_app/includes/instructions.html'
    currency_name = 'dollar'
    time_for_decision = 60
    time_for_instructions = 60
    wsd_wp_max_waiting_time = 60

    # score for each case
    disagreement = c(0)
    initial_agreement = c(3)
    eventual_agreement = c(1)


class Subsession(BaseSubsession):
    def creating_session(self):
        # select which round will be paid out, this is unique for each player
        if self.round_number == 1:
            for p in self.session.get_participants():
                p.vars['payable_round'] = random.randint(1, Constants.num_rounds)
        # check if this is the round that get paid out
        for p in self.get_players():
            p.payable_round = p.participant.vars.get('payable_round')


class Group(BaseGroup):
    is_initial_agreement = models.BooleanField()   # see if players reach agreement on first try
    is_eventual_agreement = models.BooleanField()  # see if eventual agreement is reached
    is_golden_label = models.BooleanField()        # added for analysis to see if group has picked the golden label

    def set_initial_payoffs(self):
        p1 = self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)
        p3 = self.get_player_by_id(3)

        # check if players agree with each other
        if p1.decision == p2.decision == p3.decision:
            p1.intermediary_payoff = Constants.initial_agreement
            p2.intermediary_payoff = Constants.initial_agreement
            p3.intermediary_payoff = Constants.initial_agreement
            self.is_initial_agreement = True
        else:
            p1.intermediary_payoff = Constants.disagreement
            p2.intermediary_payoff = Constants.disagreement
            p3.intermediary_payoff = Constants.disagreement
            self.is_initial_agreement = False

        for p in self.get_players():
            p.initial_decision = p.decision
            p.written_outcome = p.outcome()
            if p.payable_round == self.round_number:
                p.payoff = p.intermediary_payoff

    def set_final_payoffs(self):
        p1 = self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)
        p3 = self.get_player_by_id(3)

        # check if there is agreement reached after negotiation.
        # Player get initial_agreement points if the decision did not change, otherwise eventual_agreement points
        if p1.decision == p2.decision == p3.decision:
            self.is_eventual_agreement = True
            for p in self.get_players():
                if p.decision == p.initial_decision:
                    p.intermediary_payoff = Constants.initial_agreement
                else:
                    p.intermediary_payoff = Constants.eventual_agreement

                p.written_outcome = p.outcome()
                if p.payable_round == self.round_number:
                    p.payoff = p.intermediary_payoff
        else:
            p1.intermediary_payoff = Constants.disagreement
            p2.intermediary_payoff = Constants.disagreement
            p3.intermediary_payoff = Constants.disagreement
            self.is_eventual_agreement = False


class Player(BasePlayer):
    def current_payoff_in_real_currency(self):
        return self.intermediary_payoff.to_real_world_currency(self.session)

    def payoff_in_real_currency(self):
        return self.in_round(self.payable_round).payoff.to_real_world_currency(self.session)

    time_for_initial_decision = models.FloatField()    # time it takes to make initial decision
    time_for_decision_when_disagreement_occurred = models.FloatField()    # time it takes when there is a disagreement

    intermediary_payoff = models.CurrencyField()  # this fields hold what the payment will be in this round
    payable_round = models.IntegerField()

    def outcome(self):
        if int(self.intermediary_payoff) == int(Constants.initial_agreement):
            return 'Your team agrees with you, congratulations!'
        if int(self.intermediary_payoff) == int(Constants.disagreement):
            return 'Your team disagrees'
        if int(self.intermediary_payoff) == int(Constants.eventual_agreement):
            return "Your team eventually reached an agreement"

    written_outcome = models.StringField()    # this field hold the outcome
    initial_decision = models.IntegerField()  # stores the initial decision that is compared in case of a disagreement
    decision = models.IntegerField(label='Senses:',
                                   choices=dataset.SENSES,
                                   widget=widgets.RadioSelect)


def custom_export(players):
    players = players.filter(participant__label__isnull=False)
    participants = set([p.participant for p in players])
    yield ['assignment_id', 'bonus', 'msg', 'participant_code', 'session', ]
    for p in participants:
        if p.vars.get('payable'):
            payable_bonus = round(float(p.vars.get('payoff_in_real_currency', 0)), 2) or 0.01

            yield [p.label, payable_bonus, 'Thank you for participating!', p.code, p.session.code]
