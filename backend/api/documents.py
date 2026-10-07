import os
import shutil
from uuid import uuid4

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Form,
    HTTPException,
)

from config import settings

from ingestion.pdf_loader import (
    extract_pdf_pages,
    get_pdf_page_count,
)

from ingestion.chunker import (
    chunk_text,
)

from ingestion.metadata import (
    create_metadata,
)

from retrieval.vector_retriever import (
    vector_retriever,
)

from models.schemas import (
    UploadResponse,
)


router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


UPLOAD_DIR = "uploads"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True,
)


@router.post(
    "/upload",
    response_model=UploadResponse,
)
async def upload_document(

    file: UploadFile = File(...),

    user_id: str = Form(
        "anonymous"
    ),
):

    # -------------------------
    # Validate filename
    # -------------------------

    if not file.filename:

        raise HTTPException(
            status_code=400,
            detail="Filename is required.",
        )

    # -------------------------
    # Validate extension
    # -------------------------

    if not file.filename.lower().endswith(
        ".pdf"
    ):

        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed.",
        )

    document_id = str(
        uuid4()
    )

    file_path = os.path.join(
        UPLOAD_DIR,
        f"{document_id}.pdf",
    )

    try:

        # -------------------------
        # Save file
        # -------------------------

        with open(
            file_path,
            "wb",
        ) as buffer:

            shutil.copyfileobj(
                file.file,
                buffer,
            )

        # -------------------------
        # File size validation
        # -------------------------

        file_size = os.path.getsize(
            file_path
        )

        max_size = (
            settings.max_file_size_mb
            * 1024
            * 1024
        )

        if file_size > max_size:

            raise HTTPException(

                status_code=413,

                detail=(
                    f"File exceeds "
                    f"{settings.max_file_size_mb} MB."
                ),
            )

        # -------------------------
        # Page count
        # -------------------------

        page_count = (
            get_pdf_page_count(
                file_path
            )
        )

        if page_count > settings.max_pages:

            raise HTTPException(

                status_code=400,

                detail=(
                    f"PDF exceeds "
                    f"{settings.max_pages} pages."
                ),
            )

        # -------------------------
        # Extract text
        # -------------------------

        pages = (
            extract_pdf_pages(
                file_path
            )
        )

        # -------------------------
        # Create chunks
        # -------------------------

        chunks = []

        for page in pages:

            page_chunks = (
                chunk_text(
                    page["text"]
                )
            )

            for index, text in enumerate(
                page_chunks
            ):

                chunk_id = (
                    f"{document_id}_"
                    f"{page['page_number']}_"
                    f"{index}"
                )

                metadata = (
                    create_metadata(

                        document_id=(
                            document_id
                        ),

                        document_name=(
                            file.filename
                        ),

                        page_number=(
                            page["page_number"]
                        ),

                        chunk_id=chunk_id,

                        user_id=user_id,
                    )
                )

                chunks.append({

                    "text": text,

                    "metadata": metadata,
                })

        # -------------------------
        # No text
        # -------------------------

        if not chunks:

            raise HTTPException(

                status_code=400,

                detail=(
                    "No readable text "
                    "was found in the PDF."
                ),
            )

        # -------------------------
        # Store embeddings
        # -------------------------

        count = (
            vector_retriever.add_documents(
                chunks
            )
        )

        return UploadResponse(

            document_id=document_id,

            filename=file.filename,

            chunks_created=count,

            user_id=user_id,

            message=(
                "PDF uploaded and "
                "indexed successfully."
            ),
        )

    finally:

        # We don't need to keep the
        # original PDF on disk for
        # this first version.

        if os.path.exists(
            file_path
        ):

            os.remove(
                file_path
            )