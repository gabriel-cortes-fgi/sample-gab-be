from app.core.brand import BrandCore
from app.schemas.resources.brand import BrandSchemas
from fgi.flask import request_model
from fgi.flask import response_model
from flask_apispec import doc  # type: ignore
from flask_apispec import MethodResource
from flask_restful import Resource

brand_core = BrandCore()


@doc(tags=['Brand'])
class BrandListsResource(Resource, MethodResource):
    @request_model(query_model=BrandSchemas.GetListQuery)
    @response_model(BrandSchemas.GetListResponse)
    def get(self, query_args: BrandSchemas.GetListQuery):
        return brand_core.get_all(query_args)

    @request_model(body_model=BrandSchemas.PostRequest)
    @response_model(BrandSchemas.PostResponse)
    def post(self, payload: BrandSchemas.PostRequest):
        user_name = "test"
        return brand_core.create_brand(payload, user_name)


@doc(tags=['Brand'])
class BrandResource(Resource, MethodResource):
    @response_model(BrandSchemas.GetResponse)
    def get(self, brand_id):
        return brand_core.get(brand_id)

    @request_model(body_model=BrandSchemas.PatchRequest)
    @response_model(BrandSchemas.PatchResponse)
    def patch(
        self,
        brand_id,
        payload: BrandSchemas.PatchRequest,
    ):
        user_name = "test"
        return brand_core.update_brand(brand_id, payload, user_name)

    @response_model(BrandSchemas.DeleteResponse)
    def delete(self, brand_id):
        return brand_core.delete_brand(brand_id)
