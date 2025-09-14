import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from orders.models import Order, Payment

stripe.api_key = getattr(settings, 'STRIPE_SECRET_KEY', '')

@login_required
def create_payment_intent(request):
    """Create a payment intent for Stripe"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            order_id = data.get('order_id')

            order = Order.objects.get(id=order_id, user=request.user)

            # Create payment intent
            intent = stripe.PaymentIntent.create(
                amount=int(order.final_total * 100),  # Convert to cents
                currency='usd',
                metadata={
                    'order_id': order.id,
                    'user_id': request.user.id,
                }
            )

            return JsonResponse({
                'client_secret': intent.client_secret,
                'amount': order.final_total
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
@require_POST
def stripe_webhook(request):
    """Handle Stripe webhook events"""
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = getattr(settings, 'STRIPE_ENDPOINT_SECRET', '')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError:
        return JsonResponse({'error': 'Invalid payload'}, status=400)
    except stripe.error.SignatureVerificationError:
        return JsonResponse({'error': 'Invalid signature'}, status=400)

    # Handle the event
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']

        # Update order status
        order_id = payment_intent['metadata']['order_id']
        try:
            order = Order.objects.get(id=order_id)

            # Create payment record
            payment = Payment.objects.create(
                user=order.user,
                payment_id=payment_intent['id'],
                payment_method='Stripe',
                amount_paid=payment_intent['amount'] / 100,  # Convert back from cents
                status='Completed'
            )

            # Update order
            order.payment = payment
            order.is_ordered = True
            order.status = 'Accepted'
            order.save()

        except Order.DoesNotExist:
            pass

    return JsonResponse({'status': 'success'})

@login_required
def payment_success(request):
    """Payment success page"""
    return render(request, 'payments/success.html')

@login_required
def payment_cancelled(request):
    """Payment cancelled page"""
    return render(request, 'payments/cancelled.html')
