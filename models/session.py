from sqlalchemy.orm import relationship, Session

Session.nodes = relationship("Node", back_populates="session")