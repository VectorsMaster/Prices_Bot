from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Product
from .serializer import (
    ProductSerializer,
    ProductAdminSerializer,
)

class ProductDetailAPIView(generics.RetrieveAPIView):
    permission_classes = []
    authentication_classes = []
    lookup_field = 'pk'
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductUpdateAPIView(generics.UpdateAPIView):
    permission_classes = []
    authentication_classes = []
    lookup_field = 'pk'
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def put(self, request, pk=None, *args, **kwargs):
        print(f"Put request: pk={pk}")
        if pk is None:
            return Response({"details": "bad request"},status.HTTP_400_BAD_REQUEST)
        try:
            instance = Product.objects.get(id=pk)
        except Product.DoesNotExist:
            return Response({"details": "instance with this key does not exist"}, status=status.HTTP_404_NOT_FOUND)

        new_pk = request.data.get('id')
        if new_pk != pk:
            return Response({"details: You can not modify product key"},status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def patch(self, request, pk=None, *args, **kwargs):
        return self.put(request, pk, args, kwargs)

class ProductCreateAPIView(generics.CreateAPIView):
    permission_classes = []
    authentication_classes = []
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CategoryListAPIView(generics.ListAPIView):
    permission_classes = []
    authentication_classes = []
    def get(self, request, *args, **kwargs):
        distinct_values = Product.objects.values('category').distinct()
        values_list = list(distinct_values)
        print(values_list)
        return Response({},status=status.HTTP_200_OK)

class ProductListAPIView(generics.ListAPIView):
    permission_classes = []
    authentication_classes = []
    def get(self, request, *args, **kwargs):
        prod_category = request.GET.get('category')
        prod_description = request.GET.get('description')
        prod_vehicle_type = request.GET.get('vehicle_type')

        if prod_description == '?' or prod_description is None:
            prod_description = ''
        
        print(f"Product Category: {prod_category}, Prodcut Description: {prod_description}")
        queryset = Product.objects.filter(name__icontains=prod_description)

        if prod_category is not None:
            queryset = queryset.filter(category=prod_category)
        
        if prod_vehicle_type is not None:
            queryset = queryset.filter(vehicle_type=prod_vehicle_type)

        print(queryset)
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)


class ProductAdminListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def get(self, request, *args, **kwargs):
        prod_category = request.GET.get('category')
        prod_description = request.GET.get('description')
        prod_vehicle_type = request.GET.get('vehicle_type')

        if prod_description == '?' or prod_description is None:
            prod_description = ''
        
        print(f"Product Category: {prod_category}, Prodcut Description: {prod_description}")
        queryset = Product.objects.filter(name__icontains=prod_description)

        if prod_category is not None:
            queryset = queryset.filter(category=prod_category)
        
        if prod_vehicle_type is not None:
            queryset = queryset.filter(vehicle_type=prod_vehicle_type)
        
        print(queryset)
        serializer = ProductAdminSerializer(queryset, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

import pandas as pd
from . import naming
class FileHandleAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        file_path = request.data.get('file_path')
        if file_path is None:
            return Response({},status.HTTP_400_BAD_REQUEST)
        print(file_path)
        
        try:
            df = pd.read_excel(file_path)
        except Exception as e:
            print(e)
            return Response({"details": "couldn't read the file"}, status.HTTP_400_BAD_REQUEST)
        
        row_id = 0
        for row in df.iloc:
            print(row[naming.product_id], row[naming.product_name], row[naming.product_price])
            try:
                product_id = int(row[naming.product_id])
            except:
                print(f"Invalid id in row {row_id}")
                continue
            try:
                prod = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                prod = None

            if prod is None:
                print("This product does not exist")
                prod = Product.objects.create(id=product_id,category='new_category',price=0.0,price_sp=0.0,name='new_name')
            
            try:
                prod.price = float(row[naming.product_price])
            except: 
                prod.price = 0.0
            try:
                prod.category = row[naming.product_category]
            except:
                prod.category = 'قطع غيار'
            
            try:
                prod.name = row[naming.product_name]
            except:
                prod.name = 'قطعة جديدة'

            prod.price_sp = prod.price

            try:
                prod.vehicle_type = row[naming.product_vehicle_type]
            except:
                prod.vehicle_type = 'سايبا'
            
            try:
                prod.quantity = int(row[naming.product_quantity])
            except:
                prod.quantity = 0

            prod.save()

        return Response({},status=status.HTTP_200_OK)