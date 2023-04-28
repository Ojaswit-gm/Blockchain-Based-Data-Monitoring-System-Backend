from django.shortcuts import render
from .serializers import SensorSerializer, LiveSensorSerializer, LocationSerializer, TransactionSerializer, BlockSerializer
from .models import Sensor, Location, LiveSensor, Transaction, Mempool, Block, TxnDB1, TxnDB2
from .cryptography import encrypt, hashVerified, decryptTransactions, decrypt
from .blockchain import Wallet
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse
import ast
import random
import requests
from decouple import config
import datetime

node = Wallet()
key = 'user1key'

class BlockchainValidityAPIView(APIView):
    def get(self, request, format=None):
        blockchain = BlockSerializer(Block.objects.all(), many=True)
        result = node.is_chain_valid(blockchain.data)
        return Response(result, status=status.HTTP_200_OK)

class CorrectBlockchainAPIView(APIView):
    def get(self, request, format=None):
        try:
            # blockchain = BlockSerializer(Block.objects.all(), many=True)
            url = f"http://{config('BC_DECEN_IP', cast=str)}:{config('BC_DECEN_PORT', cast=str)}/getBlockchain/"
            x = requests.get(url)
            new_blockchain = ast.literal_eval(x.text)
            
            Block.objects.all().delete()
            for block in new_blockchain:
                index = block["index"]
                nonce = block["nonce"]
                merkle_root_hash = block["merkle_root_hash"]
                prev_hash = block["prev_hash"]
                timestamp = block["timestamp"]

                newBlock = Block(id=block['id'], index=index, nonce=nonce, merkle_root_hash=merkle_root_hash, prev_hash=prev_hash, timestamp=timestamp)
                newBlock.save()

                # Adding all the transactions of a block in blockchain
                for transaction in block["txn_db_1"]:
                        # TXN_1_DB is used
                        newTransaction = TxnDB1(block=newBlock, sensor_id=transaction['sensor_id'], data=transaction['data'], timestamp=transaction['timestamp'])
                        newTransaction.save()

                for transaction in block["txn_db_2"]:
                        # TXN_2_DB is used
                        newTransaction = TxnDB2(block=newBlock, sensor_id=transaction['sensor_id'], data=transaction['data'], timestamp=transaction['timestamp'])
                        newTransaction.save()

            return Response(new_blockchain, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(f"Error occured or replica db backend is not working - {e}", status=status.HTTP_400_BAD_REQUEST)

class GetSensorAPIView(APIView):
    sensor_serializer_class = SensorSerializer

    # Get a particular sensor
    def post(self, request, format=None):
        data = request.data
        
        sensor_id = data["sensor_id"]
        if(Sensor.objects.filter(sensor_id = sensor_id).exists()):
            req_sensor = Sensor.objects.filter(sensor_id = sensor_id).first()
            return Response(req_sensor, status=status.HTTP_200_OK)
        return Response({"Error": "No Sensor found with these credentials"}, status=status.HTTP_400_BAD_REQUEST)




# In this class, we receive data of sensors coming from Microcontrollers.
class LiveSensorAPIView(APIView):
    live_sensor_serializer_class = LiveSensorSerializer
    def post(self, request, format=None):
        res = request.data

        res['data'] = encrypt(key, str(res['data']))
        res['id'] = '4567'
        
        # return Response({"Success": "Get the data"}, status=status.HTTP_200_OK)
        # res = decrypt(res['data'])
        # res = ast.literal_eval(res)
        # hashKey = res['hashKey']

        # Checking the Hash Values Both Sides
        # if hashVerified(hashKey) is False:
        #     return Response({"Error": "Wrong Secret Key!"}, status=status.HTTP_400_BAD_REQUEST)
        
        data = res['data']
        sensor_id = res['id']
        timestamp = str(datetime.datetime.now())



        
        mempool = Mempool(data=str(data), sensor_id=sensor_id, timestamp=timestamp)
        mempool.save()

        cutOffValue = random.randint(1, 1)
        count= Mempool.objects.all().count()
        if count>=cutOffValue:
            # Mine a new block
            newBlock = node.mine_block()
            # print(newBlock)

            url = f"http://{config('BC_DECEN_IP', cast=str)}:{config('BC_DECEN_PORT', cast=str)}/storeBlockchain/"
            x = requests.post(url, json = newBlock)
            print(x.text)

        return Response({"Success": "Get the data"}, status=status.HTTP_200_OK)

class SensorAPIView(APIView):
    sensor_serializer_class = SensorSerializer

    # Get all sensors
    def get(self, request, format=None):
        all_sensors = Sensor.objects.all()
        stu_serialized = SensorSerializer(all_sensors, many=True)
        json_object = JSONRenderer().render(stu_serialized.data)
        return HttpResponse(json_object, content_type="application/Json")

    # Delete the sensor
    def delete(self, request, format=None):
        data = request.data
        sensor_id = data["sensor_id"]
        if(Sensor.objects.filter(sensor_id = sensor_id).exists()):
            req_sensor = Sensor.objects.filter(sensor_id = sensor_id).first()
            req_sensor.delete()
            location = Location.objects.all()
            loc_serialized = LocationSerializer(location, many=True)
            return Response(loc_serialized.data, status=status.HTTP_200_OK)
        return Response("No Sensor found with this ID", status=status.HTTP_400_BAD_REQUEST)

    # API to add/update a new sensor
    def post(self, request, format=None):
        data = request.data
        name = data['name']
        id = data['sensor_id']
        unit = data['unit']
        locationID = data['locationID']

        # Checking the exixting of a sensor
        if Sensor.objects.filter(sensor_id = id).exists():
            if(Location.objects.filter(locId = locationID).exists()):
                location = Location.objects.filter(locId = locationID).first()
                sensor = Sensor.objects.filter(sensor_id=id).first()
                sensor.location = location
                sensor.name = name
                sensor.unit = unit
                sensor.save()
                return Response("Data Updated Succesfully", status=status.HTTP_200_OK)
            else:
                return Response("No Location found with this ID", status=status.HTTP_400_BAD_REQUEST)
        else:
            # Check locationID is correct or not
            if(Location.objects.filter(locId = locationID).exists()):
                location = Location.objects.filter(locId = locationID).first()
                sensor = Sensor(location=location, name=name, sensor_id=id, unit=unit)
                sensor.save()
                return Response("Sensor added succesfully", status=status.HTTP_200_OK)
            else:
                print("No Location found with this ID")
                return Response("No Location found with this ID", status=status.HTTP_400_BAD_REQUEST)
            
    
    # API to update the sensor data
    def put(self, request, format=None):
        data = request.data
        sensor_serializer = self.sensor_serializer_class(data=data)
        if sensor_serializer.is_valid():
            sensor_serializer.save()
            return Response(sensor_serializer, status=status.HTTP_200_OK)
        else:
            return Response(sensor_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LocationAPIView(APIView):
    location_serializer_class = LocationSerializer

    # Get all locations
    def get(self, request, format=None):
        all_locations = Location.objects.all()
        loc_serialized = LocationSerializer(all_locations, many=True).data
        
        for location in loc_serialized:
            for sensor in location['sensors_set']:
                if(int(sensor['sensor_id']) <= config('TXN_1_DB_LIMIT', cast=int)):
                    txnDB1 = TxnDB1.objects.all()
                    for transaction in txnDB1:
                        if(sensor['sensor_id'] == transaction.sensor_id):
                            sensor['live_sensors_set'].append({"sensor_id": transaction.sensor_id, "data": transaction.data, "timestamp": transaction.timestamp})
                else:
                    txnDB2 = TxnDB2.objects.all()
                    for transaction in txnDB2:
                        if(sensor['sensor_id'] == transaction.sensor_id):
                            sensor['live_sensors_set'].append({"sensor_id": transaction.sensor_id, "data": transaction.data, "timestamp": transaction.timestamp})

        return Response(loc_serialized, status=status.HTTP_200_OK)

    # Delete the location
    def delete(self, request, format=None):
        data = request.data
        sensor_id = data["sensor_id"]
        if(Sensor.objects.filter(sensor_id = sensor_id).exists()):
            req_sensor = Sensor.objects.filter(sensor_id = sensor_id).first()
            req_sensor.delete()
            all_sensors = Sensor.objects.all()
            stu_serialized = SensorSerializer(all_sensors, many=True)
            return Response(stu_serialized.data, status=status.HTTP_200_OK)
        return Response({"Error": "No Sensor found with this ID"}, status=status.HTTP_400_BAD_REQUEST)

    # API to add a new location
    def post(self, request, format=None):
        data = request.data
        # print(data)
        location_serializer = self.location_serializer_class(data=data)
        if location_serializer.is_valid():
            location_serializer.save()
            return Response(location_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(location_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # API to update the location data
    def put(self, request, format=None):
        data = request.data
        sensor_serializer = self.sensor_serializer_class(data=data)
        if sensor_serializer.is_valid():
            sensor_serializer.save()
            return Response(sensor_serializer, status=status.HTTP_200_OK)
        else:
            return Response(sensor_serializer.errors, status=status.HTTP_400_BAD_REQUEST)