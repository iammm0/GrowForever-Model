from sqlalchemy import (
    Column, Integer, String, Text, Boolean,
    DateTime, Enum, JSON, func
)

from sqlalchemy.orm import relationship
from models.base import Base
from models.enums import OriginType, NodeType

class Node(Base):
    __tablename__ = "nodes"

    id = Column(Integer, primary_key=True, index=True)
    # 核心必填字段
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)

    # 种子节点与扩展层数
    is_seed = Column(Boolean, default=False, nullable=False)
    expansion_depth = Column(Integer, default=0, nullable=False)

    # 来源：手动或 GPT+GNN 自动生成
    origin = Column(Enum(OriginType), default=OriginType.MANUAL, nullable=False)
    # 节点类型（可选语义分类）
    type = Column(Enum(NodeType), default=NodeType.IDEA, nullable=False)

    # 可选的外部资源与多媒体
    content = Column(JSON, nullable=True)  # e.g. {"resource_links": [...], "media": [...]}
    # 标签列表
    tags = Column(JSON, nullable=True)     # e.g. ["tag1","tag2",...]

    # 额外任意元数据（如特征向量等）
    node_metadata = Column(JSON, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 与 Edge 的关系
    outgoing = relationship("Edge", back_populates="source", foreign_keys="Edge.source_id")
    incoming = relationship("Edge", back_populates="target", foreign_keys="Edge.target_id")