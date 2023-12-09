# Django
from rest_framework import views, request, response, status

# Custom
from django_celery_beat import models as django_celery_beat_models
from schedules import serializers as schedule_serializers


class ScheduleCrudApi(views.APIView):
    model_class = django_celery_beat_models.PeriodicTask
    serializer_class = schedule_serializers.PeriodicTaskSerializer

    def get(self, request: request.Request, *args, **kwargs):
        id = request.query_params.get("id", None)

        qs = self.model_class.objects.all()

        if id:
            qs = qs.filter(id=id)

        output = self.serializer_class(qs, many=True).data
        return response.Response(output, status.HTTP_200_OK)

    def post(self, request: request.Request, *args, **kwargs):
        periodic_task_serializer = self.serializer_class(
            data={**request.data, "task": "tasks.debug_task.debug_task"}
        )
        if not periodic_task_serializer.is_valid():
            return response.Response(
                periodic_task_serializer.errors, status.HTTP_400_BAD_REQUEST
            )

        periodic_task_serializer.save()
        return response.Response(periodic_task_serializer.data, status.HTTP_201_CREATED)
