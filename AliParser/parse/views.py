from django.views.generic import View
from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from .render import Render
from .parse import *


class Pdf(View):

    def get(self, request):


        merchant_products = get_products(request.GET.get('merchant'))
        seller = Seller.objects.create(url=request.GET.get('merchant'))
        seller.save()

        products_in_db = Product.objects.all().values('num')
        products_in_db = [p['num'] for p in products_in_db]

        products = []
        for prd in merchant_products:
            if prd in products_in_db:
                basic_product = Product.objects.get(num=prd)

                name = 0
                for spec in basic_product['specs']:
                    product = basic_product.copy()
                    product['id'] += '/' + str(name)
                    product['image_source'] = spec
                    products.append(product)
                    name += 1

            else:
                basic_product = get_product_info(prd)

                name = 0
                for spec in basic_product['specs']:
                    product = basic_product.copy()
                    product['id'] += '/' + str(name)
                    product['image_source'] = spec
                    products.append(product)
                    name += 1

        context = {
            'products': products,
        }

        return Render.render('pdf.html', context)
