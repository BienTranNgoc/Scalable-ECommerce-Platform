from rest_framework import serializers


class FilterUserLogSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)


class ReportUserLogSerializer(serializers.Serializer):
    type_object = serializers.CharField()
    action = serializers.CharField()
    object_id = serializers.CharField()
    status = serializers.BooleanField()


class FilterUserLogDetailSerializer(serializers.Serializer):
    start_date = serializers.DateField(format='%Y-%m-%d', required=True)
    end_date = serializers.DateField(format='%Y-%m-%d', required=False)
    start_time = serializers.TimeField(format='%H:%M', required=False)
    end_time = serializers.TimeField(format='%H:%M', required=False)
    username = serializers.ListField(child=serializers.CharField(), required=False, allow_empty=True)
    action = serializers.ListField(child=serializers.CharField(), required=False, allow_empty=True)
    object_type = serializers.ListField(child=serializers.CharField(), required=False, allow_empty=True)
    status = serializers.ListField(child=serializers.BooleanField(), required=False, allow_null=True, allow_empty=True)
    metadata = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    page = serializers.IntegerField(required=False, min_value=1, default=1)
    limit = serializers.IntegerField(required=False, min_value=1, max_value=100, default=10)
    is_export_csv = serializers.BooleanField(required=False, default=False)

    def validate(self, data):
        if not data.get('end_date'):
            data['end_date'] = data['start_date']
        elif data['end_date'] < data['start_date']:
            raise serializers.ValidationError("end_date cannot be before start_date")

        if data.get('start_time') and data.get('end_time'):
            if data['end_time'] < data['start_time']:
                raise serializers.ValidationError("end_time cannot be before start_time")

        # Ensure status is always a list
        if 'status' in data and data['status'] is not None and not isinstance(data['status'], list):
            data['status'] = [data['status']]

        return data


class FilterUserLogMetadataSerializer(serializers.Serializer):
    metadata = serializers.CharField()
    page = serializers.IntegerField(required=False, min_value=1, default=1)
    limit = serializers.IntegerField(required=False, min_value=1, max_value=100, default=10)
