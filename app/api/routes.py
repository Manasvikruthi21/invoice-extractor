from pathlib import Path
import shutil
import tempfile

from fastapi import APIRouter, UploadFile, File, HTTPException

from app.graph.workflow import graph

router = APIRouter(
    prefix="/api/v1",
    tags=["Document Intelligence"],
)


@router.post("/process")
async def process_document(
    file: UploadFile = File(...),
):
    try:

        # -------------------------------------------------
        # Save uploaded file temporarily
        # -------------------------------------------------

        suffix = Path(file.filename).suffix

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix,
        ) as tmp:

            shutil.copyfileobj(file.file, tmp)

            temp_path = tmp.name

        # -------------------------------------------------
        # Initial LangGraph State
        # -------------------------------------------------

        state = {

            "file_path": temp_path,

            "ocr_result": None,

            "extracted_text": None,

            "classification": None,

            "extracted_data": None,

            "validation": None,

            "confidence": None,

            "final_result": None,

        }

        # -------------------------------------------------
        # Execute LangGraph Workflow
        # -------------------------------------------------

        result = graph.invoke(state)

        # -------------------------------------------------
        # Return Final Response
        # -------------------------------------------------

        return result["final_result"]

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )

    finally:

        # -------------------------------------------------
        # Delete Temporary File
        # -------------------------------------------------

        try:
            Path(temp_path).unlink(missing_ok=True)
        except Exception:
            pass