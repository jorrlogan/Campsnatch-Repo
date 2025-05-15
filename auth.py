# clerk_auth.py
from fastapi import Header, HTTPException, Depends
from jwt import PyJWKClient, decode as jwt_decode

JWKS_URL = "https://legible-lynx-48.clerk.accounts.dev/.well-known/jwks.json"  # Or use your own Frontend URL + '/.well-known/jwks.json'


def verify_clerk_token(authorization: str = Header(...)):
    print(f"AUTH HEADER: {authorization}")
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token format")

    token = authorization.split(" ")[1]

    try:
        jwks_client = PyJWKClient(JWKS_URL)
        signing_key = jwks_client.get_signing_key_from_jwt(token)
        decoded = jwt_decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            options={"verify_exp": True, "verify_nbf": True},
        )

        return decoded  # Includes sub (user ID), sid (session ID), etc.

    except Exception as e:
        import traceback

        traceback.print_exc()
        raise HTTPException(
            status_code=401, detail=f"Token verification failed: {str(e)}"
        )
