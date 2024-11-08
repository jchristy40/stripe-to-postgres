"""Stripe analytics source settings and constants"""

# the most popular endpoints
# Full list of the Stripe API endpoints you can find here: https://stripe.com/docs/api.
ENDPOINTS = (
    "Subscription",
    "Account",
    "Coupon",
    "Customer",
    "Product",
    "Price",
    "PromotionCode"
)
# possible incremental endpoints
INCREMENTAL_ENDPOINTS = ("Invoice", "BalanceTransaction", "Refund", "Charge")
