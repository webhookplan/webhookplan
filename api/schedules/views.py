# Django
from rest_framework import views, request, response, status

# Swagger Modules
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

# Custom
from django_celery_beat import models as django_celery_beat_models
from schedules import serializers as schedule_serializers
from utils.responses import GET_RESPONSES, POST_RESPONSES
from tasks.webhook import make_wehbook_request

from pytz import all_timezones
import json


class ScheduleCrudApi(views.APIView):
    model_class = django_celery_beat_models.PeriodicTask
    serializer_class = schedule_serializers.PeriodicTaskSerializer

    @swagger_auto_schema(
        responses=GET_RESPONSES,
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_="query",
                type=openapi.TYPE_INTEGER,
            ),
        ],
    )
    def get(self, request: request.Request, *args, **kwargs):
        id = request.query_params.get("id", None)

        qs = self.model_class.objects.all().order_by("-id")

        if id:
            qs = qs.filter(id=id)

        output = self.serializer_class(qs, many=True).data
        return response.Response(output, status.HTTP_200_OK)

    @swagger_auto_schema(
        responses=POST_RESPONSES,
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["name", "webhook"],
            properties={
                "name": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Short Description For This Task",
                ),
                "description": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Detailed description about the details of this Periodic Task",
                ),
                "interval": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    required=["every", "period"],
                    properties={
                        "every": openapi.Schema(
                            type=openapi.TYPE_INTEGER,
                            description="Number of interval periods to wait before running the task again",
                            default=2,
                        ),
                        "period": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="The type of period between task runs (Example: days)",
                            default="days",
                            enum=[
                                "days",
                                "hours",
                                "minutes",
                                "seconds",
                                "microseconds",
                            ],
                        ),
                    },
                ),
                "crontab": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    required=[
                        "minute",
                        "hour",
                        "day_of_week",
                        "day_of_month",
                        "month_of_year",
                        "timezone",
                    ],
                    properties={
                        "minute": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Cron Minutes to Run. Use '*' for 'all'. (Example: '0,30')",
                            default="*",
                        ),
                        "hour": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='Cron Hours to Run. Use "*" for "all". (Example: "8,20")',
                            default="*",
                        ),
                        "day_of_week": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='Cron Days Of The Week to Run. Use "*" for "all", Sunday is 0 or 7, Monday is 1. (Example: "0,5")',
                            default="*",
                        ),
                        "day_of_month": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='Cron Days Of The Month to Run. Use "*" for "all". (Example: "1,15")',
                            default="*",
                        ),
                        "month_of_year": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='Cron Months (1-12) Of The Year to Run. Use "*" for "all". (Example: "1,12")',
                            default="*",
                        ),
                        "timezone": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Timezone to Run the Cron Schedule on. Default is UTC.",
                            default="UTC",
                            enum=[i for i in all_timezones],
                        ),
                    },
                ),
                "solar": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    required=["every", "latitude", "longitude"],
                    properties={
                        "event": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="The type of solar event when the job should run",
                            default="sunrise",
                            enum=[
                                "dawn_astronomical",
                                "dawn_civil",
                                "dawn_nautical",
                                "dusk_astronomical",
                                "dusk_civil",
                                "dusk_nautical",
                                "solar_noon",
                                "sunrise",
                                "sunset",
                            ],
                        ),
                        "latitude": openapi.Schema(
                            type=openapi.TYPE_NUMBER,
                            description="Run the task when the event happens at this latitude",
                            default=0,
                        ),
                        "longitude": openapi.Schema(
                            type=openapi.TYPE_NUMBER,
                            description="Run the task when the event happens at this longitude",
                            default=0,
                        ),
                    },
                ),
                "clocked": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    required=["clocked_time"],
                    properties={
                        "clocked_time": openapi.Schema(
                            type=openapi.FORMAT_DATETIME,
                            description="Run the task at clocked time",
                        ),
                    },
                ),
                "expires": openapi.Schema(
                    type=openapi.FORMAT_DATETIME,
                    description="Datetime after which the schedule will no longer trigger the task to run",
                ),
                "expire_seconds": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="Timedelta with seconds which the schedule will no longer trigger the task to run",
                ),
                "one_off": openapi.Schema(
                    type=openapi.TYPE_BOOLEAN,
                    description="If True, the schedule will only run the task a single time",
                ),
                "start_time": openapi.Schema(
                    type=openapi.FORMAT_DATETIME,
                    description="Datetime when the schedule should begin triggering the task to run",
                ),
                "enabled": openapi.Schema(
                    type=openapi.TYPE_BOOLEAN,
                    description="Set to False to disable the schedule",
                ),
                "webhook": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    required=["url", "method"],
                    properties={
                        "url": openapi.Schema(type=openapi.TYPE_STRING),
                        "method": openapi.Schema(
                            type=openapi.TYPE_STRING, default="GET"
                        ),
                        "query": openapi.Schema(type=openapi.TYPE_OBJECT),
                        "payload": openapi.Schema(type=openapi.TYPE_OBJECT),
                        "headers": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "Content-Type": openapi.Schema(
                                    type=openapi.TYPE_STRING, default="application/json"
                                ),
                            },
                        ),
                    },
                ),
            },
        ),
    )
    def post(self, request: request.Request, *args, **kwargs):
        data = request.data

        name = data.get("name", None)
        description = data.get("description", None)

        interval = data.get("interval", None)
        crontab = data.get("crontab", None)
        solar = data.get("solar", None)
        clocked = data.get("clocked", None)

        expires = data.get("expires", None)
        expire_seconds = data.get("expire_seconds", None)
        one_off = data.get("one_off", None)
        start_time = data.get("start_time", None)
        enabled = data.get("enabled", None)

        webhook: dict = data.get("webhook", {})

        # name is required
        if not name:
            return response.Response(
                {"details": "name is required"}, status.HTTP_400_BAD_REQUEST
            )

        # shoud send atleast ONE of the following schedules
        if not any([interval, crontab, solar, clocked]):
            return response.Response(
                {
                    "details": "Either of interval, crontab, solar or clocked are reqired"
                },
                status.HTTP_400_BAD_REQUEST,
            )

        # Should only send ONE of the following schedules
        if sum(bool(x) for x in [interval, crontab, solar, clocked]) > 1:
            return response.Response(
                {
                    "details": "Either of interval, crontab, solar or clocked are reqired"
                },
                status.HTTP_400_BAD_REQUEST,
            )

        # validate webhook data
        webhook_data = {
            "pt_name": name,
            "url": webhook.get("url", None),
            "method": webhook.get("method", "GET"),
            "query": webhook.get("query", {}),
            "payload": webhook.get("payload", None),
            "headers": webhook.get("headers", {}),
        }
        webhook_serializer = schedule_serializers.WebhookSerializer(data=webhook_data)
        if not webhook_serializer.is_valid():
            return response.Response(
                webhook_serializer.errors, status.HTTP_400_BAD_REQUEST
            )

        # validate and save interval data
        interval_instance = None
        if interval:
            interval_serializer = schedule_serializers.IntervalScheduleSerializer(
                data=interval
            )
            if not interval_serializer.is_valid():
                return response.Response(
                    interval_serializer.errors, status.HTTP_400_BAD_REQUEST
                )
            interval_instance = interval_serializer.save()

        # validate and save crontab data
        crontab_instance = None
        if crontab:
            crontab_serializer = schedule_serializers.CrontabScheduleSerializer(
                data=crontab
            )
            if not crontab_serializer.is_valid():
                return response.Response(
                    crontab_serializer.errors, status.HTTP_400_BAD_REQUEST
                )
            crontab_instance = crontab_serializer.save()

        # validate and save solar data
        solar_instance = None
        if solar:
            solar_serializer = schedule_serializers.SolarScheduleSerializer(data=solar)
            if not solar_serializer.is_valid():
                return response.Response(
                    solar_serializer.errors, status.HTTP_400_BAD_REQUEST
                )
            solar_instance = solar_serializer.save()

        # validate and save clocked data
        clocked_instance = None
        if clocked:
            clocked_serializer = schedule_serializers.ClockedScheduleSerializer(
                data=clocked
            )
            if not clocked_serializer.is_valid():
                return response.Response(
                    clocked_serializer.errors, status.HTTP_400_BAD_REQUEST
                )
            clocked_instance = clocked_serializer.save()

        pt_data = {
            "name": name,
            "description": description or "",
            "task": "tasks.webhook.webhook_job",
            "interval": interval_instance.id if interval_instance else None,
            "crontab": crontab_instance.id if crontab_instance else None,
            "solar": solar_instance.id if solar_instance else None,
            "clocked": clocked_instance.id if clocked_instance else None,
            "kwargs": json.dumps(webhook_serializer.data),
            "expires": expires,
            "expire_seconds": expire_seconds,
            "one_off": one_off,
            "start_time": start_time,
            "enabled": enabled,
        }
        pt_serializer = schedule_serializers.PeriodicTaskSerializer(data=pt_data)
        if not pt_serializer.is_valid():
            if interval_instance:
                interval_instance.delete()
            if crontab_instance:
                crontab_instance.delete()
            if solar_instance:
                solar_instance.delete()
            if clocked_instance:
                clocked_instance.delete()
            return response.Response(pt_serializer.errors, status.HTTP_400_BAD_REQUEST)

        pt_serializer.save()
        return response.Response(pt_serializer.data, status.HTTP_201_CREATED)


class TestWebhookApi(views.APIView):
    @swagger_auto_schema(
        responses=POST_RESPONSES,
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["url", "method"],
            properties={
                "url": openapi.Schema(type=openapi.TYPE_STRING),
                "method": openapi.Schema(type=openapi.TYPE_STRING, default="GET"),
                "query": openapi.Schema(type=openapi.TYPE_OBJECT),
                "payload": openapi.Schema(type=openapi.TYPE_OBJECT),
                "headers": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "Content-Type": openapi.Schema(
                            type=openapi.TYPE_STRING, default="application/json"
                        ),
                    },
                ),
            },
        ),
    )
    def post(self, request: request.Request, *args, **kwargs):
        webhook = request.data

        # extract webhook data
        webhook_data = {
            "pt_name": None,
            "url": webhook["url"],
            "method": webhook.get("method", "GET"),
            "query": webhook.get("query", {}),
            "payload": webhook.get("payload", None),
            "headers": webhook.get("headers", {}),
        }
        webhook_serializer = schedule_serializers.WebhookSerializer(data=webhook_data)
        if not webhook_serializer.is_valid():
            return response.Response(
                webhook_serializer.errors, status.HTTP_400_BAD_REQUEST
            )

        payload = make_wehbook_request(**webhook_serializer.data)

        return response.Response(payload, status.HTTP_200_OK)
