from app.errors import ResourceConflictError
from app.errors import ResourceNotFoundError


class BrandNotFoundError(ResourceNotFoundError):
    def __init__(self, description=''):
        super().__init__(name='Brand not found', description=description)


class BrandAlreadyExistsError(ResourceConflictError):
    def __init__(self, description=''):
        super().__init__(
            name='Brand code already exists',
            description=description,
        )
