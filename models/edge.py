from sqlalchemy import (
    Column, Integer, ForeignKey, Float,
    DateTime, Enum as SqlEnum, JSON, func
)
from sqlalchemy.orm import relationship
from models.base import Base
from models.enums import OriginType, RelationType, Direction

class Edge(Base):
    __tablename__ = "edges"

    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(Integer, ForeignKey("nodes.id"), nullable=False)
    target_id = Column(Integer, ForeignKey("nodes.id"), nullable=False)

    # 语义类型与方向
    relation_type = Column(SqlEnum(RelationType), nullable=False, default=RelationType.RELATED)
    direction = Column(SqlEnum(Direction), nullable=False, default=Direction.DIRECTED)

    # 来源标记：手动添加 or 自动生成
    origin = Column(SqlEnum(OriginType), default=OriginType.AUTO, nullable=False)
    # 关系权重
    weight = Column(Float, default=1.0, nullable=False)

    # 额外元数据
    metadata = Column(JSON, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    source = relationship("Node", back_populates="outgoing", foreign_keys=[source_id])
    target = relationship("Node", back_populates="incoming", foreign_keys=[target_id])
