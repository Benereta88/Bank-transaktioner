from Bank_transaktioner.models import Customer, Account, Transaction
from datetime import datetime

def test_transaction_links_to_accounts(db_session):
    c = Customer(
        personnummer="197001017654",
        customer_name="Bo Bertil",
        phone="0700000000",
        address="Gata 5"
    )
    db_session.add(c)
    db_session.commit()

    acc1 = Account(bank_account="SE111", customer_id=c.id)
    acc2 = Account(bank_account="SE222", customer_id=c.id)
    db_session.add_all([acc1, acc2])
    db_session.commit()

    txn = Transaction(
        transaction_id="tx1",
        timestamp=datetime.now(),
        amount=100,
        currency="USD",
        amount_sek=1050,
        sender_account_id=acc1.id,
        receiver_account_id=acc2.id,
        sender_country="SE",
        sender_municipality="Stockholm",
        receiver_country="SE",
        receiver_municipality="Göteborg",
        transaction_type="Internal",
        notes="Test"
    )
    db_session.add(txn)
    db_session.commit()

    result = db_session.query(Transaction).filter_by(transaction_id="tx1").first()
    assert result.sender_account.bank_account == "SE111"
    assert result.receiver_account.bank_account == "SE222"
