from typing import Any, Dict, Optional
from fastapi import HTTPException, status

def create_response(
    message: str,
    data: Optional[Any] = None,
    success: bool = True
) -> Dict[str, Any]:
    """Create a standardized API response"""
    response = {
        "success": success,
        "message": message
    }
    
    if data is not None:
        response["data"] = data
    
    return response

def create_error_response(
    message: str,
    status_code: int = status.HTTP_400_BAD_REQUEST,
    detail: Optional[str] = None
) -> HTTPException:
    """Create a standardized error response"""
    error_detail = detail or message
    return HTTPException(
        status_code=status_code,
        detail=error_detail
    )

# Common error responses
class ErrorResponses:
    @staticmethod
    def user_not_found(username: str) -> HTTPException:
        return create_error_response(
            message=f"User '{username}' not found",
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    @staticmethod
    def user_already_exists(username: str) -> HTTPException:
        return create_error_response(
            message=f"User '{username}' already exists",
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    @staticmethod
    def database_error() -> HTTPException:
        return create_error_response(
            message="Database operation failed",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    @staticmethod
    def validation_error(message: str) -> HTTPException:
        return create_error_response(
            message=f"Validation error: {message}",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )
