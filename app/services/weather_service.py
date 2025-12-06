import httpx
from typing import Optional
import logging

logger = logging.getLogger(__name__)


async def get_temperature_for_city(city_name: str) -> Optional[float]:
    """
    Fetches current temperature for a city from wttr.in API.
    
    Args:
        city_name: City name
        
    Returns:
        Temperature in Celsius or None if data could not be fetched
        
    Raises:
        httpx.HTTPError: If HTTP request error occurred
    """
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            # URL for wttr.in API (free, no API key required)
            url = f"https://wttr.in/{city_name}?format=j1"
            response = await client.get(url)
            response.raise_for_status()  # Raises exception for HTTP errors
            
            data = response.json()
            
            # Extract temperature from response
            temperature = float(data["current_condition"][0]["temp_C"])
            
            logger.info(f"Fetched temperature for {city_name}: {temperature}°C")
            return temperature
            
    except httpx.HTTPError as e:
        logger.error(f"HTTP request error for {city_name}: {e}")
        return None
    except (KeyError, IndexError, ValueError) as e:
        logger.error(f"Data parsing error for {city_name}: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error for {city_name}: {e}")
        return None