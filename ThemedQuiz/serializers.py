from rest_framework import serializers
from ThemedQuiz.models import DayTheme, DayThemeTranslation, DayQuestionHeader, DayQuestions


class DayThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DayTheme
        fields = ('id', 'target_date','main_theme', 'active', 'imageURL', 'description', 'created_at', 'updated_at',)


class DayThemeTranslationSerializer(serializers.ModelSerializer):
    theme_image = serializers.FileField(source='theme.imageURL', required=False)
    theme_background_image = serializers.FileField(source=
                                                   'theme.backgroundImageURL',
                                                   required=False)
    target_date = serializers.DateField(source='theme.target_date', required=False)
    main_theme = serializers.BooleanField(source='theme.main_theme', required=False)

    class Meta:
        model = DayThemeTranslation
        fields = ('theme_image', 'theme_background_image', 'target_date',
                  'main_theme', 'id',
                  'language', 'name', 'description', 'created_at', 'updated_at',)


class DayQuestionHeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = DayQuestionHeader
        fields = ('id', 'active', 'description', 'created_at', 'updated_at',)


class DayQuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DayQuestions
        fields = ('id', 'header', 'language', 'question', 'answer1', 'answer2', 'right_answer', 'description', 'created_at', 'updated_at',)
