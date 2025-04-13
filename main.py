from fastapi import FastAPI, Depends, HTTPException, Body
from neo4j import Session as NeoSession
from sqlalchemy import text, select
from sqlalchemy.orm import Session

from core.database import get_db
from core.neo4jConfig import get_neo4j
from models.node import Node
from schemas.node_schema import NodeResponse, NodeCreate, NodeUpdate
from services.gnn_service import parse_text_to_graph
from services.gpt_service import generate_text
from utils.lifespan import lifespan

app = FastAPI(lifespan=lifespan)

# router = APIRouter(prefix="/nodes", tags=["Nodes"])


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/postgres-check")
def postgres_check(db: Session = Depends(get_db)):
    # 测试PostgreSQL连接
    try:
        db.execute(text("SELECT 1"))
        return {"status": "PostgreSQL Connected"}
    except Exception as e:
        return {"status": "Error", "detail": str(e)}


@app.get("/neo4j-check")
def neo4j_check(session: NeoSession = Depends(get_neo4j)):
    # 测试Neo4j连接
    try:
        result = session.run("RETURN 1 AS result")
        value = result.single()["result"]
        return {"status": "Neo4j Connected", "value": value}
    except Exception as e:
        return {"status": "Error", "detail": str(e)}


@app.post("/expand", summary="根据用户提示扩展图结构")
def expand_prompt(prompt: str = Body(..., embed=True, description="用户输入的待扩展文本"),
                  max_length: int = Body(200, description="生成文本的最长长度")):
    """
    完整流程：接收用户输入 -> GPT 生成扩展文本 -> GNN 解析文本为图结构。
    """
    try:
        # 调用 GPT 服务生成长文本
        generated_text = generate_text(prompt, max_length=max_length)
        # 调用 GNN 服务将生成文本转为图结构
        graph = parse_text_to_graph(generated_text)
        return {
            "prompt": prompt,
            "generated_text": generated_text,
            "graph": graph
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/nodes/", response_model=NodeResponse)
def create_node(node: NodeCreate, db: Session = Depends(get_db)):
    db_node = Node(**node.model_dump(exclude_unset=True))
    db.add(db_node)
    db.commit()
    db.refresh(db_node)
    return db_node


@app.get("/nodes/{node_id}", response_model=NodeResponse)
def read_node(node_id: int, db: Session = Depends(get_db)):
    stmt = select(Node).where(Node.id == node_id)  # type: ignore

    db_node = db.execute(stmt).scalar_one_or_none()
    if not db_node:
        raise HTTPException(status_code=404, detail="Node not found")

    return db_node


@app.patch("/nodes/{node_id}", response_model=NodeResponse)
def update_node(node_id: int, node: NodeUpdate, db: Session = Depends(get_db)):
    db_node = db.query(Node).filter(Node.id == node_id).first() # type: ignore
    if not db_node:
        raise HTTPException(status_code=404, detail="Node not found")

    node_data = node.model_dump(exclude_unset=True)
    for key, value in node_data.items():
        setattr(db_node, key, value)

    db.commit()
    db.refresh(db_node)
    return db_node