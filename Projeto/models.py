from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
import random

# cada Categoria receberá uma cor aleatória para suas cartas
def random_color():
    return f"#{random.randint(0, 0xFFFFFF):06x}"


class Categoria(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str = Field(index=True, unique=True)
    cor: str = Field(default_factory=random_color)

    bagulhos: List["Bagulho"] = Relationship(back_populates="categoria")


class Bagulho(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str = Field(index=True, unique=True)
    imagem: Optional[str] = None
    score: int = 0

    categoria_id: Optional[int] = Field(default=None, foreign_key="categoria.id")
    categoria: Optional[Categoria] = Relationship(back_populates="bagulhos")