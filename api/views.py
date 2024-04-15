import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.firebase_config import usersCollection
from api.services import send_email, get_user_by_email, generate_otp


@api_view(['POST'])
def send_email_from_dashboard(request):
    try:
        data = json.loads(request.body)
        if not data.get('message') or not data.get('subject'):
            return Response({"status": False, "error": "Missing required fields"}, status=403)

        subject = data.get('subject')
        message = data.get('message')
        email = data.get('email')

        if email is None:
            return Response({"status": False, "error": "email is required"}, status=403)

        value = send_email(subject=subject, body=message, email=email)
        if value is True:
            return Response({"status": True, "message": f"emails sent successfully to {email}"}, status=200)

        return Response({"status": False, "error": "Error sending email", 'reason': value}, status=403)

    except Exception as e:
        return Response({'status': False, 'error': str(e)}, status=500)


@api_view(['POST'])
def request_otp(request):
    try:
        data = json.loads(request.body)
        email = data.get('email')
        user = get_user_by_email(email)
        if not user:
            return Response({'status': False, "error": "User does not exist"}, status=404)

        new_otp = generate_otp(6)
        result = send_email("Forgot Password Request", f"Your OTP code is: {new_otp}", email)
        if result is not True:
            return Response({'status': False, "error": "error sending email please try again later"}, status=500)

        usersCollection.document(user.get('id')).update({'otp': new_otp})
        return Response({"status": True}, status=200)
    except Exception as e:
        return Response({"status": False, "error": str(e)}, status=500)


@api_view(['POST'])
def verify_otp(request):
    try:
        data = json.loads(request.body)
        email = data.get('email')
        otp = data.get('otp')
        user = get_user_by_email(email)
        if not user:
            return Response({'status': False, "error": "User does not exist"}, status=404)

        if not user.get('otp') == otp:
            return Response({'status': False, "error": "otp incorrect"}, status=404)
        usersCollection.document(user.get('id')).update({'otp': None})
        return Response({"status": True}, status=200)
    except Exception as e:
        return Response({"status": False, "error": str(e)}, status=500)



