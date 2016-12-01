"""
We include here configurations to be shared between the crypto library
components.
"""

# cryptography suggests this value for
# the public exponent, stating that "65537 should almost always be used"
# However, 65537 is the most used value if we use a lower value with a good
# padding scheme we don't loose any security and gain more performance
# Using e=3 might improve performance by 8x
PUBLIC_EXPONENT = 65537

KEY_SIZE = 2048
