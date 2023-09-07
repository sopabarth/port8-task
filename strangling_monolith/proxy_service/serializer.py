from rest_framework import serializers


class RulesSerializer(serializers.Serializer):
    key = serializers.CharField()
    value = serializers.ChoiceField(choices=['LEGACY', 'MODERN'])
