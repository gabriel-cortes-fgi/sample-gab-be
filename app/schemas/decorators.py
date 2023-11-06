from dataclasses import dataclass


@dataclass
class JwtToken:
    name: str
    email: str
    sub: str
    iat: int
