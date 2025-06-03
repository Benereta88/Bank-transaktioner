from Bank_transaktioner.models import SkippedTransaction
from datetime import datetime

def test_skipped_transaction_saves_correctly(db_session):
    txn = SkippedTransaction(
        transaction_id="skipped_tx1",
        timestamp=datetime.now(),
        amount=200,
        currency="EUR",
        sender_account="SE0001",
        receiver_account="SE0002",
        sender_country="NO",
        sender_municipality="Oslo",
        receiver_country="FI",
        receiver_municipality="Helsinki",
        transaction_type="Failed",
        notes="Missing accounts"
    )
    db_session.add(txn)
    db_session.commit()

    result = db_session.query(SkippedTransaction).filter_by(transaction_id="skipped_tx1").first()
    assert result.currency == "EUR"
    assert result.sender_account == "SE0001"
