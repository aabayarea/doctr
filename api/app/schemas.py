from typing import Tuple

from pydantic import BaseModel, Field


class RecognitionOut(BaseModel):
    value: str = Field(..., example="Hello")


class DetectionOut(BaseModel):
    box: Tuple[float, float, float, float]


class OCROut(RecognitionOut, DetectionOut):
    page_num: int  # Add this line
