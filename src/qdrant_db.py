from pathlib import Path
from qdrant_client import QdrantClient


# Local storage location for Qdrant
QDRANT_PATH = Path(__file__).resolve().parent.parent / "qdrant_storage"

# Collection name
COLLECTION_NAME = "programming_languages"


def get_qdrant_client():
    """
    Creates and returns a local Qdrant client.
    """
    client = QdrantClient(path=str(QDRANT_PATH))
    return client


if __name__ == "__main__":
    client = get_qdrant_client()

    print("Qdrant client created successfully!")
    print("Storage location:", QDRANT_PATH)

    client.close()
    print("Qdrant client closed successfully!")