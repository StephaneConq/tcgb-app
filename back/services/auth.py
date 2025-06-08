import os
import firebase_admin
from firebase_admin import credentials, auth
from fastapi import Depends, HTTPException, status, Request
from typing import Optional

# Initialize Firebase Admin SDK
if not firebase_admin._apps:
    firebase_admin.initialize_app()

async def get_current_user_email(request: Request) -> str:
    """
    Dependency to extract and verify Firebase access token from Authorization header.
    Returns the user's email if token is valid.
    """
    authorization = request.headers.get("Authorization")
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = authorization.replace("Bearer ", "")
    
    try:
        # Verify the token and get user info
        decoded_token = auth.verify_id_token(token)
        email = decoded_token.get("email")
        
        if not email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token does not contain email",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return email
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )
