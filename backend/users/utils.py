from django.conf import settings
from datetime import datetime, timedelta, timezone
import jwt


def generate_access_token(user):
	payload = {
		'user_id': user.user_id,
		'exp': datetime.now(tz=timezone.utc) + timedelta(days=1, minutes=0),
		'iat': datetime.now(tz=timezone.utc)
	}

	access_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
	return access_token