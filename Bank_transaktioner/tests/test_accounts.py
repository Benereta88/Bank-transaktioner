

from Bank_transaktioner.models import Customer, Account

def test_account_links_to_customer(db_session):
    customer = Customer(
        personnummer="198001019876",
        customer_name="Anna Andersson",
        phone="0707654321",
        address="Exempelgatan 2"
    )
    db_session.add(customer)
    db_session.commit()

    account = Account(
        bank_account="SE1234567890123456789012",
        customer_id=customer.id
    )
    db_session.add(account)
    db_session.commit()

    result = db_session.query(Account).filter_by(bank_account="SE1234567890123456789012").first()
    assert result.customer.customer_name == "Anna Andersson"

