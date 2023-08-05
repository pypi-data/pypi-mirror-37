# -*- coding: utf-8 -*-

from datetime import datetime

from flask_split.models import Alternative, Experiment
from flexmock import flexmock

from . import TestCase


class TestAlternative(TestCase):
    def test_has_name(self):
        alternative = Alternative(self.redis, 'Basket', 'basket_text')
        assert alternative.name == 'Basket'

    def test_has_default_participation_count_of_0(self):
        alternative = Alternative(self.redis, 'Basket', 'basket_text')
        assert alternative.participant_count == 0

    def test_has_default_completed_count_of_0(self):
        alternative = Alternative(self.redis, 'Basket', 'basket_text')
        assert alternative.completed_count == 0

    def test_belong_to_an_experiment(self):
        experiment = Experiment(self.redis, 'basket_text', 'Basket', 'Cart')
        experiment.save()
        alternative = Alternative(self.redis, 'Basket', 'basket_text')
        assert alternative.experiment.name == experiment.name

    def test_saves_to_redis(self):
        alternative = Alternative(self.redis, 'Basket', 'basket_text')
        alternative.save()
        assert 'basket_text:Basket' in self.redis

    def test_increment_participation_count(self):
        experiment = Experiment(self.redis, 'basket_text', 'Basket', "Cart")
        experiment.save()
        alternative = Alternative(self.redis, 'Basket', 'basket_text')
        old_participant_count = alternative.participant_count
        alternative.increment_participation()
        assert alternative.participant_count == old_participant_count + 1

    def test_increment_completed_count(self):
        experiment = Experiment(self.redis, 'basket_text', 'Basket', "Cart")
        experiment.save()
        alternative = Alternative(self.redis, 'Basket', 'basket_text')
        old_completed_count = alternative.participant_count
        alternative.increment_completion()
        assert alternative.completed_count == old_completed_count + 1

    def test_can_be_reset(self):
        alternative = Alternative(self.redis, 'Basket', 'basket_text')
        alternative.participant_count = 10
        alternative.completed_count = 4
        alternative.reset()
        assert alternative.participant_count == 0
        assert alternative.completed_count == 0

    def test_know_if_it_is_the_control_of_an_experiment(self):
        experiment = Experiment(self.redis, 'basket_text', 'Basket', 'Cart')
        experiment.save()
        alternative = Alternative(self.redis, 'Basket', 'basket_text')
        assert alternative.is_control
        alternative = Alternative(self.redis, 'Cart', 'basket_text')
        assert not alternative.is_control

    def test_conversion_rate_is_0_if_there_are_no_conversions(self):
        alternative = Alternative(self.redis, 'Basket', 'basket_text')
        assert alternative.completed_count == 0
        assert alternative.conversion_rate == 0

    def test_conversion_rate_does_something(self):
        alternative = Alternative(self.redis, 'Basket', 'basket_text')
        alternative.participant_count = 10
        alternative.completed_count = 4
        assert alternative.conversion_rate == 0.4

    def test_z_score_is_none_for_the_control(self):
        experiment = Experiment.find_or_create(
            self.redis, 'link_color', 'blue', 'red')
        assert experiment.control.z_score is None

    def test_z_score_is_none_when_the_control_has_no_participations(self):
        experiment = Experiment(self.redis, 'link_color', 'blue', 'red')
        experiment.save()
        alternative = Alternative(self.redis, 'red', 'link_color')
        assert alternative.z_score is None

    def test_z_score_is_none_when_alternative_has_no_participations(self):
        experiment = Experiment.find_or_create(
            self.redis, 'link_color', 'blue', 'red')
        experiment.save()
        alternative = Alternative(self.redis, 'red', 'link_color')
        assert alternative.z_score is None

    def test_z_score_when_control_and_alternative_have_perfect_conversion(self):
        experiment = Experiment.find_or_create(
            self.redis, 'link_color', 'blue', 'red')
        experiment.save()
        control = Alternative(self.redis, 'blue', 'link_color')
        control.completed_count = 10
        control.participant_count = 10
        alternative = Alternative(self.redis, 'red', 'link_color')
        alternative.completed_count = 8
        alternative.participant_count = 8
        assert alternative.z_score is None

    def test_z_score(self):
        Experiment.find_or_create(self.redis, 'Treatment',
            'Control', 'Treatment A', 'Treatment B', 'Treatment C')

        control = Alternative(self.redis, 'Control', 'Treatment')
        control.participant_count = 182
        control.completed_count = 35

        treatment_a = Alternative(self.redis, 'Treatment A', 'Treatment')
        treatment_a.participant_count = 180
        treatment_a.completed_count = 45

        treatment_b = Alternative(self.redis, 'Treatment B', 'Treatment')
        treatment_b.participant_count = 189
        treatment_b.completed_count = 28

        treatment_c = Alternative(self.redis, 'Treatment C', 'Treatment')
        treatment_c.participant_count = 188
        treatment_c.completed_count = 61

        assert control.z_score is None
        assert round(treatment_a.z_score, 2) == 1.33
        assert round(treatment_b.z_score, 2) == -1.13
        assert round(treatment_c.z_score, 2) == 2.94


class TestExperiment(TestCase):
    def test_has_name(self):
        experiment = Experiment(self.redis, 'basket_text', 'Basket', 'Cart')
        assert experiment.name == 'basket_text'

    def test_has_alternatives(self):
        experiment = Experiment(self.redis, 'basket_text', 'Basket', 'Cart')
        assert len(experiment.alternatives) == 2

    def test_saves_to_redis(self):
        experiment = Experiment(self.redis, 'basket_text', 'Basket', 'Cart')
        experiment.save()
        assert 'basket_text' in self.redis

    def test_saves_the_start_time_to_redis(self):
        experiment_start_time = datetime(2012, 3, 9, 22, 1, 34)
        (flexmock(Experiment)
            .should_receive('_get_time')
            .and_return(experiment_start_time))
        experiment = Experiment(self.redis, 'basket_text', 'Basket', 'Cart')
        experiment.save()
        assert experiment.start_time == experiment_start_time

    def test_handles_not_having_a_start_time(self):
        experiment_start_time = datetime(2012, 3, 9, 22, 1, 34)
        (flexmock(Experiment)
            .should_receive('_get_time')
            .and_return(experiment_start_time))
        experiment = Experiment(self.redis, 'basket_text', 'Basket', 'Cart')
        experiment.save()

        self.redis.hdel('experiment_start_times', experiment.name)

        assert experiment.start_time is None

    def test_does_not_create_duplicates_when_saving_multiple_times(self):
        experiment = Experiment(self.redis, 'basket_text', 'Basket', 'Cart')
        experiment.save()
        experiment.save()
        assert 'basket_text' in self.redis
        assert self.redis.lrange('basket_text', 0, -1) == ['Basket', 'Cart']

    def test_deleting_should_delete_itself(self):
        experiment = Experiment(self.redis, 'basket_text', 'Basket', 'Cart')
        experiment.save()

        experiment.delete()
        assert 'basket_text' not in self.redis

    def test_deleting_should_increment_the_version(self):
        experiment = Experiment.find_or_create(
            self.redis, 'link_color', 'blue', 'red', 'green')
        assert experiment.version == 0
        experiment.delete()
        assert experiment.version == 1

    def test_is_new_record_knows_if_it_hasnt_been_saved_yet(self):
        experiment = Experiment(self.redis, 'basket_text', 'Basket', 'Cart')
        assert experiment.is_new_record

    def test_is_new_record_knows_if_it_has_been_saved_yet(self):
        experiment = Experiment(self.redis, 'basket_text', 'Basket', 'Cart')
        experiment.save()
        assert not experiment.is_new_record

    def test_find_returns_an_existing_experiment(self):
        experiment = Experiment(self.redis, 'basket_text', 'Basket', 'Cart')
        experiment.save()
        assert Experiment.find(self.redis, 'basket_text').name == 'basket_text'

    def test_handles_non_existing_experiment(self):
        assert Experiment.find(self.redis, 'non_existent_experiment') is None

    def test_control_is_the_first_alternative(self):
        experiment = Experiment(self.redis, 'basket_text', 'Basket', 'Cart')
        experiment.save()
        assert experiment.control.name == 'Basket'

    def test_have_no_winner_initially(self):
        experiment = Experiment.find_or_create(
            self.redis, 'link_color', 'blue', 'red')
        assert experiment.winner is None

    def test_allow_you_to_specify_a_winner(self):
        experiment = Experiment.find_or_create(
            self.redis, 'link_color', 'blue', 'red')
        experiment.winner = 'red'

        experiment = Experiment.find_or_create(
            self.redis, 'link_color', 'blue', 'red')
        assert experiment.winner.name == 'red'

    def test_reset_should_reset_all_alternatives(self):
        experiment = Experiment.find_or_create(
            self.redis, 'link_color', 'blue', 'red', 'green')
        green = Alternative(self.redis, 'green', 'link_color')
        experiment.winner = 'green'

        assert experiment.next_alternative().name == 'green'
        green.increment_participation()

        experiment.reset()

        reset_green = Alternative(self.redis, 'green', 'link_color')
        assert reset_green.participant_count == 0
        assert reset_green.completed_count == 0

    def test_reset_should_reset_the_winner(self):
        experiment = Experiment.find_or_create(
            self.redis, 'link_color', 'blue', 'red', 'green')
        green = Alternative(self.redis, 'green', 'link_color')
        experiment.winner = 'green'

        assert experiment.next_alternative().name == 'green'
        green.increment_participation()

        experiment.reset()

        assert experiment.winner is None

    def test_reset_should_increment_the_version(self):
        experiment = Experiment.find_or_create(
            self.redis, 'link_color', 'blue', 'red', 'green')
        assert experiment.version == 0
        experiment.reset()
        assert experiment.version == 1

    def test_next_alternative_always_returns_the_winner_if_one_exists(self):
        experiment = Experiment.find_or_create(
            self.redis, 'link_color', 'blue', 'red', 'green')
        green = Alternative(self.redis, 'green', 'link_color')
        experiment.winner = 'green'

        assert experiment.next_alternative().name == 'green'
        green.increment_participation()

        experiment = Experiment.find_or_create(
            self.redis, 'link_color', 'blue', 'red', 'green')
        assert experiment.next_alternative().name == 'green'

    def test_reset_an_experiment_if_loaded_with_different_alternatives(self):
        experiment = Experiment(
            self.redis, 'link_color', 'blue', 'red', 'green')
        experiment.save()
        blue = Alternative(self.redis, 'blue', 'link_color')
        blue.participant_count = 5
        blue.save()
        same_experiment = Experiment.find_or_create(
            self.redis, 'link_color', 'blue', 'yellow', 'orange')
        alternative_names = [a.name for a in same_experiment.alternatives]
        assert alternative_names == ['blue', 'yellow', 'orange']
        new_blue = Alternative(self.redis, 'blue', 'link_color')
        assert new_blue.participant_count == 0
