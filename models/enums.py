import enum

class OriginType(enum.Enum):
    MANUAL = "manual"
    AUTO = "auto"

class RelationType(enum.Enum):
    RELATED = "related"
    SUB_CONCEPT = "sub_concept"
    CAUSES = "causes"
    INSPIRED_BY = "inspired_by"
    # …可继续扩充

class Direction(enum.Enum):
    DIRECTED = "directed"
    BIDIRECTIONAL = "bidirectional"
    UNDIRECTED = "undirected"

class NodeType(enum.Enum):
    IDEA = "idea"
    MEMORY = "memory"
    EMOTION = "emotion"
    FEATURE = "feature"
    EVENT = "event"
    USER_DEFINED = "user_defined"