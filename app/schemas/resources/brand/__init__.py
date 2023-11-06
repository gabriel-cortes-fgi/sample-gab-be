from dataclasses import dataclass
from typing import List
from typing import Optional

import desert
from marshmallow import validate
from marshmallow.fields import Int
from marshmallow.fields import Str


class BrandSchemas:
    @dataclass
    class Brand():
        id: int
        code: str
        name: str
        is_active: bool

    @dataclass
    class GetListQuery:
        page: int = 1
        per_page: int = desert.field(
            Int(validate=validate.Range(max=100)), default=100,
        )
        code: str = desert.field(
            Str(validate=validate.Length(max=250)), default='',
        )
        name: str = ''
        is_active: Optional[bool] = None

    @dataclass
    class GetListResponse:
        data: List['BrandSchemas.Brand']
        page_num: int
        page_size: int
        total_pages: int

    @dataclass
    class GetResponse:
        data: 'BrandSchemas.Brand'

    @dataclass
    class PostRequest:
        code: str = ''
        name: str = ''
        is_active: bool = True

    @dataclass
    class PostResponse:
        data: 'BrandSchemas.Brand'

    @dataclass
    class PatchRequest:
        code: str = ''
        name: str = ''
        is_active: bool = True

    @dataclass
    class PatchResponse:
        data: 'BrandSchemas.Brand'

    @dataclass
    class DeleteResponse:
        data: 'BrandSchemas.Brand'
