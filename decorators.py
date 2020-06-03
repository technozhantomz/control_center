from typing import Type, Union, Callable, Awaitable, Mapping, Optional
from aiohttp.web import Request, Response, HTTPException, json_response
import functools
import re
import json
from json.decoder import JSONDecodeError
from marshmallow.exceptions import ValidationError as SchemaValidationError
import logging


from data_transfer_classes import DataTransferClass


class InvalidJSON(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class InvalidJSONType(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class InternalInvalidJSONType(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)

# TODO: variadic callable, blocked by
# https://github.com/python/typing/issues/239
OriginalHandler = Callable[[Request], Awaitable[Response]]

# TODO: variadic callable, blocked by
# https://github.com/python/typing/issues/239
ErrorsMapHandler = Callable[[Request], Awaitable[Response]]


ErrorsMapWrapper = Callable[[ErrorsMapHandler], OriginalHandler]


def errors_map(errors: Mapping[Type[Exception],
                               Type[HTTPException]]) -> ErrorsMapWrapper:
    def to_snake_case(name: str) -> str:
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)

        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    def handler_wrapper(handler: ErrorsMapHandler) -> OriginalHandler:
        @functools.wraps(handler)
        async def map(request: Request, *args) -> Response:
            try:
                return await handler(request, *args)
            except Exception as exception:
                for error_from, error_to in errors.items():
                    if isinstance(exception, error_from):
                        logging.getLogger('aiohttp.web').exception(exception)

                        raise error_to(body=json.dumps({
                            'error': {
                                'type': to_snake_case(error_from.__name__),
                                'description': str(exception)
                            }
                        }), content_type='application/json')

                raise exception
        return map
    return handler_wrapper

# TODO: variadic callable, blocked by
# https://github.com/python/typing/issues/239
DTOValidateHandler = Union[Callable[[Request, DataTransferClass],
                                     Awaitable[DataTransferClass]],
                           Callable[[Request], Awaitable[DataTransferClass]]]


DTOValidateWrapper = Callable[[DTOValidateHandler], OriginalHandler]


def dto_validate(dtc: Optional[DataTransferClass] = None) -> DTOValidateWrapper:
    def handler_wrapper(handler: DTOValidateHandler) -> OriginalHandler:
        @functools.wraps(handler)
        async def validate(request: Request, *args) -> Response:
            if dtc is None:
                dto = await handler(request, *args)
            else:
                try:
                    payload = await request.json()
                except JSONDecodeError as exception:
                    raise InvalidJSON(
                        f'Invalid JSON payload: {exception}'
                    )
                try:
                    dto = dtc.Schema().load(payload)
                except SchemaValidationError as exception:
                    raise InvalidJSONType(
                        f'Invalid JSON payload type: {exception}'
                    )
                dto = await handler(request, dto, *args)

            schema = dto.Schema()
            payload = schema.dump(dto)

            try:
                schema.validate(payload)
            except SchemaValidationError as exception:
                raise InternalInvalidJSONType(
                    f'Invalid JSON payload type: {exception}'
                )

            return json_response(payload)
        return validate
    return handler_wrapper
