import razorpay
from django.conf import settings
from django.shortcuts import render

def payment_view(request):
    
    client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))
    print('***********')
    print(client)
    print('***********')
    amount = 100  # Set the amount dynamically or based on your requirements
    data = {
        'amount': amount * 100,  # Razorpay expects amount in paise (e.g., 100 INR = 10000 paise)
        'currency': 'INR',
        'payment_capture': '1'  # Auto capture the payment after successful authorization
    }
    payment = client.order.create(data=data)
    print('***********')
    print(payment)
    print('***********')
    context = {
        'payment': payment,
        'amount': amount
    }
    return render(request, 'payment.html', context)

def payment_success_view(request):
    
    client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))

    order_id = request.POST.get('order_id')
    payment_id = request.POST.get('razorpay_payment_id')
    signature = request.POST.get('razorpay_signature')
    params_dict = {
        'razorpay_order_id': order_id,
        'razorpay_payment_id': payment_id,
        'razorpay_signature': signature
    }
    try:
        client.utility.verify_payment_signature(params_dict)
        # Payment signature verification successful
        # Perform any required actions (e.g., update the order status)
        return render(request, 'payment_success.html')
    except razorpay.errors.SignatureVerificationError as e:
        # Payment signature verification failed
        # Handle the error accordingly
        return render(request, 'payment_failure.html')
