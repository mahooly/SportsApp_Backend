from rest_framework import filters


class NewsFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        for key in request.GET.keys():
            if key == 'title':
                return queryset.filter(title__icontains=request.GET['title'])
            elif key == 'text':
                return queryset.filter(text__icontains=request.GET['text'])
            elif key == 'tag':
                return queryset.filter(tags__name__icontains=request.GET['tag'])
        return queryset


# class MatchOrderingFilterBackend(filters.OrderingFilter):
#     def filter_queryset(self, request, queryset, view):
#         for key in request.GET.keys():
#             if key == 'ordering':
#                 if request.GET['ordering'] == 'opp':
#                     return queryset.order_by(team2)
#         return queryset