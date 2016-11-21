from rest_framework import serializers
from SimpleQuiz.models import QuestionHeader, Questions


class QuestionHeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionHeader
        fields = ('id', 'active', 'description', 'created_at', 'updated_at',)


class QuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questions
        fields = ('id', 'header', 'language', 'question', 'answer1', 'answer2', 'right_answer', 'created_at', 'updated_at',)
