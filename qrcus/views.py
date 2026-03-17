from django.shortcuts import render, redirect
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .models import registration, Bill, Product, Payment, Sale, Customer
import stripe
from decimal import Decimal

# -------- Home --------
def index(request):
    # Check if user is logged in
    user_id = request.session.get('user_id')
    fname = request.session.get('fname')
    if not user_id:
        return redirect('login')
    
    # Fetch recent bills for the registered customer
    try:
        user = registration.objects.get(id=user_id)
        customer = Customer.objects.get(email=user.email)
        recent_bills = Bill.objects.filter(customer=customer).order_by('-bill_date')[:5]
    except (registration.DoesNotExist, Customer.DoesNotExist):
        recent_bills = []

    return render(request, 'index.html', {
        'fname': fname, 
        'recent_bills': recent_bills
    })

# -------- Register --------
def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        if registration.objects.filter(email=email).exists():
            return render(request, 'register.html', {'registered': "This email is already registered.!!"})

        obj = registration(
            fname=request.POST['fname'],
            lname=request.POST['lname'],
            email=email,
            password=request.POST['password'],
            address=request.POST['address'],
            mobile=request.POST['mobile'],
            city=request.POST['city'],
            state=request.POST['state'],
            pincode=request.POST['pincode']
        )
        obj.save()
        return render(request, 'register.html', {'saved': "Registration Done Successfully!!"})
    return render(request, 'register.html')

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Using Django's built-in authenticate (requires custom User model or backend if using email)
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)  # Sets the session securely
            return redirect('index')
        else:
            messages.error(request, 'Invalid email or password')
            return render(request, 'login.html')
    
    return render(request, 'login.html')


def logout(request):
    request.session.pop('login', None)
    return redirect('index')


# -------- View Bill --------
def view_bill(request):
    if 'login' not in request.session:
        return redirect('login')
    try:
        user = registration.objects.get(email=request.session['login'])
        bills = Bill.objects.filter(user=user)
        return render(request, 'bill.html', {'bills': bills})
    except registration.DoesNotExist:
        return redirect('login')


# -------- Payment --------
def payment_page(request):
    return render(request, 'payment.html', {'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY})



def update_bill_status(request):
    if request.method == "POST":
        bill_id = request.POST.get("bill_id")
        try:
            bill = Bill.objects.get(id=bill_id)
            bill.status = "Paid"
            bill.save()
        except Bill.DoesNotExist:
            pass
    return redirect("view_bill")

# -------- Admin --------
def admin_dashboard(request):
    paid_count = Payment.objects.filter(status="Paid").count()
    pending_count = Payment.objects.filter(status="Pending").count()
    failed_count = Payment.objects.filter(status="Failed").count()
    
    return render(request, 'admin_dashboard.html', {
        'paid_count': paid_count,
        'pending_count': pending_count,
        'failed_count': failed_count
    })


# -------- Products --------
def manage_products(request):
    products = Product.objects.all()
    return render(request, 'manage_products.html', {'products': products})


def add_product(request):
    if request.method == "POST":
        Product.objects.create(
            Product_name=request.POST['Product_name'],
            Price=request.POST['Price'],
            GST_percentage=request.POST['GST_percentage'],
            Preset_flag=request.POST.get('Preset_flag') == 'on'
        )
        return redirect('manage_products')
    return render(request, 'add_product.html')


def edit_product(request, id):
    product = Product.objects.get(Product_id=id)

    if request.method == "POST":
        product.Product_name = request.POST['Product_name']
        product.Price = request.POST['Price']
        product.GST_percentage = request.POST['GST_percentage']
        product.Preset_flag = bool(request.POST.get('Preset_flag'))
        product.save()
        return redirect('manage_products')

    return render(request, 'edit_product.html', {'product': product})


def delete_product(request, id):
    try:
        product = Product.objects.get(Product_id=id)
        product.delete()
    except Product.DoesNotExist:
        pass
    return redirect('manage_products')


# -------- Users --------
def manage_users(request):
    users = registration.objects.all()
    return render(request, 'manage_users.html', {'users': users})


# -------- Payments & Sales --------

def payment_status(request):
    payments = Payment.objects.all().order_by('-date')
    
    paid_count = Payment.objects.filter(status="Paid").count()
    pending_count = Payment.objects.filter(status="Pending").count()
    failed_count = Payment.objects.filter(status="Failed").count()
    
    context = {
        'payments': payments,
        'paid_count': paid_count,
        'pending_count': pending_count,
        'failed_count': failed_count
    }
    return render(request, 'payment_status.html', context)

def sales_report(request):
    sales = Sale.objects.all().order_by('-date')
    context = {'sales': sales}
    return render(request, 'sales_report.html', context)

# -------- Preset Billing --------
def preset_billing(request):
    preset_products = Product.objects.filter(Preset_flag=True)
    return render(request, 'preset_billing.html', {'products': preset_products})

def admin_logout(request):
    logout(request)   # logs out admin user
    return render(request, 'admin_logout.html')


# Cashier Login
def cashier_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Demo credentials
        if username == "cashier" and password == "12345":
            request.session["cashier"] = username  # store session
            return redirect("cashier_dashboard")
        else:
            return render(request, "cashier_login.html", {"error": "Invalid username or password"})

    return render(request, "cashier_login.html")


# CASHIER DASHBOARD
def cashier_dashboard(request):
    # Check if cashier is logged in
    if "cashier" not in request.session:
        return redirect("cashier_login")
    return render(request, "cashier_dashboard.html")


# CASHIER LOGOUT
def cashier_logout(request):
    if "cashier" in request.session:
        del request.session["cashier"]
    return redirect("cashier_login")


from decimal import Decimal
from django.shortcuts import render, redirect
from .models import Product, Customer, Bill, Sale

def create_bill(request):
    products = Product.objects.all()
    registered_users = registration.objects.all()

    if request.method == "POST":
        customer_name = request.POST.get('customer_name')
        customer_email = request.POST.get('customer_email')

        # ✅ Check if customer is registered in registration table
        if not registration.objects.filter(email=customer_email).exists():
            return render(request, 'create_bill.html', {
                'products': products,
                'error': f"Customer with email '{customer_email}' is not registered. Only registered customers can generate bills."
            })

        # Create or get customer
        customer, created = Customer.objects.get_or_create(
            email=customer_email,
            defaults={'name': customer_name}
        )

        total_amount = Decimal('0.00')
        product_ids = request.POST.getlist('product_id')
        quantities = request.POST.getlist('quantity')

        # First, calculate total and prepare items to create Bill before Sales
        valid_items_to_process = []
        for pid, qty in zip(product_ids, quantities):
            if pid:
                try:
                    product = Product.objects.get(Product_id=pid)
                    qty = int(qty) if qty else 0
                    if qty <= 0: continue

                    price = Decimal(str(product.Price))
                    gst_amount = (price * qty * Decimal(product.GST_percentage) / 100)
                    row_amount = price * qty + gst_amount
                    total_amount += row_amount

                    valid_items_to_process.append({
                        'product': product,
                        'qty': qty,
                        'row_amount': row_amount
                    })
                except Product.DoesNotExist:
                    continue

        if not valid_items_to_process:
            return redirect('create_bill')

        # Prepare summary of items
        items_names = [item['product'].Product_name for item in valid_items_to_process]
        items_summary_str = ", ".join(items_names)

        # ✅ Apply 10% overall tax to match view logic
        final_total = total_amount * Decimal('1.10')

        # ✅ CREATE BILL FIRST
        bill = Bill.objects.create(
            customer=customer,
            amount=float(final_total),
            status="Pending",
            items_summary=items_summary_str
        )

        # ✅ CREATE PENDING PAYMENT ENTRY
        Payment.objects.create(
            customer=customer,
            amount=float(final_total),
            status="Pending"
        )

        # ✅ LINK EACH SALE TO THE BILL
        for item in valid_items_to_process:
            product = item['product']
            qty = item['qty']
            row_amount = item['row_amount']

            Sale.objects.create(
                bill=bill,  # Linked to the specific bill
                customer=customer,
                product_name=product.Product_name,
                quantity=qty,
                total_amount=float(row_amount)
            )

            # Update product stock
            product.Quantity -= qty
            product.save()

        return redirect('cashier_dashboard')

    return render(request, 'create_bill.html', {'products': products, 'registered_users': registered_users})
# Preset Items page
def cashier_preset_items(request):
    # fetch ONLY preset products added from admin
    preset_products = Product.objects.filter(Preset_flag=True)

    return render(
        request,
        'cashier_preset_items.html',
        {'preset_products': preset_products}
    )
# Payment page
def cashier_payment(request):
    # Fetch all bills sorted by date
    bills = Bill.objects.all().order_by('-id')
    return render(request, 'cashier_payment.html', {'bills': bills})


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Bill
from django.contrib.auth import logout



def customer_bill(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    
    try:
        user_reg = registration.objects.get(id=user_id)
        customer = Customer.objects.get(email=user_reg.email)
        bills = Bill.objects.filter(customer=customer).order_by('-bill_date')
    except (registration.DoesNotExist, Customer.DoesNotExist):
        bills = []
    
    return render(request, 'customer_bill.html', {'bills': bills})

def view_invoice(request, bill_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
        
    try:
        bill = Bill.objects.get(id=bill_id)
        # Ensure the bill belongs to the logged-in user
        user_reg = registration.objects.get(id=user_id)
        if bill.customer.email != user_reg.email:
            return redirect('index')
            
        items = Sale.objects.filter(bill=bill)
        
        # Calculate subtotal from items, and derive tax from the stored total amount
        subtotal = sum(item.total_amount for item in items)
        total = bill.amount
        tax = round(total - subtotal, 2)
        if tax < 0: tax = 0
        
        context = {
            'bill': bill,
            'items': items,
            'subtotal': subtotal,
            'tax': tax,
            'total': total
        }
        return render(request, 'invoice.html', context)
    except Bill.DoesNotExist:
        return redirect('index')


@login_required
def customer_payment(request):
    try:
        customer = Customer.objects.get(email=request.user.email)
        bills = Bill.objects.filter(customer=customer, paid=True)
    except Customer.DoesNotExist:
        bills = []  # or handle it however you like
    return render(request, 'customer_payment.html', {'bills': bills})

@login_required
def customer_profile(request):
    return render(request, 'customer_profile.html')

# @login_required
# def customer_logout(request):
#     logout(request)
#     return redirect('login')


@login_required(login_url='login')
def customer_logout(request):
    if request.method == "POST":
        logout(request)
        return redirect('index')  # Redirect to dashboard after logout
    return redirect('index')

# def customer_logout(request):
#     if request.method == "POST":
#         logout(request)
#         return render(request, 'customer_logout.html')
#     return redirect('index')

def scan_qr(request):
    # Only logged-in users can see their bill
    if not request.user.is_authenticated:
        messages.warning(request, "Please login first.")
        return redirect('login')

    # Fetch the first unpaid bill for the logged-in user
    bill = Bill.objects.filter(customer__email=request.user.email, status=False).select_related('customer').prefetch_related('items').first()

    if not bill:
        messages.warning(request, "No bill available.")

    # Calculate totals
    if bill:
        bill.subtotal = sum([item.quantity * item.price for item in bill.items.all()])
        bill.tax = bill.subtotal * 0.10  # 10% tax
        bill.total_amount = bill.subtotal + bill.tax

    return render(request, 'scan_qr.html', {'bill': bill})

# def scan_qr(request):
#     # If the user is not logged in, redirect to login
#     if not request.user.is_authenticated:
#         messages.warning(request, "Please login first.")
#         return redirect('login')

#     # Fetch the first unpaid bill for the logged-in user
#     bill = Bill.objects.filter(customer__email=request.user.email, status=False).select_related('customer').prefetch_related('items').first()

#     if bill:
#         # Calculate totals
#         bill.subtotal = sum([item.quantity * item.price for item in bill.items.all()])
#         bill.tax = bill.subtotal * 0.10  # 10% tax
#         bill.total_amount = bill.subtotal + bill.tax

#     return render(request, 'scan_qr.html', {'bill': bill})
def view_current_bill(request):
    # Check customer login
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    try:
        customer_reg = registration.objects.get(id=user_id)
        # Link to Customer table
        customer = Customer.objects.get(email=customer_reg.email)
    except Customer.DoesNotExist:
        return render(request, 'view_current_bill.html', {'bill': None})

    # Fetch latest pending bill
    bill = Bill.objects.filter(customer=customer, status="Pending").order_by('-bill_date').first()
    if bill:
        # ✅ Fetch items linked ONLY to this specific bill
        items = Sale.objects.filter(bill=bill)
        bill.items = items

        # Calculate breakdown based on saved amount
        subtotal = sum(item.total_amount for item in items)
        total = bill.amount
        tax = round(total - subtotal, 2)
        if tax < 0: tax = 0

        bill.subtotal = subtotal
        bill.tax = tax
        bill.total_amount = total

    return render(request, 'view_current_bill.html', {'bill': bill})

def razorpayment(request):
    currency = 'INR'

    return render(request,'razorpay.html')


# ----------------- Customer Login -----------------
from django.shortcuts import render, redirect
from .models import registration  # your custom registration model

# ----------------- Customer Login -----------------
def user_login(request):
    context = {}
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = registration.objects.get(email=email, password=password)
            # store user info in session
            request.session['user_id'] = user.id
            request.session['fname'] = user.fname
            request.session['lname'] = user.lname
            return redirect('index')  # redirect to dashboard
        except registration.DoesNotExist:
            context['login'] = "Invalid Email or Password"

    return render(request, 'login.html', context)


# ----------------- Dashboard -----------------

# # PAYMENT SUCCESS PAGE
def payment_success(request):
    payment_id = request.GET.get("payment_id")
    bill_id = request.GET.get("bill_id")

    if bill_id:
        try:
            bill = Bill.objects.get(id=bill_id)
            bill.status = "Paid"
            bill.save()
            
            # Update Payment entry
            payment = Payment.objects.filter(customer=bill.customer, status="Pending").order_by('-id').first()
            if payment:
                payment.status = "Paid"
                payment.transaction_id = payment_id
                payment.save()
            else:
                # If no pending payment exists (e.g. manual payment or direct link), create one
                Payment.objects.create(
                    customer=bill.customer,
                    amount=bill.amount,
                    status="Paid",
                    transaction_id=payment_id
                )
        except Bill.DoesNotExist:
            pass

    return render(request, "payment_success.html", {
        "payment_id": payment_id,
        "bill_id": bill_id
    })

RAZOR_KEY_ID = 'rzp_test_SO0pkfXRlta3E3'
RAZOR_KEY_SECRET = 'CtE2ct3VGPBuFFJUJFlX0fbR'

import razorpay

razorpay_client = razorpay.Client(auth=(RAZOR_KEY_ID,RAZOR_KEY_SECRET))
import razorpay
from django.conf import settings
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@csrf_exempt
def paymenthandler(request):
    if request.method == "POST":
        try:
            payment_id = request.POST.get('razorpay_payment_id', '')
            order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            bill_id = request.POST.get('bill_id') # If passed

            client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
            
            # Verify payment signature
            params_dict = {
                'razorpay_order_id': order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            client.utility.verify_payment_signature(params_dict)

            # Update bill status to Paid
            if bill_id:
                bill = Bill.objects.get(id=bill_id)
                bill.status = "Paid"
                bill.save()
                
                # Update Payment entry
                payment = Payment.objects.filter(customer=bill.customer, status="Pending").order_by('-id').first()
                if payment:
                    payment.status = "Paid"
                    payment.transaction_id = payment_id
                    payment.save()

            return JsonResponse({'status': 'Payment successful'})
        except Exception as e:
            # Optionally record as Failed Payment
            return JsonResponse({'status': 'Payment failed', 'error': str(e)})
    else:
        return JsonResponse({'status': 'Invalid request'})

def pay_now(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    try:
        user_reg = registration.objects.get(id=user_id)
        customer = Customer.objects.get(email=user_reg.email)
        # Get the latest pending bill
        bill = Bill.objects.filter(customer=customer, status="Pending").order_by('-id').first()
        
        if not bill:
            return render(request, "pay_now.html", {"error": "No pending bills found."})

        # Amount in paise
        amount_paise = int(bill.amount * 100)

        # Create Razorpay order
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        razorpay_order = client.order.create(dict(
            amount=amount_paise, 
            currency='INR', 
            payment_capture='1'
        ))

        context = {
            "razorpay_order_id": razorpay_order['id'],
            "razorpay_key": settings.RAZOR_KEY_ID,
            "amount": amount_paise,
            "display_amount": bill.amount,
            "bill": bill,
            "customer_name": user_reg.fname + " " + user_reg.lname,
            "customer_email": user_reg.email,
            "customer_mobile": user_reg.mobile
        }
        return render(request, "pay_now.html", context)

    except (registration.DoesNotExist, Customer.DoesNotExist):
        return redirect('index')
    except Exception as e:
        return render(request, "pay_now.html", {"error": str(e)})
