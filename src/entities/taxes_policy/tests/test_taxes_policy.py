import pytest
from entities.taxes_policy.models import TaxesPolicy
from common.exceptions import IntegrityError


@pytest.mark.django_db
class TestTaxesPolicy:

    def test_create(self):
        year = 2020
        policy = TaxesPolicy.objects.create(year=year)
        assert policy
        assert policy.year == year
        assert policy.ranges.count() == 0

    def test_create_without_year(self):
        with pytest.raises(IntegrityError):
            TaxesPolicy.objects.create()

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
