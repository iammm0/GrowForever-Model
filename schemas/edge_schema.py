from pydantic import BaseModel, Field
from typing import Optional, Dict
from datetime import datetime
from models.enums import OriginType, RelationType, Direction

class EdgeBase(BaseModel):
    source_id: int
    target_id: int
    relation_type: RelationType = Field(..., description="关系语义类型")
    direction: Direction = Field(..., description="关系方向")
    origin: Optional[OriginType] = Field(OriginType.AUTO, description="链接来源")
    weight: Optional[float] = Field(1.0, description="关系强度")
    metadata: Optional[Dict[str, any]] = None

class EdgeCreate(EdgeBase):
    pass

class EdgeResponse(EdgeBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
