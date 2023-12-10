from rest_framework import serializers

from timezone_field.rest_framework import TimeZoneSerializerField

from django_celery_beat.models import (
    IntervalSchedule,
    CrontabSchedule,
    SolarSchedule,
    ClockedSchedule,
    PeriodicTask,
)

from config import METHOD_CHOICES

import json


class IntervalScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntervalSchedule
        fields = "__all__"


class CrontabScheduleSerializer(serializers.ModelSerializer):
    timezone = TimeZoneSerializerField()

    class Meta:
        model = CrontabSchedule
        fields = "__all__"


class SolarScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolarSchedule
        fields = "__all__"


class ClockedScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClockedSchedule
        fields = "__all__"


class PeriodicTaskSerializer(serializers.ModelSerializer):
    interval_details = IntervalScheduleSerializer(source="interval", read_only=True)
    crontab_details = CrontabScheduleSerializer(source="crontab", read_only=True)
    solar_details = SolarScheduleSerializer(source="solar", read_only=True)
    clocked_details = ClockedScheduleSerializer(source="clocked", read_only=True)

    class Meta:
        model = PeriodicTask
        fields = (
            "id",
            "name",
            "description",
            "task",
            "interval",
            "crontab",
            "solar",
            "clocked",
            "interval_details",
            "crontab_details",
            "solar_details",
            "clocked_details",
            "kwargs",
            "expires",
            "expire_seconds",
            "one_off",
            "start_time",
            "enabled",
            "last_run_at",
            "total_run_count",
            "date_changed",
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.pop("task")
        kwargs = data.pop("kwargs")
        data["webhook"] = json.loads(kwargs or "{}")
        return data


class WebhookSerializer(serializers.Serializer):
    pt_name = serializers.CharField(allow_blank=True, allow_null=True)
    url = serializers.URLField(required=True)
    method = serializers.ChoiceField(required=True, choices=METHOD_CHOICES)
    query = serializers.DictField(allow_empty=True, allow_null=True)
    payload = serializers.DictField(allow_empty=True, allow_null=True)
    headers = serializers.DictField(allow_empty=True, allow_null=True)
