from rest_framework import serializers
from ThemedQuiz.models import DayTheme, DayThemeTranslation, DayQuestionHeader, DayQuestions


class DayThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DayTheme
        fields = ('id', 'target_date', 'active', 'imageURL', 'description', 'created_at', 'updated_at',)


class DayThemeTranslationSerializer(serializers.ModelSerializer):
    theme_image = serializers.FileField(source='theme.imageURL', required=False)

    class Meta:
        model = DayThemeTranslation
        fields = ('theme_image', 'id', 'language', 'name', 'description', 'created_at', 'updated_at',)


class DayQuestionHeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = DayQuestionHeader
        fields = ('id', 'active', 'description', 'created_at', 'updated_at',)


class DayQuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DayQuestions
        fields = ('id', 'header', 'language', 'question', 'answer1', 'answer2', 'right_answer', 'description', 'created_at', 'updated_at',)
