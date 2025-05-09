# services/gnn_service.py

import re
from typing import List, Tuple
from schemas.node_schema import NodeCreate
from schemas.edge_schema import EdgeCreate
from models.enums import OriginType, RelationType, Direction

SENTENCE_SPLIT_PATTERN = re.compile(r'[。\.!\?]\s*')


def split_into_chunks(text: str) -> List[str]:
    """
    将长文本按句号、问号、感叹号等标点分割为若干短描述片段。
    """
    parts = SENTENCE_SPLIT_PATTERN.split(text)
    return [p.strip() for p in parts if p.strip()]


def summarize_chunk(chunk: str, max_len: int = 80) -> str:
    """
    简单截断或摘要：这里做最基础的截断，
    你也可以接入专门的摘要模型来生成更精炼的标题。
    """
    return (chunk[:max_len] + '...') if len(chunk) > max_len else chunk


def parse_text_to_graph(
        parent_id: int,
        text: str,
        parent_depth: int
) -> Tuple[List[NodeCreate], List[EdgeCreate]]:
    """
    将 GPT 生成的长文本解析为子节点与边。

    Args:
      parent_id: 父节点在数据库中的 ID，用以构造 EdgeCreate
      text: GPT 生成的长文本
      parent_depth: 父节点的 expansion_depth

    Returns:
      nodes: 待创建的子节点列表
      edges: 对应的 EdgeCreate 列表
    """
    chunks = split_into_chunks(text)
    nodes: List[NodeCreate] = []
    edges: List[EdgeCreate] = []

    for idx, chunk in enumerate(chunks):
        title = summarize_chunk(chunk)
        # 构造新节点
        node = NodeCreate(
            title=title,
            description=chunk,
            is_seed=False,
            expansion_depth=parent_depth + 1,
            origin=OriginType.AUTO,
            type=None,  # 可留空，后续由业务填充或默认
            content=None,
            tags=None,
            metadata=None
        )
        nodes.append(node)

        # 构造新边
        edge = EdgeCreate(
            source_id=parent_id,
            target_id=None,  # 创建时先为 None，后端逻辑在持久化后补充实际 target_id
            relation_type=RelationType.RELATED,
            direction=Direction.DIRECTED,
            origin=OriginType.AUTO,
            weight=1.0,
            metadata=None
        )
        edges.append(edge)

    return nodes, edges
