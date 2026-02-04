"""
JWT-based authentication and authorization.
Includes password hashing and role-based access control.
"""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

from config import settings


# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# HTTP Bearer token scheme
security = HTTPBearer()


class TokenData(BaseModel):
    """Token payload data."""
    user_id: str
    email: str
    role: str = "user"
    exp: Optional[datetime] = None


class Token(BaseModel):
    """Token response model."""
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class AuthService:
    """Authentication service for user management."""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash a password using bcrypt.
        
        Args:
            password: Plain text password
        
        Returns:
            Hashed password
        """
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verify a password against a hash.
        
        Args:
            plain_password: Plain text password
            hashed_password: Bcrypt hashed password
        
        Returns:
            True if password matches
        """
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def create_access_token(
        user_id: str,
        email: str,
        role: str = "user",
        expires_delta: Optional[timedelta] = None
    ) -> Token:
        """
        Create a JWT access token.
        
        Args:
            user_id: User's unique ID
            email: User's email
            role: User's role (user, admin, analyst)
            expires_delta: Optional custom expiration time
        
        Returns:
            Token object with access token and metadata
        """
        if expires_delta is None:
            expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        
        expire = datetime.utcnow() + expires_delta
        
        payload = {
            "sub": user_id,
            "email": email,
            "role": role,
            "exp": expire,
            "iat": datetime.utcnow()
        }
        
        encoded_jwt = jwt.encode(
            payload,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM
        )
        
        return Token(
            access_token=encoded_jwt,
            expires_in=int(expires_delta.total_seconds())
        )
    
    @staticmethod
    def decode_token(token: str) -> TokenData:
        """
        Decode and validate a JWT token.
        
        Args:
            token: JWT token string
        
        Returns:
            TokenData with user information
        
        Raises:
            HTTPException: If token is invalid or expired
        """
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM]
            )
            
            user_id = payload.get("sub")
            email = payload.get("email")
            role = payload.get("role", "user")
            
            if user_id is None or email is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token payload"
                )
            
            return TokenData(
                user_id=user_id,
                email=email,
                role=role
            )
        
        except JWTError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Token validation failed: {str(e)}"
            )
    
    @staticmethod
    def refresh_token(token: str) -> Token:
        """
        Refresh an access token.
        
        Args:
            token: Current valid token
        
        Returns:
            New Token object
        """
        token_data = AuthService.decode_token(token)
        return AuthService.create_access_token(
            user_id=token_data.user_id,
            email=token_data.email,
            role=token_data.role
        )


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> TokenData:
    """
    Dependency to get current authenticated user.
    
    Args:
        credentials: HTTP Bearer token credentials
    
    Returns:
        TokenData with current user information
    """
    return AuthService.decode_token(credentials.credentials)


def require_admin(current_user: TokenData = Depends(get_current_user)) -> TokenData:
    """
    Dependency to require admin role.
    
    Args:
        current_user: Current authenticated user
    
    Returns:
        TokenData if user is admin
    
    Raises:
        HTTPException: If user is not admin
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user


def require_analyst(current_user: TokenData = Depends(get_current_user)) -> TokenData:
    """
    Dependency to require analyst or admin role.
    """
    if current_user.role not in ["analyst", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Analyst access required"
        )
    return current_user


# Create global auth service instance
auth_service = AuthService()
