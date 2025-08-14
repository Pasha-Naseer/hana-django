from django.contrib import admin
from .models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User


admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)


# create OrderItem inline
class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0


# extend Order model
class OrderAdmin(admin.ModelAdmin):
    model = Order
    inlines = [OrderItemInline]
    readonly_fields = ['date_ordered']
    fields = ['user', 'full_name', 'email', 'shipping_address', 'amount_paid', 'date_ordered', 'shipped', 'date_shipped']

admin.site.unregister(Order)
admin.site.register(Order, OrderAdmin)