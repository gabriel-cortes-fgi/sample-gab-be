from dataclasses import asdict
from http import HTTPStatus

from flask import Response

from app.errors.brand import BrandNotFoundError
from app.extensions import db
from app.models.brand import Brand
from app.schemas.resources.brand import BrandSchemas
# from app.errors.brand import BrandAlreadyExistsError


class BrandCore:
    def get_all(self, query_args: BrandSchemas.GetListQuery):
        brand_query = Brand.query
        if query_args.is_active is not None:
            brand_query = brand_query.filter(
                Brand.is_active == query_args.is_active,
            )

        brand_query = brand_query.filter(
            Brand.code.ilike(f'%{query_args.code}%'),
        ).filter(Brand.name.ilike(f'%{query_args.name}%'))

        paginated_brand = brand_query.paginate(
            page=query_args.page, per_page=query_args.per_page,
            error_out=False,
        )
        brands = paginated_brand.items

        return {
            'data': brands,
            'page_num': query_args.page,
            'page_size': paginated_brand.per_page,
            'total_pages': paginated_brand.pages,
        }

    def get(self, brand_id: int):
        brand = Brand.query.get(brand_id)
        if brand is None:
            raise BrandNotFoundError(f'Brand with id {brand_id} not found')

        return {
            'data': brand,
        }

    def create_brand(self, payload: BrandSchemas.PostRequest, user_name: str):
        brand = Brand.query.filter_by(code=payload.code).first()
        if brand is not None:
            return Response(
                {
                    'error': 'test',
                    'description': 'test description',
                }, HTTPStatus.CONFLICT,
            )

        brand = Brand(**asdict(payload))
        brand.created_by = user_name
        db.session.add(brand)
        db.session.commit()

        return {
            'data': brand,
        }

    def update_brand(
            self,
            brand_id: int,
            payload: BrandSchemas.PatchRequest,
            user_name: str,
    ):
        brand = Brand.query.get(brand_id)
        if brand is None:
            raise BrandNotFoundError(f'Brand with id {brand_id} not found')

        brand.modified_by = user_name
        patch_model(brand, asdict(payload))

        db.session.commit()
        return {
            'data': brand,
        }

    def delete_brand(self, brand_id: int):
        brand = Brand.query.get(brand_id)
        if brand is None:
            raise BrandNotFoundError(f'Brand with id {brand_id} not found')

        db.session.delete(brand)
        db.session.commit()
        return {'data': 'Successfully deleted the brand record'}
