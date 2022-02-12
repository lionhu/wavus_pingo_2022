from urllib.parse import parse_qs
from django.conf import settings
from pingo.conf import settings as pingo_settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections
from channels.db import database_sync_to_async
import jwt
from datetime import timedelta as td
from django.utils import timezone
from django.db.models.expressions import F
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.cache import cache
from .models import LoggedInUser
import json
import logging

logger = logging.getLogger("error_logger")

User = get_user_model()


@database_sync_to_async
def get_user(token):
    close_old_connections()
    token_info = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    try:
        user = User.objects.get(id=token_info['user_id'])
    except Exception as exception:
        return AnonymousUser()
    if not user.is_active:
        return AnonymousUser()
    return user


class TokenAuthMiddleware:

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        query_string = parse_qs(scope['query_string'].decode())
        token = query_string.get('token')
        if not token:
            scope['user'] = AnonymousUser()
        else:
            scope['user'] = await get_user(token[0])

        print("user", scope['user'])
        return await self.app(scope, receive, send)


class LastUserActivityMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            try:
                print("IP WEB location")
                print(request.ipinfo.ip)
                print(request.ipinfo.country)
                print(request.ipinfo.country_name)
                print(request.ipinfo.loc)
                session_last_activity = request.session.get("last-activity")
                last_activity = json.loads(session_last_activity)
                print(last_activity)
                # If key is old enough, update database.
                too_old_time = timezone.now() - td(seconds=pingo_settings.LAST_ACTIVITY_INTERVAL_SECS)
                if not last_activity or last_activity < too_old_time:
                    last_location = {
                        "ip": request.ipinfo.ip,
                        "country": request.ipinfo.country,
                        "city": request.ipinfo.city,
                        "loc": request.ipinfo.loc,
                    }

                    User.objects.filter(pk=request.user.pk).update(
                        last_login=timezone.now(),
                        login_count=F('login_count') + 1,
                        last_location=last_location)

                request.session["last-activity"] = json.dumps(timezone.now())
                print("update authenticated user last_login")
            except Exception as err:
                pass

        return None


class PingoJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        print("Pingo JWTauthentication")

        header = self.get_header(request)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)
        user = self.get_user(validated_token)

        try:
            print("IP JWT location")
            last_login_in_redis_key = str(pingo_settings.USER_LAST_LOGIN).format(user.id)
            redis_key = cache.get(last_login_in_redis_key, None)
            print(redis_key)
            if redis_key is None:
                last_location = {
                    "ip": request.ipinfo.ip,
                    "country": request.ipinfo.country,
                    "city": request.ipinfo.city,
                    "loc": request.ipinfo.loc,
                }
                user.last_login = timezone.now()
                user.login_count += 1
                user.last_location = last_location
                user.save()

                LoggedInUser.objects.update_or_create(user=user, defaults={
                    "web": True
                })
                print("Pingo update user last_login_in")
                cache.set(last_login_in_redis_key, user.last_login, pingo_settings.LAST_ACTIVITY_INTERVAL_SECS)

        except Exception as err:
            pass
        return user, validated_token
