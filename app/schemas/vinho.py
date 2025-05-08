from pydantic import BaseModel, Field
from typing import Optional


# Produção, Processamento e Comercialização
class VinhoBase(BaseModel):
    ano: int = Field(..., ge=1970, le=2100)
    tipo: str
    quantidade: float = Field(..., ge=0)

class VinhoEntrada(BaseModel):
    ano: int = Field(..., ge=1970, le=2100)
    tipo: str
    quantidade: float = Field(..., ge=0)

class VinhoSaida(VinhoBase):
    id: Optional[int] = None
    
class ComercializacaoItem(BaseModel):
    produto: str
    quantidade_litros: float


# Importação e Exportação
class ComercioExteriorBase(BaseModel):
    ano: int = Field(..., ge=1970, le=2100)
    categoria: str
    pais: str
    quantidade: float = Field(..., ge=0)
    valor: float = Field(..., ge=0)

class ComercioEntrada(BaseModel):
    ano: int
    pais: str
    categoria: str
    quantidade: float
    valor: float

class ComercioSaida(ComercioExteriorBase):
    id: Optional[int] = None
