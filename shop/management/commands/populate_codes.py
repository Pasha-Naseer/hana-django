from django.core.management.base import BaseCommand
from shop.models import Product, ProductCode
from django.utils import timezone


class Command(BaseCommand):
    help = 'Populate the database with test products'

    def handle(self, *args, **kwargs):
        count = 10  # Number of test products to create
        codes_to_create = []
        self.stdout.write(f'Creating {count} test product codes...')

        for i in Product.objects.all():
            for j in range(1, count + 1):
                code = ProductCode(
                    code=j,
                    product=i,
                )
                codes_to_create.append(code)

        print(codes_to_create)
        # Bulk create for high performance
        ProductCode.objects.bulk_create(codes_to_create)

        self.stdout.write(self.style.SUCCESS(f'Successfully created {count} product codes!'))
