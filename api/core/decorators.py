from functools import wraps
from rest_framework.permissions import IsAuthenticated


#  функция, которая принимает параметры params и returns и возвращает декоратор
def define_usage(params=None, returns=None):
    # декоратор, который принимает функцию представления в качестве аргумента
    def decorator(function):
        # Получаем класс представления из функции представления
        cls = function.view_class
        header = None
        # Требуется ли аутентификация для доступа к этому представлению?
        if IsAuthenticated in cls.permission_classes:
            # Если да, то устанавливаем заголовок
            header = {'Authorization': 'Token String'}
        # Создаем список допустимых методов для представления, исключая метод options
        methods = [method.upper() for method in cls.http_method_names if method != 'options']
        # Создаем словарь usage с информацией о типах запросов, заголовках, параметрах запроса и возвращаемых данных
        usage = {'Request Types': methods, 'Headers': header, 'Body': params, 'Returns': returns}

        # @wraps используем для сохранения метаданных и документации исходной функции представления
        @wraps(function)
        def _wrapper(*args, **kwargs):
            return function(*args, **kwargs)
        _wrapper.usage = usage
        return _wrapper
    return decorator
