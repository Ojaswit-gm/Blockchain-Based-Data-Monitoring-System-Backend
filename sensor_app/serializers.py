from rest_framework import serializers
from .models import Sensor, LiveSensor, Location, Block, Transaction, Mempool, TxnDB1, TxnDB2
from django.contrib.auth.models import User


class MempoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mempool
        fields = ('__all__')

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('__all__')

class TxnDB1Serializer(serializers.ModelSerializer):
    class Meta:
        model = TxnDB1
        fields = ('__all__')

class TxnDB2Serializer(serializers.ModelSerializer):
    class Meta:
        model = TxnDB2
        fields = ('__all__')

class BlockSerializer(serializers.ModelSerializer):
    txn_db_1 = TxnDB1Serializer(source='block_txnDB1', many=True, read_only=True)
    txn_db_2 = TxnDB2Serializer(source='block_txnDB2', many=True, read_only=True)
    class Meta:
        model = Block
        fields = ('__all__')


class LiveSensorSerializer(serializers.ModelSerializer):
    # user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    # is_latest = serializers.BooleanField(default=True, initial=True)
    
    class Meta:
        model = LiveSensor
        fields = ('__all__')

class SensorSerializer(serializers.ModelSerializer):
    live_sensors_set = LiveSensorSerializer(source='live_sensors', many=True, read_only=True)
    class Meta:
        model = Sensor
        fields = ('__all__')

class LocationSerializer(serializers.ModelSerializer):
    sensors_set = SensorSerializer(source='sensors', many=True, read_only=True)
    class Meta:
        model = Location
        fields = ('__all__')


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True}}






# class CustomUserSerializer(serializers.ModelSerializer):
#     resumes = ResumeSerializer(source='resume_set', many=True, read_only=True)
#     isDeleted = serializers.HiddenField(default=False)

#     class Meta:
#         model = CustomUser
#         fields = ('id', 'email', 'first_name', 'last_name', 'isDeleted', 'resumes')

#     def update(self, instance, validated_data):
#         instance.first_name = validated_data['first_name']
#         instance.last_name = validated_data['last_name']
#         instance.save()
#         return instance


# class UserRegistrationSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(required=True, write_only=True)
#     password2 = serializers.CharField(required=True, write_only=True)

#     class Meta:
#         model = CustomUser
#         fields = ('email', 'password', 'password2')

#         extra_kwargs = {
#             'password': {'write_only': True},
#             'password2': {'write_only': True},
#         }

#     def create(self, data):
#         email = data.get('email')
#         password = data.get('password')
#         password2 = data.get('password2')

#         if password == password2:
#             user = CustomUser(email=email)
#             user.set_password(password)
#             user.save()
#             return user
#         else:
#             raise serializers.ValidationError({
#                 "error": "Both passwords do not match"
#             })