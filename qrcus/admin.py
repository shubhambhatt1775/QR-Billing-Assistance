from django.contrib import admin
from.models import author
from.models import registration
from.models import Bill
from.models import Product
from.models import Customer
from.models import Payment
from.models import Sale
# Register your models here.

admin.site.register(author)
class reg_(admin.ModelAdmin):
    list_display = ['id','fname','lname','email','address','mobile']
    search_fields =['fname','lname','email']
admin.site.register(registration,reg_)

# admin.site.register(signin)

class bill_(admin.ModelAdmin):
    list_display = ['id', 'customer', 'items_summary', 'amount', 'bill_date', 'status']
    search_fields = ['customer__email', 'items_summary']
    list_filter = ['status', 'bill_date']

admin.site.register(Bill, bill_)


# --------- Product Admin ----------
class ProductAdmin(admin.ModelAdmin):
    list_display = ('Product_id', 'Product_name', 'Quantity','Price', 'GST_percentage', 'Preset_flag')
    list_filter = ('Preset_flag',)   # filter by preset or not
    search_fields = ('Product_name',)
    list_editable = ('Price', 'GST_percentage', 'Preset_flag')  # editable in list view
    ordering = ('Product_id',)

admin.site.register(Product, ProductAdmin)

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email']
    search_fields = ['name', 'email']
    list_per_page = 20

admin.site.register(Customer, CustomerAdmin)

class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'transaction_id', 'amount', 'status', 'date']
    search_fields = ['customer__name', 'customer__email']
    list_filter = ['status', 'date']
    list_editable = ['status']  # allow changing status directly
    ordering = ['-date']
    list_per_page = 20

admin.site.register(Payment, PaymentAdmin)


class SaleAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'product_name', 'quantity', 'total_amount', 'date']
    search_fields = ['customer__name', 'product_name']
    list_filter = ['date']
    ordering = ['-date']
    list_per_page = 20

admin.site.register(Sale, SaleAdmin)


class BillAdmin(admin.ModelAdmin):
    list_display = ('bill_id', 'customer', 'amount', 'due_date', 'status')
    list_filter = ['status', 'bill_date']
    search_fields = ('bill_id', 'customer__username')


