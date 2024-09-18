from django.shortcuts import render
from django.contrib.auth.models import User

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message, Notification, SendResponse


@api_view(["POST"])
def register_user(request):
    try:
        username = request.data.get('username')
        password = request.data.get('password')
        registration_token = request.data.get('registration_token')
        device_type = request.data.get('device_type')

        print(f"Registration Token: {registration_token}")

        user = User.objects.create_user(username=username, password=password)
        FCMDevice.objects.create(
            user=user, registration_id=registration_token, type="android"
        )

    except Exception as e:
        print(f"Error: {str(e)}")
        return Response({"error": "There was an error!"}, status=400)

    return Response(status=status.HTTP_200_OK)


@api_view(["POST"])
def send_notification(request):
    registration_token = request.data.get('registration_token')
    fcm_dev = FCMDevice.objects.get(registration_id=registration_token)

    # Ensure you are sending the message to the correct device
    message = Message(
        notification=Notification(
            title="Test Notification", body="This is a test notification"
        ),
        token=registration_token,
    )
    response = fcm_dev.send_message(message)
    if isinstance(response, SendResponse):
        print(f"FCM Response: {response.message_id}")  # Message ID if successful
    else:
        print(f"FCM Error: {response}")

    return Response(status=status.HTTP_200_OK)
