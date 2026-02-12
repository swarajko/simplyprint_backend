from fastapi import APIRouter, HTTPException
from app.printers.simplyprint import SimplyPrintClient
from app.models.datamodels import Printer

router = APIRouter(prefix="/api/v1/printers", tags=["printers"])
simplyprint_client = SimplyPrintClient()


@router.get("/", response_model=dict)
async def list_printers():
    """Get list of all printers"""
    try:
        printers = await simplyprint_client.list_printers()
        return {"success": True, "printers": printers}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{printer_id}", response_model=dict)
async def get_printer(printer_id: str):
    """Get specific printer info"""
    try:
        printer = await simplyprint_client.get_printer_info(printer_id)
        if not printer:
            raise HTTPException(status_code=404, detail="Printer not found")
        return {"success": True, "printer": printer}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{printer_id}/start")
async def start_print_job(printer_id: str, file_id: str):
    """Start a print job"""
    try:
        response = await simplyprint_client.start_print_job(printer_id, file_id)
        return {"success": response.get("status", False), "message": response.get("message", "")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{printer_id}/pause")
async def pause_print(printer_id: str):
    """Pause print"""
    try:
        response = await simplyprint_client.pause_print(printer_id)
        return {"success": response.get("status", False), "message": response.get("message", "")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{printer_id}/resume")
async def resume_print(printer_id: str):
    """Resume print"""
    try:
        response = await simplyprint_client.resume_print(printer_id)
        return {"success": response.get("status", False), "message": response.get("message", "")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{printer_id}/cancel")
async def cancel_print(printer_id: str):
    """Cancel print"""
    try:
        response = await simplyprint_client.cancel_print(printer_id)
        return {"success": response.get("status", False), "message": response.get("message", "")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
