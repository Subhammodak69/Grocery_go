from enum import Enum

class Role(Enum):
    ADMIN = 1
    ENDUSER = 2
    DELIVERYWORKER = 3

class PaymentMethod(Enum):
    UPI = 1
    CREDITCARD = 2
    DEBITCARD = 3
    NETBANKING = 4
    COD = 5

class PaymentStatus(Enum):
    PENDING = 1
    COMPLETED = 2
    FAILED = 3
    REFUNDED = 4

class OrderStatus(Enum):
    PENDING = 1
    PROCESSING = 2
    OUTFORDELIVERY = 3
    DELIVERED = 4
    CANCELLED = 5
    CONFIRMED = 6
    FAILED = 7
 

class ExchangeOrReturnStatus(Enum):
    PENDING = 1
    APPROVED = 2
    REJECTED = 3
    EXCHANGED = 4
    RETURNED = 5 

class DeliveryStatus(Enum):
    ASSIGNED = 1
    IN_PROGRESS = 2
    DELIVERED = 3
    FAILED = 4 
    PICKEDUP = 5

class Purpose(Enum):
    DELIVERY = 1
    PICKUP = 2

class ExOrRePurpose(Enum):
    EXCHANGE = 1
    RETURN = 2

class HelpStatus(Enum):
    PENDING = 1
    ACCEPTED = 2
    RESOLVED = 3
    FAILED = 4