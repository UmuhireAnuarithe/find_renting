from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response


from .filters import DistrictFilter, SectorFilter, CellFilter
from .models import (Province, District, Sector, Cell, Manager, Landlord, PropertyType, Property, PropertyImages, PublishingPayment, GetInTouch, Testimonial)
from .serializers import (ProvinceSerializer, DistrictSerializer, SectorSerializer, CellSerializer, ManagerSerializer, LandlordSerializer, PropertyTypeSerializer, PropertySerializer, PropertyImagesSerializer, PublishingPaymentSerializer, GetInTouchSerializer, TestimonialSerializer)



class ProvinceViewSet(viewsets.ModelViewSet):
    serializer_class = ProvinceSerializer

    def list(self, request,):
        queryset = Province.objects.filter()
        serializer = ProvinceSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Province.objects.filter()
        province = get_object_or_404(queryset, pk=pk)
        serializer = ProvinceSerializer(province)
        return Response(serializer.data)

class DistrictViewSet(viewsets.ModelViewSet):
    serializer_class = DistrictSerializer
    # filter by district
    filter_backends = [DjangoFilterBackend]
    filterset_class = DistrictFilter
    # .

    def list(self, request, province_pk=None):
        queryset = District.objects.filter(province=province_pk)
        serializer = DistrictSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, province_pk=None):
        queryset = District.objects.filter(pk=pk, province=province_pk)
        district = get_object_or_404(queryset, pk=pk)
        serializer = DistrictSerializer(district)
        return Response(serializer.data)

class SectorViewSet(viewsets.ModelViewSet):
    serializer_class = SectorSerializer
    # filter by sector
    filter_backends = [DjangoFilterBackend]
    filterset_class = SectorFilter
    # .

    def list(self, request, province_pk=None, district_pk=None):
        queryset = Sector.objects.filter(district__province=province_pk, district=district_pk)
        serializer = SectorSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, province_pk=None, district_pk=None):
        queryset = Sector.objects.filter(pk=pk, district=district_pk, district__province=province_pk)
        sector = get_object_or_404(queryset, pk=pk)
        serializer = SectorSerializer(sector)
        return Response(serializer.data)


class CellViewSet(viewsets.ModelViewSet):
    queryset = Cell.objects.all()
    serializer_class = CellSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CellFilter
    # .

    def list(self, request, province_pk=None, district_pk=None, sector_pk=None):
        queryset = Cell.objects.filter(sector__district__province=province_pk, sector__district=district_pk, sector=sector_pk)
        serializer = SectorSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, province_pk=None, district_pk=None, sector_pk=None):
        queryset = Cell.objects.filter(pk=pk, sector__district__province=province_pk, sector__district=district_pk, sector=sector_pk)
        cell = get_object_or_404(queryset, pk=pk)
        serializer = SectorSerializer(cell)
        return Response(serializer.data)

class ManagerViewSet(viewsets.ModelViewSet):
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer
    # def get_queryset(self):
    #     return self.queryset.filter(user=self.request.user)
    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)
    # def perform_update(self, serializer):
    #     obj = self.get_object()
    #     if self.request.user!=obj.user:
    #         raise PermissionDenied(
    #             'You do not have permission to perform this action.'
    #         )
    #     serializer.save(user=self.request.user)
    # def perform_destroy(self, instance):
    #     instance.delete()

class LandlordViewSet(viewsets.ModelViewSet):
    queryset = Landlord.objects.all()
    serializer_class = LandlordSerializer
    # def get_queryset(self):
    #     return self.queryset.filter(user=self.request.user)
    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)
    # def perform_update(self, serializer):
    #     obj = self.get_object()
    #     if self.request.user!=obj.user:
    #         raise PermissionDenied(
    #             'You do not have permission to perform this action.'
    #         )
    #     serializer.save(user=self.request.user)
    # def perform_destroy(self, instance):
    #     instance.delete()

class PropertyTypeViewSet(viewsets.ModelViewSet):
    queryset = PropertyType.objects.all()
    serializer_class = PropertyTypeSerializer

class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['province', 'district', 'sector', 'cell']
    search_fields = ['title', 'description']
    ordering_fields = ['renting_price']

    @action(detail=True, methods=['get'])
    def images(self, request, pk=None):
        property_obj = self.get_object()
        serializer = PropertyImagesSerializer(property_obj.images.all(), many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(landlord=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        province = self.request.query_params.get('province', None)
        district = self.request.query_params.get('district', None)
        sector = self.request.query_params.get('sector', None)
        cell = self.request.query_params.get('cell', None)

        if province:
            queryset = queryset.filter(province=province)
        if district:
            queryset = queryset.filter(district=district)
        if sector:
            queryset = queryset.filter(sector=sector)
        if cell:
            queryset = queryset.filter(cell=cell)

        return queryset


class PropertyImagesViewSet(viewsets.ModelViewSet):
    queryset = PropertyImages.objects.all()
    serializer_class = PropertyImagesSerializer

class PublishingPaymentViewSet(viewsets.ModelViewSet):
    queryset = PublishingPayment.objects.all()
    serializer_class = PublishingPaymentSerializer

class GetInTouchViewSet(viewsets.ModelViewSet):
    queryset = GetInTouch.objects.all()
    serializer_class = GetInTouchSerializer

class TestimonialViewSet(viewsets.ModelViewSet):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer
