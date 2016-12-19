import datetime
from rest_framework import filters
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response
from SimpleQuiz.models import QuestionHeader, Questions
from SimpleQuiz.serializers import QuestionHeaderSerializer, QuestionsSerializer


class QuestionHeaderViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = QuestionHeader.objects.all()
    serializer_class = QuestionHeaderSerializer

    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter,)
    ordering_fields = ('created_at', 'updated_at')

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = None

    def filter_queryset(self, queryset):
        queryset = QuestionHeader.objects.all()
        return queryset

    @list_route(methods=['get'], url_path='get-questions/(?P<p_language>[A-Z]+)')
    def get_questions(self, request, p_language=None):

        if p_language is None or p_language not in ['E','R']:
            p_language = 'E'

        questions_by_language = Questions.objects.filter(language=p_language, header__active=True)
        if questions_by_language.count() > 0:

            serializer = QuestionsSerializer(questions_by_language, many=True)
            return Response(serializer.data)

        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @list_route(methods=['get'], url_path='get-changed-questions/(?P<p_language>[A-Z]+)')
    def get_changed_questions(self, request, p_language=None):

        today = datetime.datetime.today()

        # day_val = self.request.query_params.get('day', None)
        # month_val = self.request.query_params.get('month', None)
        # year_val = self.request.query_params.get('year', None)

        try:
            # if day_val is not None and month_val is not None and year_val is not None:
            #     max_change_date = datetime.date(year=int(year_val), month=int(month_val), day=int(day_val))
            # else:
            #     max_change_date = datetime.date(year=today.year, month=today.month, day=today.day)

            time_stamp_val = float(self.request.query_params.get('update_time_stamp', None))

            if time_stamp_val is not None:
                max_change_date = datetime.datetime.fromtimestamp(time_stamp_val/1e3)
            else:
                max_change_date = datetime.date(year=today.year, month=today.month, day=today.day)

        except ValueError:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if p_language is None or p_language not in ['E','R']:
            p_language = 'E'

        questions_by_language = Questions.objects.filter(updated_at__gte=max_change_date, language=p_language, header__active=True)
        if questions_by_language.count() > 0:

            serializer = QuestionsSerializer(questions_by_language, many=True)
            return Response(serializer.data)

        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class QuestionsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Questions.objects.all()
    serializer_class = QuestionsSerializer

    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter,)
    filter_fields = ('language', 'header',)
    ordering_fields = ('created_at', 'updated_at')

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = None

    def filter_queryset(self, queryset):
        queryset = Questions.objects.all()

        lang_val = self.request.query_params.get('language', None)

        if lang_val is not None:
            queryset = queryset.filter(language=lang_val)
        else:
            queryset = queryset.filter(language='E')

        return queryset
