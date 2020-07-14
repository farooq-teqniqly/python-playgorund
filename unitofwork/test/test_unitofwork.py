import pytest
from unitofwork.unitofwork import AbstractUnitOfWork, UnitOfWorkState, UnitOfWork


@pytest.fixture(scope="module")
def unit_of_work():
    return UnitOfWork("do stuff")


def test_unitofwork_when_created_state_is_new(unit_of_work: AbstractUnitOfWork):
    assert unit_of_work.state == UnitOfWorkState.NEW


def test_unitofwork_when_transaction_started_state_is_started(
    unit_of_work: AbstractUnitOfWork,
):
    with unit_of_work:
        assert unit_of_work.state == UnitOfWorkState.STARTED


def test_unitofwork_when_committed_state_is_comitted(unit_of_work: AbstractUnitOfWork):
    unit_of_work.commit()
    assert unit_of_work.state == UnitOfWorkState.COMMITTED


def test_unitofwork_when_rolledback_state_is_reversed(unit_of_work: AbstractUnitOfWork):
    unit_of_work.rollback()
    assert unit_of_work.state == UnitOfWorkState.REVERSED


def test_unitofwork_uncommitted_transaction_is_rolled_back(
    unit_of_work: AbstractUnitOfWork,
):
    with unit_of_work:
        pass

    assert unit_of_work.state == UnitOfWorkState.REVERSED


def test_unitofwork_when_error_raised_transaction_is_reversed_and_state_is_error(
    unit_of_work: AbstractUnitOfWork,
):
    with pytest.raises(Exception):
        with unit_of_work:
            raise Exception()

    assert unit_of_work.state in [UnitOfWorkState.ERROR, UnitOfWorkState.REVERSED]
