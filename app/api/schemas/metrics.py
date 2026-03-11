from pydantic import BaseModel
from typing import List


class MetricItem(BaseModel):
    engagement: float
    clarity: float
    interaction: float
    final_score: float


class MetricsResponse(BaseModel):
    status: str
    data: List[MetricItem]
