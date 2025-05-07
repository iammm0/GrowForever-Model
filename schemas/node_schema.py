from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from models.enums import OriginType, NodeType

class NodeContent(BaseModel):
    resource_links: Optional[List[str]] = Field(None, description="外部资源链接列表")
    media: Optional[List[str]] = Field(None, description="媒体文件 URL 列表")

class NodeBase(BaseModel):
    title: str = Field(..., max_length=255, description="节点标题（必填）")
    description: str = Field(..., description="节点描述（必填）")
    is_seed: Optional[bool] = Field(False, description="是否为种子节点")
    expansion_depth: Optional[int] = Field(0, description="扩展层数")
    origin: Optional[OriginType] = Field(OriginType.MANUAL, description="节点来源")
    type: Optional[NodeType] = Field(NodeType.IDEA, description="节点类型")
    content: Optional[NodeContent] = None
    tags: Optional[List[str]] = None
    metadata: Optional[Dict[str, any]] = None

class NodeCreate(NodeBase):
    pass

class NodeUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    is_seed: Optional[bool] = None
    expansion_depth: Optional[int] = None
    origin: Optional[OriginType] = None
    type: Optional[NodeType] = None
    content: Optional[NodeContent] = None
    tags: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None

class NodeResponse(NodeBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True