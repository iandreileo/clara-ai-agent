from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> str:
    """
    Verify the Bearer token and return the token value.
    
    Args:
        credentials: The Bearer token credentials
        
    Returns:
        str: The token value if valid
        
    Raises:
        HTTPException: If token is missing or invalid
    """
    try:
        if not credentials or not credentials.credentials:
            raise HTTPException(
                status_code=401,
                detail="Missing authentication token"
            )
            
        return credentials.credentials
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error verifying token: {str(e)}"
        )
