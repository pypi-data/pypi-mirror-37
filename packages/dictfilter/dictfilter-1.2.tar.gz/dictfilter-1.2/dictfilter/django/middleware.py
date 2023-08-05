from dictfilter import query


def dictfilter_middleware(get_response):
    def middleware(request):
        fields_param = request.GET.get('fields')

        response = get_response(request)

        if 200 <= response.status_code < 300:
            if not fields_param or fields_param == '*':
                query_fields = None
            else:
                query_fields = fields_param.split(',')

            if query_fields is not None:
                filtered_data = query(response.data, query_fields)

                # re-render the response
                response.data = filtered_data
                response._is_rendered = False
                response.render()

        return response

    return middleware
