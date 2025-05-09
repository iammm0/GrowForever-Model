from sqlalchemy.orm import declarative_base

# 生成一个“基类”，所有的 ORM 模型都继承自它
Base = declarative_base()
