from typing import Optional

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from core.database import get_db
from models.node import Node
from schemas.node_schema import NodeResponse
from services.gnn_service import parse_text_to_graph
from services.gpt_service import generate_expansion_text

router = APIRouter()

@router.post("/nodes/{node_id}/expand", response_model=list[NodeResponse])
def expand_node(node_id: int, db: Session = Depends(get_db)):
    # 1. 读取父节点
    parent: Optional[Node] = db.get(Node, node_id)
    if not parent:
        raise HTTPException(404, "Parent node not found")

    # 2. 调用 GPT 生成扩展文本
    text = generate_expansion_text(parent.title, parent.description, parent.expansion_depth)

    # 3. 调用 GNN 服务解析成子节点 & 边
    new_nodes, new_edges = parse_text_to_graph(parent_id=parent.id, text=text, parent_depth=parent.expansion_depth)

    # 4. 持久化：先创建节点，再创建边并补充target_id
    created_nodes = []
    for node_data in new_nodes:
        n = Node(**node_data.model_dump())
        db.add(n); db.flush()  # flush 以获得 n.id
        created_nodes.append(n)
    db.commit()

    # 5. 创建边
    created_edges = []
    for edge_data, child_node in zip(new_edges, created_nodes):
        edge_data.target_id = child_node.id
        from models.edge import Edge
        e = Edge(**edge_data.model_dump())
        db.add(e)
        created_edges.append(e)
    db.commit()

    return created_nodes
