#     Copyright 2020 getcarrier.io
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.


from json import JSONDecodeError
from typing import Any, Optional, Callable, Union, List

from pydantic import BaseModel, ValidationError, parse_obj_as
from requests import Response


class ApiResponseError(BaseModel):
    message: Any = None
    error_code: Optional[int] = None


class ApiResponse(BaseModel):
    status: int = 200
    success: bool = True
    error: Optional[ApiResponseError] = ApiResponseError()
    data: Any = {}
    debug: Any = {}

    @classmethod
    def failed(cls, status_code: int = 400, error_message: Any = None):
        klass = cls()
        klass.error.message = error_message
        klass.error.error_code = status_code
        klass.status = klass.error.error_code
        klass.success = False
        return klass

    @staticmethod
    def get_debug_data(response: Response, response_debug_processor: Optional[Callable] = None) -> dict:
        if response_debug_processor:
            try:
                debug_data = response_debug_processor(response)
                if not isinstance(debug_data, dict):
                    return {'data': debug_data}
                else:
                    return debug_data
            except Exception as e:
                return {'processor_failed': str(e)}
        return {}

    @staticmethod
    def get_data_from_response(response: Response):
        try:
            return response.json()
        except JSONDecodeError:
            return response.text

    @staticmethod
    def format_response_data(data: Any, response_data_type: Union[Callable, BaseModel, List]):
        if issubclass(response_data_type, BaseModel):
            try:
                parsed_data = response_data_type.parse_obj(data)
            except (ValidationError, TypeError) as e:
                if isinstance(data, str):
                    parsed_data = response_data_type.parse_raw(data)
                elif isinstance(data, list):
                    parsed_data = parse_obj_as(List[response_data_type], data)
                else:
                    raise e
        else:
            parsed_data = response_data_type(data)
        return parsed_data
