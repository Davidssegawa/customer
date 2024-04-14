from django.conf import settings

def stripe_keys(request):
    # Make sure the settings contain the necessary Stripe keys
    if hasattr(settings, 'STRIPE_PUBLIC_KEY'):
        return {'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY}
    else:
        # Return an empty dictionary if the Stripe public key is not defined
        return {}
