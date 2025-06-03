from Bank_transaktioner.models import Customer

def test_create_customer(db_session):
    customer = Customer(
        personnummer="199001019999",
        customer_name="Test Testsson",
        phone="0701234567",
        address="Testvägen 1"
    )
    db_session.add(customer)
    db_session.commit()

    result = db_session.query(Customer).filter_by(personnummer="199001019999").first()
    assert result.customer_name == "Test Testsson"

