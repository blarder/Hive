from rest_framework import generics
from rest_framework.views import Response, APIView, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from .models import SMSDevice, GCMDevice, APNSDevice
from .serializers import GCMDeviceSerializer, APNSDeviceSerializer, SMSDeviceSerializer
from uuid import UUID


class MyDevicesList(APIView):

    permission_classes = (IsAuthenticated, )

    serializer_map = {
        'APNS': APNSDeviceSerializer,
        'GCM': GCMDeviceSerializer,
        'SMS': SMSDeviceSerializer
    }

    def get(self, request, format=None):

        my_apnsdevices = APNSDevice.objects.filter(user=request.user)
        my_smsdevices = SMSDevice.objects.filter(user=request.user)
        my_gcmdevices = GCMDevice.objects.filter(user=request.user)

        apns_serializer = APNSDeviceSerializer(my_apnsdevices, many=True)
        sms_serializer = SMSDeviceSerializer(my_smsdevices, many=True)
        gcm_serializer = GCMDeviceSerializer(my_gcmdevices, many=True)

        return Response(apns_serializer.data + sms_serializer.data + gcm_serializer.data,
                        status=status.HTTP_200_OK)


class APNSDeviceList(generics.ListCreateAPIView):

    serializer_class = APNSDeviceSerializer
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        return APNSDevice.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):

        request.DATA['user'] = request.user.id

        try:
            obj = APNSDevice.objects.get(device_id=UUID(request.DATA['device_id']))
            serializer = APNSDeviceSerializer(obj, request.DATA, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except (APNSDevice.DoesNotExist, ValueError, KeyError):

            return super().post(request, *args, **kwargs)


class APNSDeviceDetail(generics.RetrieveAPIView):

    serializer_class = APNSDeviceSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return APNSDevice.objects.filter(user=self.request.user)


class SMSDeviceList(generics.ListCreateAPIView):

    serializer_class = SMSDeviceSerializer
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def pre_save(self, obj):
        obj.user = self.request.user

    def get_queryset(self):
        return SMSDevice.objects.filter(user=self.request.user)


class SMSDeviceDetail(generics.RetrieveAPIView):

    serializer_class = SMSDeviceSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return SMSDevice.objects.filter(user=self.request.user)


class GCMDeviceList(generics.ListCreateAPIView):

    serializer_class = GCMDeviceSerializer
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        return GCMDevice.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):

        request.DATA['user'] = request.user.id

        try:
            obj = GCMDevice.objects.get(device_id=request.DATA['device_id'])
            serializer = GCMDeviceSerializer(obj, request.DATA, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except (GCMDevice.DoesNotExist, ValueError, KeyError):

            return super().post(request, *args, **kwargs)


class GCMDeviceDetail(generics.RetrieveAPIView):

    serializer_class = GCMDeviceSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return GCMDevice.objects.filter(user=self.request.user)
