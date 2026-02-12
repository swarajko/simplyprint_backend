
import httpx
from typing import List, Optional, Dict, Any
from app.core.config import settings
from app.models.datamodels import Printer


class SimplyPrintClient:
    
    def __init__(self):
        self.api_key = settings.simplyprint_api_key
        self.company_id = settings.simplyprint_company_id
        self.base_url = f"{settings.simplyprint_base_url}/{self.company_id}"
        self.headers = {
            "X-API-KEY": self.api_key,
            "Content-Type": "application/json"
        }
    
    async def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:

        url = f"{self.base_url}/{endpoint}"
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.request(
                    method=method,
                    url=url,
                    headers=self.headers,
                    json=data,
                    timeout=30.0
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as e:
            return {
                "status": False,
                "message": f"API request failed: {str(e)}"
            }
        except Exception as e:
            return {
                "status": False,
                "message": f"Unexpected error: {str(e)}"
            }
    
    async def list_printers(self) -> List[Printer]:

        response = await self._make_request("GET", "printers/Get")
        
        if not response.get("status", False):
            return []
        
        printers = []

        for printer_data in response.get("data", []):
            printer = Printer(
                id=str(printer_data.get("id", "")),
                name=printer_data.get("name", "Unknown Printer"),
                status=printer_data.get("status", "offline"),
                ip_address=printer_data.get("ip_address"),
                printer_type=printer_data.get("printer_type"),
                in_service=printer_data.get("is_online", False)
            )
            printers.append(printer)
        
        return printers
    
    async def get_printer_info(self, printer_id: str) -> Optional[Printer]:

        response = await self._make_request("GET", f"printers/Get/{printer_id}")
        
        if not response.get("status", False):
            return None
        
        printer_data = response.get("data", {})
        return Printer(
            id=str(printer_data.get("id", printer_id)),
            name=printer_data.get("name", "Unknown Printer"),
            status=printer_data.get("status", "offline"),
            ip_address=printer_data.get("ip_address"),
            printer_type=printer_data.get("printer_type"),
            in_service=printer_data.get("is_online", False)
        )
    
    async def start_print_job(self, printer_id: str, file_id: str) -> Dict[str, Any]:

        data = {
            "printer_id": printer_id,
            "file_id": file_id
        }
        return await self._make_request("POST", "printers/PrintJob", data)
    
    async def pause_print(self, printer_id: str) -> Dict[str, Any]:

        data = {"printer_id": printer_id}
        return await self._make_request("POST", "printers/PausePrint", data)
    
    async def resume_print(self, printer_id: str) -> Dict[str, Any]:

        data = {"printer_id": printer_id}
        return await self._make_request("POST", "printers/ResumePrint", data)
    
    async def cancel_print(self, printer_id: str) -> Dict[str, Any]:

        data = {"printer_id": printer_id}
        return await self._make_request("POST", "printers/CancelPrint", data)
