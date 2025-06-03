from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, autoincrement=True)
    personnummer = Column(String, unique=True, nullable=False, index=True)
    customer_name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    address = Column(String, nullable=False)
    accounts = relationship("Account", back_populates="customer")


class Account(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    bank_account = Column(String, unique=True, nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    customer = relationship("Customer", back_populates="accounts")
    sent_transactions = relationship(
        "Transaction",
        foreign_keys='Transaction.sender_account_id',
        back_populates="sender_account"
    )
    received_transactions = relationship(
        "Transaction",
        foreign_keys='Transaction.receiver_account_id',
        back_populates="receiver_account"
    )


class Transaction(Base):
    __tablename__ = "transactions"
    transaction_id = Column(String, primary_key=True)
    timestamp = Column(DateTime, nullable=False)
    amount = Column(Numeric(15, 2), nullable=False)
    currency = Column(String(3), nullable=False)
    amount_sek = Column(Numeric(15, 2), nullable=True)
    sender_account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    receiver_account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    sender_country = Column(String, nullable=False)
    sender_municipality = Column(String, nullable=False)
    receiver_country = Column(String, nullable=False)
    receiver_municipality = Column(String, nullable=False)
    transaction_type = Column(String, nullable=False)
    notes = Column(String)

    sender_account = relationship(
        "Account",
        foreign_keys=[sender_account_id],
        back_populates="sent_transactions"
    )
    receiver_account = relationship(
        "Account",
        foreign_keys=[receiver_account_id],
        back_populates="received_transactions"
    )


class SkippedTransaction(Base):
    __tablename__ = "skipped_transactions"
    transaction_id = Column(String, primary_key=True)
    timestamp = Column(DateTime, nullable=False)
    amount = Column(Numeric(15, 2), nullable=False)
    currency = Column(String(3), nullable=False)
    amount_sek = Column(Numeric(15, 2), nullable=True)  # SEK-konvertering även här
    sender_account = Column(String, nullable=False)
    receiver_account = Column(String, nullable=False)
    sender_country = Column(String, nullable=False)
    sender_municipality = Column(String, nullable=False)
    receiver_country = Column(String, nullable=False)
    receiver_municipality = Column(String, nullable=False)
    transaction_type = Column(String, nullable=False)
    notes = Column(String)
