from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from datetime import datetime
from app.models import DailyPrice, Index
from app.serializers import DailyPriceSerializer
from rest_framework import pagination
from math import ceil
from urllib.parse import unquote
from django.db.models import Min, Max
class DailyPricePagination(pagination.PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 100

class DailyPriceAPIView(APIView):
    pagination_class = DailyPricePagination
    def parse_filter(self, filter_str):
        filter_str = unquote(filter_str)
        print("filter_str : ", filter_str)
        import re
        match = re.match(r"([A-Z_]+)([<>]=?)(\d+(\.\d+)?)", filter_str)
        if not match:
            raise ValueError("Invalid filter format")

        field, operator, value, _ = match.groups()  # Extract only first 3 values
        operator_mapping = {'>': 'gt', '<': 'lt', '>=': 'gte', '<=': 'lte'}
        return field, operator_mapping[operator], float(value)

    def get(self, request, index_id):
        
        if 'start_date' not in request.query_params or request.query_params['start_date'] == '' :
            return JsonResponse({'error': 'start_date is required'}, status=400)
        if 'end_date' not in request.query_params or request.query_params['end_date'] == '' :
            return JsonResponse({'error': 'end_date is required'}, status=400)  
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        filters_dict = {'index_id': index_id, 'date__range': [start_date, end_date]}

        if 'filters' in request.query_params:
            filters = request.query_params.get('filters')
            # print("filters : ", filters)
            filter_mapping = {
                'OPEN': 'open_price',
                'HIGH': 'high_price',
                'LOW': 'low_price',
                'CLOSE': 'close_price',
                'SHARES_TRADED': 'shares_traded',
                'TURNOVER': 'turnover'
            }


            try:
                key, operator, value= self.parse_filter(filters)
                # print("key, operator, value : ", key, operator, value)
                if key in filter_mapping:
                    filters_dict[f"{filter_mapping[key]}__{operator}"] = value
            except ValueError:
                return JsonResponse({'error': f'Invalid filter format: {filters}'}, status=400)
        # print("filters_dict : ", filters_dict)
        queryset = DailyPrice.objects.filter(**filters_dict)
        # print("queryset : ", queryset)
        aggregates = queryset.aggregate(
            open_lowest=Min('open_price'), open_highest=Max('open_price'),
            high_lowest=Min('high_price'), high_highest=Max('high_price'),
            low_lowest=Min('low_price'), low_highest=Max('low_price'),
            close_lowest=Min('close_price'), close_highest=Max('close_price'),
            shares_traded_lowest=Min('shares_traded'), shares_traded_highest=Max('shares_traded'),
            turnover_lowest=Min('turnover'), turnover_highest=Max('turnover')
        )
        # print("aggregates : ", aggregates)
        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = DailyPriceSerializer(paginated_queryset, many=True)

        total_rows = queryset.count()
        total_pages = ceil(total_rows / paginator.page_size) if paginator.page_size else 1

        response = {
            'start-date': start_date,
            'end-date': end_date,
            'data': serializer.data,
            'pagination': {
                'page': paginator.page.number if paginator.page else 1,
                'total_pages': total_pages,
                'total_rows': total_rows
            },
            'ranges': {
                'open': {'lowest': aggregates['open_lowest'], 'highest': aggregates['open_highest']},
                'high': {'lowest': aggregates['high_lowest'], 'highest': aggregates['high_highest']},
                'low': {'lowest': aggregates['low_lowest'], 'highest': aggregates['low_highest']},
                'close': {'lowest': aggregates['close_lowest'], 'highest': aggregates['close_highest']},
                'shares_traded': {'lowest': aggregates['shares_traded_lowest'], 'highest': aggregates['shares_traded_highest']},
                'turnover': {'lowest': aggregates['turnover_lowest'], 'highest': aggregates['turnover_highest']}
            }
        }

        return Response(response)
