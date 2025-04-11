from fastapi import FastAPI, Depends
from neo4j import Session as NeoSession
from sqlalchemy.orm import Session

from core.database import get_db
from core.neo4jConfig import get_neo4j

app = FastAPI()


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
        db.execute("SELECT 1")
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