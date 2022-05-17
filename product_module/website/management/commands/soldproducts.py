from django.core.management.base import BaseCommand
from website.models import *
from django.core import serializers 
import csv

class Command(BaseCommand):
    help = "Create CSV of Entered month...!"

    def add_arguments(self, parser):
        parser.add_argument('param', type=int)

    def handle(self, *args, **options):
        param = options.get('param')
        date = SellProducts.objects.filter(date__month=param)
        if date:
            with open(f"soldproducts_in_{param}th_month.csv","w") as c:
                writer = csv.writer(c)
                writer.writerow(["user", "product", "quantity", "total_price", "date"])
                for i in date:
                    writer.writerow([i.user, i.product.product_name, i.quantity, i.total_price, i.date])
                    print("------------------>", i)
        else:
            print("------------------> Nothing Sold in this month...!")