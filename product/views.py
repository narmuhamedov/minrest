from rest_framework.decorators import api_view
from rest_framework.response import Response
from product.serializers import ProductSerializer
from product.models import Product
from rest_framework import status
@api_view(['GET', 'POST'])
def product_list_view(request):
    if request.method == 'GET':
        product = Product.objects.all()
        data = ProductSerializer(product, many=True).data
        return Response(data=data)
    elif request.method == 'POST':
        print(request.data)
        title = request.data.get('title')
        description = request.data.get('description')
        price = request.data.get('price')
        category_id = request.data.get('category_id')
        product = Product.objects.create(title=title, description=description, price=price,category_id=category_id)
        #Product.objects.create(title=title, description=description, price=price,category_id=category_id)
        #return Response(data={'message': 'Данные получены'})
        return Response(data=ProductSerializer(product).data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def product_detail_view(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND,
                        data={'message': 'Продукт не найден'})
    data = ProductSerializer(product).data
    return Response(data=data)



@api_view(['GET'])
def test(request):
    context = {
        'integer': 12,
        'string': 'Hello World',
        'boolean': True,
        'list': [
            1, 2, 3
        ]
    }
    return Response(data=context)
