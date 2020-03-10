from rest_framework import serializers


class ProjectStatusSerializer(serializers.Serializer):
    web_tx_identifier = serializers.CharField(read_only=True)
    web_tx_status = serializers.IntegerField(help_text='Estado del proyecto', label='Estado')

    def update(self, instance, validated_data):
        instance.web_tx_status = validated_data.get('web_tx_status', instance.web_tx_status)
        instance.save()
        return instance