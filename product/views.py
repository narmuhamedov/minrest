from rest_framework.decorators import api_view
from rest_framework.response import Response
from product.serializers import ProductSerializer, ProductCreateUpdateSerializer
from product.models import Product
from rest_framework import status
@api_view(['GET', 'POST'])
def product_list_view(request):
    if request.method == 'GET':
        product = Product.objects.all()
        data = ProductSerializer(product, many=True).data
        return Response(data=data)
    elif request.method == 'POST':
        serializer = ProductCreateUpdateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data={'errors': serializer.errors}, status=status.HTTP_406_NOT_ACCEPTABLE)
        #print(request.data)
        title = request.data.get('title')
        # if not title:
        #     return Response(data={'error': 'title not found'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        description = request.data.get('description')
        price = request.data.get('price')
        category_id = request.data.get('category_id')
        product = Product.objects.create(title=title, description=description, price=price,
                                         category_id=category_id)
        #Product.objects.create(title=title, description=description, price=price,category_id=category_id)
        #return Response(data={'message': 'Данные получены'})
        return Response(data=ProductSerializer(product).data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail_view(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND,
                        data={'message': 'Продукт не найден'})
    if request.method == "GET":
        data = ProductSerializer(product).data
        return Response(data=data)
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        product.title = request.data.get('title')
        product.description = request.data.get('description')
        product.price = request.data.get('price')
        product.category_id = request.data.get('category_id')
        product.save()
        return Response(data=ProductSerializer(product).data)



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
