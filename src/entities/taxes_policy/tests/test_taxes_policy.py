import pytest

from common.utils import InfinityLimit
from entities.taxes_policy.models import TaxesPolicy, TaxesPolicyRange
from common.exceptions import IntegrityError, ValidationError


@pytest.mark.django_db
class TestTaxesPolicy:

    def test_create(self):
        year = 2020
        policy = TaxesPolicy.objects.create(year=year)
        assert policy
        assert policy.year == year
        assert policy.ranges.count() == 0

    def test_create_without_year(self):
        policy = TaxesPolicy.objects.create()
        assert policy.year == 0

    def test_create_for_already_existing_year(self, taxes_policy_factory):
        policy = taxes_policy_factory()
        with pytest.raises(IntegrityError):
            TaxesPolicy.objects.create(year=policy.year)

    @pytest.mark.django_db(transaction=True)
    def test_create_with_invalid_year(self, taxes_policy_factory, fake):
        for invalid_year in [-1200, None, '', fake.word(), type]:
            try:
                TaxesPolicy.objects.create(year=invalid_year)
                assert False
            except (IntegrityError, ValueError, TypeError):
                assert True

    def test_edit_year(self, taxes_policy_factory):
        old_year, new_year = 2020, 2021
        policy = taxes_policy_factory(year=old_year)
        assert policy.year == old_year
        policy.year = new_year
        policy.save()
        policy.refresh_from_db()
        assert policy.year == new_year

    def test_try_to_change_year_to_already_existing(self, taxes_policy_factory):
        policy_1, policy_2 = taxes_policy_factory(), taxes_policy_factory()
        with pytest.raises(IntegrityError):
            policy_2.year = policy_1.year
            policy_2.save()

    def test_add_range(self, taxes_policy_factory, taxes_policy_range_factory):
        policy = taxes_policy_factory()
        policy_range = taxes_policy_range_factory()
        assert policy.ranges.count() == 0
        policy.ranges.add(policy_range)
        assert policy.ranges.count() == 1
        assert policy_range in policy.ranges.all()
        assert policy in policy_range.taxes_policies.all()

    def test_remove_range(self, taxes_policy_factory, taxes_policy_range_factory):
        policy = taxes_policy_factory()
        policy_range = taxes_policy_range_factory()
        assert policy.ranges.count() == 0
        policy.ranges.set([policy_range])
        assert policy.ranges.count() == 1
        assert policy_range in policy.ranges.all()
        assert policy in policy_range.taxes_policies.all()

    def test_set_range(self, taxes_policy_factory, taxes_policy_range_factory):
        policy = taxes_policy_factory()
        policy_range = taxes_policy_range_factory()
        policy.ranges.add(policy_range)
        assert policy.ranges.count() == 1
        policy.ranges.remove(policy_range)
        assert policy.ranges.count() == 0

    def test_delete(self, taxes_policy_factory, taxes_policy_range_factory):
        policy = taxes_policy_factory()
        policy_range = taxes_policy_range_factory()
        policy.ranges.add(policy_range)
        policy.delete()
        assert not TaxesPolicy.objects.first()
        assert policy_range.taxes_policies.count() == 0


@pytest.mark.django_db
class TestTaxesPolicyRange:

    def test_create(self):
        policy_range: TaxesPolicyRange = TaxesPolicyRange.objects.create(amount_to=100)
        assert policy_range.amount_to == 100
        assert policy_range.amount_from == 0
        assert policy_range.percent == 0
        assert policy_range.taxes_policies.count() == 0

        amount_to, amount_from, percent = 100, 80, 25
        policy_range: TaxesPolicyRange = TaxesPolicyRange.objects.create(
            amount_to=100, amount_from=amount_from, percent=percent
        )
        assert policy_range.amount_to == amount_to
        assert policy_range.amount_from == amount_from
        assert policy_range.percent == percent
        assert policy_range.taxes_policies.count() == 0

    def test_try_to_create_with_amount_to_less_then_amount_from(self, taxes_policy_range_factory):
        with pytest.raises(ValidationError):
            taxes_policy_range_factory(amount_to=100, amount_from=200)

    def test_create_with_amount_to_as_infinity_limit(self, taxes_policy_range_factory):
        policy_range = TaxesPolicyRange.objects.create(amount_to=None)
        assert policy_range.amount_from == 0
        assert policy_range.amount_to == InfinityLimit()
        assert policy_range._amount_to is None
        policy_range = TaxesPolicyRange.objects.create(amount_to=None)
        assert policy_range.amount_from == 0
        assert policy_range.amount_to == InfinityLimit()
        assert policy_range._amount_to is None
        assert policy_range.is_overlapping_with(taxes_policy_range_factory())

    def test_create_with_invalid_percent(self, taxes_policy_range_factory):
        taxes_policy_range_factory(percent=0)
        taxes_policy_range_factory(percent=100)
        with pytest.raises(IntegrityError):
            taxes_policy_range_factory(percent=-1)
            taxes_policy_range_factory(percent=101)

    def test_is_overlapping_with(self):
        not_overlapping_amount_values = [
            ((0, 5), (6, 10)),
            ((5, 15), (60, 250)),

            ((0, 20), (21, None)),
        ]
        overlapping_amount_values = [
            ((0, 5), (5, 10)),
            ((5, 15), (15, 100)),
            ((0, 50), (5, 10)),
            ((5, 10), (0, 50)),

            ((0, None), (10, 15)),
        ]
        for values_for_range_1, values_for_range_2 in not_overlapping_amount_values:
            range_1 = TaxesPolicyRange.objects.create(amount_from=values_for_range_1[0], amount_to=values_for_range_1[1])  # noqa
            range_2 = TaxesPolicyRange.objects.create(amount_from=values_for_range_2[0], amount_to=values_for_range_2[1])  # noqa
            assert not range_1.is_overlapping_with(range_2)

        for values_for_range_1, values_for_range_2 in overlapping_amount_values:
            range_1 = TaxesPolicyRange.objects.create(amount_from=values_for_range_1[0], amount_to=values_for_range_1[1])  # noqa
            range_2 = TaxesPolicyRange.objects.create(amount_from=values_for_range_2[0], amount_to=values_for_range_2[1])  # noqa
            assert range_1.is_overlapping_with(range_2)
