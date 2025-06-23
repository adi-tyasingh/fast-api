import os
from datetime import datetime
from enum import Enum as PyEnum
from typing import List, Optional

from dotenv import load_dotenv
from sqlalchemy import (
    URL,
    Boolean,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    Numeric,
    String,
    UniqueConstraint,
)
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

load_dotenv("../.env")

url_object = URL.create(
    "postgresql+asyncpg",
    username=os.getenv("USERNAME"),
    password=os.getenv("PASSWORD"),
    host=os.getenv("HOST"),
    port=int(os.getenv("PORT")),
    database=os.getenv("DB"),
)

engine = create_async_engine(url_object, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class OrderStatus(PyEnum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"


class OfferCode(Base):
    __tablename__ = "offercode"

    id: Mapped[str] = mapped_column(String(10), primary_key=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    flat: Mapped[float] = mapped_column(Numeric(3, 2))
    percent: Mapped[int] = mapped_column(Numeric(2, 0))

    orders: Mapped[List["Order"]] = relationship(back_populates="offercode")


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    author: Mapped[str] = mapped_column(String(100))
    quantity: Mapped[int] = mapped_column(Integer)
    price: Mapped[float] = mapped_column(Numeric(5, 2))

    order_items: Mapped[List["OrderItem"]] = relationship(back_populates="book")


class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint("email", name="uq_users_email"),
        UniqueConstraint("number", name="uq_users_number"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    number: Mapped[str] = mapped_column(String(10), nullable=False)

    orders: Mapped[List["Order"]] = relationship(back_populates="user")


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    time: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    status: Mapped[OrderStatus] = mapped_column(
        Enum(OrderStatus), default=OrderStatus.PENDING
    )
    offercode_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey("offercode.id"), nullable=True
    )
    total: Mapped[float] = mapped_column(Numeric(5, 2))

    user: Mapped["User"] = relationship(back_populates="orders")
    offercode: Mapped[Optional["OfferCode"]] = relationship(back_populates="orders")
    items: Mapped[List["OrderItem"]] = relationship(back_populates="order")


class OrderItem(Base):
    __tablename__ = "order_items"
    __table_args__ = (UniqueConstraint("order_id", "book_id", name="pk_order_items"),)

    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"), primary_key=True)
    quantity: Mapped[int]
    unit_price: Mapped[float] = mapped_column(Numeric(5, 2))

    order: Mapped["Order"] = relationship(back_populates="items")
    book: Mapped["Book"] = relationship(back_populates="order_items")
