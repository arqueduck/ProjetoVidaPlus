from datetime import timedelta

SECRET_KEY = (
    "R%8d@099l!u6A6*VXS1hzqJp1mcIAH41$KEj$XEWY2jMG#p^7clA2*JM04mYw&v46yJ3DAtArFli1yBbz5pnm$$SC##QmfQiBSA0wn*rWaoOy9g9sC6%Au%PVB79ex5E"
)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 1 hora


def get_access_token_expires() -> timedelta:
    return timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
