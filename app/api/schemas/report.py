from pydantic import BaseModel
from typing import List


class InsightItem(BaseModel):
    timestamp: str
    insight: str


class ReportResponse(BaseModel):
    status: str
    data: List[InsightItem]
