from django.dispatch import receiver
from django.db.models.signals import post_save
from website.models import *

@receiver(post_save, sender=SellProducts)
def on_sell(sender, instance, created, **kwargs):
    if created:
        product_id = instance.product.id
        actual_quantity = instance.product.quantity
        sold_quantity = int(instance.quantity)
        remaining_quantity = actual_quantity - sold_quantity
        updateproduct = Products.objects.filter(pk=product_id).update(quantity=remaining_quantity)