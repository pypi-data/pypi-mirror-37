import logging
from functools import wraps
from dm.cloudtrailsdk.utils.functions import send_custom_logger, send_exception_logger
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def build_apigateway_response(response):
    """

    :param response:
    :return:
    """
    return {
        'statusCode': response['code'],
        'body': json.dumps(response)
    }


def cloudtrails_apigateway(app_name="undefined", app_version="undefined", tracker_environment=None):
    """
        Decorador para handlers que implementan lambdas que procesan eventos de AWS ApiGateway
    :param app_name:
    :param app_version:
    :param tracker_environment:
    :return:
    """

    def cloudtrails_apigateway_tracker_decorator(func):
        """
            Funcion interna para el decorador
        :param func:
        :return:
        """

        @wraps(func)
        def apigateway_wrapper(event, context):
            """
            Wrapper que extrae los datos del request a partir del parametro Event de ApiGateway
            :param event:
            :param context:
            :return:
            """

            # Intentar obtener el resultado de la funcion original
            result = {}
            try:
                result = func(event, context)
            except Exception as e:
                # Si la funcion original dio error logear un evento exception y retornar un 500 generico
                send_exception_logger(app_name, app_version)
                logger.error(e.message)
                error_response = {'message': 'Ha ocurrido un error no controlado', 'code': 500}
                result = build_apigateway_response(error_response)

            # Extraer los datos del evento Apigateway Proxy Integration
            function_name = func.__name__
            properties = {
                "EventType": "WebApiCall",
                'FunctionName': function_name,
                "RequestMethod": event['httpMethod'],
                "RequestScheme": "https",
                "RequestHost": event['headers'].get('Host', ''),
                "RequestPath": event.get('path', ''),
                "RequestQueryString": json.dumps(event.get('queryStringParameters', {})),
                "ClientIP": event['headers'].get('X-Forwarded-For', ''),
                "UserAgent": event['headers'].get('User-Agent', ''),
                "RequestPayload": json.dumps(event.get('body', {})),
                "ResponsePayload": json.dumps(result.get('body', {})),
                "ResponseHttpStatus": result.get('statusCode', '0'),
                "Headers": json.dumps(event.get('headers', {}))
            }

            # Poner Custom Dimensions si hay alguna
            if result.get('cloudtrails_dimensions', None) is not None:
                properties['Dimensions'] = result.get('cloudtrails_dimensions', None)
                result.pop('cloudtrails_dimensions', None)

            # Poner Custom  properties si hay alguna
            if result.get('cloudtrails_properties', None) is not None:
                properties.update(result.get('cloudtrails_properties', None))
                result.pop('cloudtrails_properties', None)

            send_custom_logger(app_name=app_name, app_version=app_version,
                               tracker_environment=tracker_environment, **properties)

            # Retornar el resultado final
            return result
        
        return apigateway_wrapper

    return cloudtrails_apigateway_tracker_decorator
