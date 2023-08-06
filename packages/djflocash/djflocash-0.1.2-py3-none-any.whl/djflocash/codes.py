import pycountry


COUNTRY_CODES = [c.alpha_2 for c in pycountry.countries]
COUNTRY_LABEL = {c.alpha_2: c.name for c in pycountry.countries}

CURRENCY_CODES = [c.alpha_3 for c in pycountry.currencies]
CURRENCY_LABEL = {c.alpha_3: c.name for c in pycountry.currencies}

STATUS_LABEL = {
    "0000": "Payment is successful.",
    "0001": "Payment was aborted.",
    "0002": "Customer cancelled the payment.",
    "0003": "Transaction was not authorized.",
    "0004": "Payment is pending.",
}

#: status known to mean payment is ok
PAID_STATUS = {0}
#: status known to mean payment is not ok
UNPAID_STATUS = {1, 2, 3}
#: status known to mean payment is pending, further notification expected
PENDING_STATUS = {4}
#: resolved status, all but pendings
RESOLVED_STATUS = PAID_STATUS | UNPAID_STATUS
