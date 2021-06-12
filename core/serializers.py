from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from core.models import MessageModel, ScenarioModel
from rest_framework.serializers import ModelSerializer, CharField, DateTimeField, IntegerField
from rest_framework.response import Response
from django.db.models import Q

class MessageModelSerializer(ModelSerializer):
    user = CharField(source='user.username', read_only=True)
    recipient = CharField(source='recipient.username')

    def create(self, validated_data):
        user = self.context['request'].user
        recipient = get_object_or_404(
            User, username=validated_data['recipient']['username'])
        msg = MessageModel(recipient=recipient,
                           body=validated_data['body'],
                           user=user,
                           sid=validated_data['sid']     
                        )
        msg.save()
        return msg

    class Meta:
        model = MessageModel
        fields = ('id', 'user', 'recipient', 'timestamp', 'body', 'sid')


class UserModelSerializer(ModelSerializer):
    latest_message = CharField()
    timestamp = DateTimeField()
    class Meta:
        model = User
        fields = ('username', 'latest_message','timestamp')

class ScenarioModelSerializer(ModelSerializer):
    user = CharField(source='user.username', read_only=True)
    recipient = CharField(source='recipient.username')
    sid = IntegerField()

    def create(self, validated_data):
        user = self.context['request'].user
        recipient = get_object_or_404(
            User, username=validated_data['recipient']['username'])
        queryset = ScenarioModel.objects.filter(Q(recipient=recipient, user=user) |
                                            Q(recipient=user, user=recipient))
       
        if queryset.exists():
            id = queryset.values().first()["id"]
            scenario = ScenarioModel.objects.get(id=id)
            scenario.sid = validated_data["sid"]  # change field
            scenario.save(update_fields=["sid"])
            return scenario
        else:
            print("No entry")
            msg = ScenarioModel(recipient=recipient,
                            user=user,
                            sid=validated_data['sid']     
                            )
            msg.save()
            return msg

        
    class Meta:
        model = ScenarioModel
        fields = ('user', 'recipient','sid')


