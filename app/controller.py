from fastapi import APIRouter, HTTPException
from bson import ObjectId
from .models import ResearchRequest
from .service import ResearchService
from .database import reports_collection

router = APIRouter()
service = ResearchService()

# -------------------------------------------------
# RESEARCH ENDPOINT
# -------------------------------------------------
@router.post("/research")
def research(request: ResearchRequest):

    if not request.query or request.query.strip() == "":
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    try:
        result = service.process_query(
            request.query,
            request.chat_history
        )

        return {
            "id": result["_id"],
            "query": result["query"],
            "report": result["report"],
            "timestamp": result["timestamp"]
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Research processing failed: {str(e)}"
        )


# -------------------------------------------------
# SEARCH HISTORY (FOR SIDEBAR LIST)
# -------------------------------------------------
@router.get("/search-history")
def search_history():

    try:
        history = list(
            reports_collection.find(
                {},
                {
                    "query": 1,
                    "timestamp": 1
                }
            )
            .sort("timestamp", -1)
            .limit(50)
        )

        for doc in history:
            doc["_id"] = str(doc["_id"])

        return history

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch history: {str(e)}"
        )


# -------------------------------------------------
# GET FULL REPORT (FOR LOADING OLD CONVERSATION)
# -------------------------------------------------
@router.get("/report/{report_id}")
def get_report(report_id: str):

    try:
        doc = reports_collection.find_one({"_id": ObjectId(report_id)})

        if not doc:
            raise HTTPException(status_code=404, detail="Report not found")

        # Convert ObjectId
        doc["_id"] = str(doc["_id"])

        # Ensure chat_history exists
        if "chat_history" not in doc:
            doc["chat_history"] = []

        return doc

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch report: {str(e)}"
        )
