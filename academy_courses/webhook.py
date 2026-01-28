from django.views.decorators.csrf import csrf_exempt
import stripe
import academy.settings as settings
from django.http import HttpResponse
from .models import Transaction, Order, Course
from accounts.models import Profile


@csrf_exempt
def stripe_webhook(request):
    print('Stripe webhook')
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_ENDPOINT_SECRET
        )
    except ValueError as e:
        print('Invalid payload')
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        print('Invalid signature')
        return HttpResponse(status=400)

    # Handle the event
    if event.type == 'payment_intent.succeeded':
        payment_intent = event.data.object
        print('payment_intent.succeeded')
        transaction_id = payment_intent.metadata.transaction
        make_order(transaction_id)
        print(payment_intent.metadata)
    # ... handle other event types
    else:
        print('Unhandled event type {}'.format(event['type']))
    return HttpResponse(status=200)



def make_order(transaction_id):
    transaction = Transaction.objects.get(pk=transaction_id)
    order = Order.objects.create(transaction=transaction)
   
    
    if transaction.user.profile.courses is None:
        transaction.user.profile.courses = [order.transaction.course_id]
        transaction.user.profile.save()
    elif transaction.user.profile.courses and order.transaction.course_id not in transaction.user.profile.courses:
        transaction.user.profile.courses.append(order.transaction.course_id)
        transaction.user.profile.save()


    order.orderproduct_set.create(
        course_id=transaction.course_id,
        price=transaction.course.price
    )