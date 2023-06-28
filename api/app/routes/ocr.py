# Copyright (C) 2021-2023, Mindee.

# This program is licensed under the Apache License 2.0.
# See LICENSE or go to <https://opensource.org/licenses/Apache-2.0> for full license details.

from typing import List
from fastapi import APIRouter, File, UploadFile, status
from app.schemas import OCROut
from app.vision import predictor
from doctr.io import DocumentFile
from doctr.models import ocr_predictor
import os
import uuid
import re
import uuid
import os


def secure_filename(filename):
    """
    This function removes any inappropriate characters from the filename to ensure it is secure
    """
    return re.sub(r'(?u)[^-\w.]', '', filename)


router = APIRouter()

model = ocr_predictor('linknet_resnet18_rotation', pretrained=True, assume_straight_pages=False, preserve_aspect_ratio=True)

@router.post("/", response_model=List[OCROut], status_code=status.HTTP_200_OK, summary="Perform OCR")
async def perform_ocr(file: UploadFile = File(...)):
    """Runs docTR OCR model to analyze the input PDF file"""
    # Save the uploaded file to a temporary location
    filename = secure_filename(file.filename)
    file_path = os.path.join("/tmp", f"{uuid.uuid4().hex}_{filename}")
    with open(file_path, 'wb') as buffer:
        buffer.write(file.file.read())

    doc = DocumentFile.from_pdf(file_path)
    result = model(doc)

    # Delete the temporary file
    os.remove(file_path)

    output = result.export()
    
    return [
        OCROut(box=(*word['geometry'][0], *word['geometry'][1]), value=word['value'])
        for page in output['pages']
        for block in page['blocks']
        for line in block['lines']
        for word in line['words']
    ]
