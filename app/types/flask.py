from http import HTTPStatus
from typing import Any
from typing import Dict
from typing import Tuple
from typing import Union

ResourceResponseType = Union[
    Dict[Any, Any],
    Tuple[Dict[Any, Any], Union[HTTPStatus, int]],
]
