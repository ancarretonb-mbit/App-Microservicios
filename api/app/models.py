from sqlalchemy import Table, Column, String, Float, ForeignKey, MetaData
from sqlalchemy.orm import relationship, registry

mapper_registry = registry()
metadata = MetaData()

# Tabla de pictures
pictures_table = Table(
    "pictures",
    metadata,
    Column("id", String(36), primary_key=True),
    Column("path", String(255), nullable=False),
    Column("date", String(19), nullable=False),
)

# Tabla de tags
tags_table = Table(
    "tags",
    metadata,
    Column("tag", String(32), primary_key=True),
    Column("picture_id", String(36), ForeignKey("pictures.id"), primary_key=True),
    Column("confidence", Float, nullable=False),
    Column("date", String(19), nullable=False),
)

# Clases ORM
class Picture:
    def __init__(self, id, path, date):
        self.id = id
        self.path = path
        self.date = date
        self.tags = []

class Tag:
    def __init__(self, tag, picture_id, confidence, date):
        self.tag = tag
        self.picture_id = picture_id
        self.confidence = confidence
        self.date = date

# Mapear clases a tablas
mapper_registry.map_imperatively(Picture, pictures_table, properties={
    "tags": relationship(Tag, backref="picture")
})
mapper_registry.map_imperatively(Tag, tags_table)
