from typing import Any, Dict, Optional
import aiohttp
from aiohttp import ClientTimeout
from fastapi import HTTPException

class HTTPClient:
    def __init__(self, base_url: str = None, timeout: int = 30):
        """Initialize async HTTP client with optional base URL and timeout
        
        Args:
            base_url: Base URL for all requests
            timeout: Timeout in seconds
        """
        self.base_url = base_url
        self.timeout = ClientTimeout(total=timeout)
        self.session = None
        
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession(
            base_url=self.base_url,
            timeout=self.timeout,
            raise_for_status=True
        )
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):  
        """Async context manager exit"""
        if self.session:
            await self.session.close()
            
    async def ensure_session(self):
        """Ensure session exists"""
        if self.session is None:
            self.session = aiohttp.ClientSession(
                base_url=self.base_url,
                timeout=self.timeout,
                raise_for_status=True
            )
    
    async def get(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Make async GET request
        
        Args:
            url: Endpoint URL
            params: Query parameters
            headers: Request headers
            
        Returns:
            Response data as dictionary
            
        Raises:
            HTTPException: If request fails
        """
        await self.ensure_session()
        
        try:
            async with self.session.get(url, params=params, headers=headers) as response:
                return await response.json()
                
        except aiohttp.ClientResponseError as e:
            print(e)
            raise HTTPException(
                status_code=e.status,
                detail=f"HTTP error occurred: {str(e)}"
            )
        except aiohttp.ClientError as e:
            print(e)
            raise HTTPException(
                status_code=500,
                detail=f"Request error occurred: {str(e)}"
            )
    
    async def post(
        self,
        url: str,
        json: Optional[Dict[str, Any]] = None,
        data: Any = None,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make async POST request
        
        Args:
            url: Endpoint URL
            json: JSON body data
            data: Form data or other content
            headers: Request headers
            params: Query parameters
            
        Returns:
            Response data as dictionary
            
        Raises:
            HTTPException: If request fails
        """
        await self.ensure_session()
        
        try:
            async with self.session.post(
                url,
                json=json,
                data=data,
                headers=headers,
                params=params
            ) as response:
                return await response.json()
                
        except aiohttp.ClientResponseError as e:
            raise HTTPException(
                status_code=e.status,
                detail=f"HTTP error occurred: {str(e)}"
            )
        except aiohttp.ClientError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Request error occurred: {str(e)}"
            )
            
    async def close(self):
        """Close the session"""
        if self.session:
            await self.session.close()
            self.session = None
