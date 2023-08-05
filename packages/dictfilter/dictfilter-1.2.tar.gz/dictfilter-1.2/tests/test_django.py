from dictfilter.django.middleware import dictfilter_middleware


class Request:
    def __init__(self, get):
        self.GET = get


class Response:
    def __init__(self, data):
        self.data = data
        self.status_code = 200
        self._is_rendered = True
        self._render_was_called = False

    def render(self):
        assert self._is_rendered is False
        self._is_rendered = True
        self._render_was_called = True


def test_middleware_with_fields():
    def get_response(_):
        return Response({
            'a': 1,
            'b': 'test',
            'c': True,
            'd': 'unwanted',
        })

    middleware = dictfilter_middleware(get_response)

    request = Request(get={
        'fields': 'a,b,c',
    })
    response = middleware(request)

    expected = {
        'a': 1,
        'b': 'test',
        'c': True,
    }

    assert response._render_was_called
    assert response.data == expected


def test_middleware_with_asterisk():
    def get_response(_):
        return Response({
            'a': 1,
            'b': 'test',
            'c': True,
            'd': 'another',
        })

    middleware = dictfilter_middleware(get_response)

    request = Request(get={
        'fields': '*',
    })
    response = middleware(request)

    expected = {
        'a': 1,
        'b': 'test',
        'c': True,
        'd': 'another',
    }

    assert not response._render_was_called
    assert response.data == expected


def test_middleware_with_no_fields():
    def get_response(_):
        return Response({
            'a': 1,
            'b': 'test',
            'c': True,
            'd': 'another',
        })

    middleware = dictfilter_middleware(get_response)

    request = Request(get={})
    response = middleware(request)

    expected = {
        'a': 1,
        'b': 'test',
        'c': True,
        'd': 'another',
    }

    assert not response._render_was_called
    assert response.data == expected
