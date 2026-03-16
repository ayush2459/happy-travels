GST = 0.18
SECURITY_FEE = 300


def calculate_price(base, airline):

    subtotal = (
        base
        * airline["base_price_multiplier"]
        + airline["surcharge"]
        + SECURITY_FEE
    )

    gst = subtotal * GST

    return int(subtotal + gst)