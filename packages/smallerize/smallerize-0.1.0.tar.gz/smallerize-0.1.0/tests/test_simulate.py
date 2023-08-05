import smallerize
from smallerize.simulate import SimulatedTrial

from .fixtures import (
    factor_age,
    factor_sex,
    arm_one,
    arm_two,
    get_simple_minimizer,
    get_example_3to1,
    example_male_age_participants,
    example_table_one,
    get_simple_simulated_trial
)


class TestSimulatedTrial:

    def test_creation(self, factor_sex, get_simple_minimizer):
        minimizers = {
            'range': get_simple_minimizer(d_imbalance_method='range'),
            'std_dev': get_simple_minimizer(
                d_imbalance_method='standard_deviation'
            )
        }
        sim = SimulatedTrial(
            minimizers=minimizers,
            factors=[factor_sex]
        )
        assert isinstance(sim, SimulatedTrial)
        assert all(isinstance(m, smallerize.Minimizer)
                   for m in sim.minimizers.values())
        assert all(isinstance(f, smallerize.Factor)
                   for f in sim.factors.values())

    def test_create_random_participants(self, get_simple_simulated_trial):
        sim_trial = get_simple_simulated_trial()
        random_ppts = sim_trial.create_random_participants(10)

        for participant in random_ppts:
            for factor, level in participant.items():
                sim_factor = sim_trial.factors[factor]
                assert factor == sim_factor.name
                assert level in sim_factor.levels

    def test_assign_one(self, get_simple_simulated_trial):
        sim_trial = get_simple_simulated_trial()
        male = {'Sex': 'Male'}
        counts_before = {name: minner.get_current_x_counts(male)
                         for name, minner in sim_trial.minimizers.items()}
        assign_results = sim_trial.assign_one(male)
        counts_after = {name: minner.get_current_x_counts(male)
                        for name, minner in sim_trial.minimizers.items()}
        for name, minner in sim_trial.minimizers.items():
            arm = assign_results[name]['arm']
            assigned_before = counts_before[name]['Sex'][arm]
            assigned_after = counts_after[name]['Sex'][arm]
            assert assigned_after == assigned_before + 1

