from rest_framework import serializers

from timezone_field.rest_framework import TimeZoneSerializerField

from django_celery_beat.models import (
    IntervalSchedule,
    CrontabSchedule,
    SolarSchedule,
    ClockedSchedule,
    PeriodicTask,
)


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
            "name",
            "task",
            "interval",
            "crontab",
            "solar",
            "clocked",
            "interval_details",
            "crontab_details",
            "solar_details",
            "clocked_details",
            "args",
            "kwargs",
            "queue",
            "exchange",
            "routing_key",
            "headers",
            "priority",
            "expires",
            "expire_seconds",
            "one_off",
            "start_time",
            "enabled",
            "last_run_at",
            "total_run_count",
            "date_changed",
            "description",
        )
