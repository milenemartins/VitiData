import pytest
from pydantic import ValidationError
from app.schemas.vinho import (
    VinhoBase, VinhoEntrada, VinhoSaida,
    ComercializacaoItem,
    ComercioExteriorBase, ComercioEntrada, ComercioSaida
)

# ----------------------
# Testes VinhoEntrada
# ----------------------

def test_vinho_entrada_valido():
    vinho = VinhoEntrada(ano=2020, tipo="Tinto", quantidade=100.0)
    assert vinho.ano == 2020
    assert vinho.tipo == "Tinto"
    assert vinho.quantidade == 100.0

def test_vinho_entrada_ano_invalido_abaixo():
    with pytest.raises(ValidationError):
        VinhoEntrada(ano=1969, tipo="Tinto", quantidade=50.0)

def test_vinho_entrada_ano_invalido_acima():
    with pytest.raises(ValidationError):
        VinhoEntrada(ano=2101, tipo="Tinto", quantidade=50.0)

def test_vinho_entrada_quantidade_negativa():
    with pytest.raises(ValidationError):
        VinhoEntrada(ano=2020, tipo="Branco", quantidade=-10)

# ----------------------
# Testes VinhoSaida
# ----------------------

def test_vinho_saida_com_id():
    vinho = VinhoSaida(id=1, ano=2021, tipo="Rosé", quantidade=80.0)
    assert vinho.id == 1

def test_vinho_saida_sem_id():
    vinho = VinhoSaida(ano=2021, tipo="Rosé", quantidade=80.0)
    assert vinho.id is None

# ----------------------
# Testes VinhoBase
# ----------------------

def test_vinho_base_valido():
    vinho = VinhoBase(ano=2000, tipo="Espumante", quantidade=10.0)
    assert vinho.tipo == "Espumante"

def test_vinho_base_quantidade_zero():
    vinho = VinhoBase(ano=1999, tipo="Branco", quantidade=0.0)
    assert vinho.quantidade == 0.0

# ----------------------
# Testes ComercializacaoItem
# ----------------------

def test_comercializacao_item_valido():
    item = ComercializacaoItem(produto="Vinho do Porto", quantidade_litros=50.0)
    assert item.produto == "Vinho do Porto"
    assert item.quantidade_litros == 50.0

# ----------------------
# Testes ComercioEntrada
# ----------------------

def test_comercio_entrada_valido():
    entrada = ComercioEntrada(ano=2022, pais="Chile", categoria="Importação", quantidade=1000, valor=50000)
    assert entrada.pais == "Chile"
    assert entrada.valor == 50000

# ----------------------
# Testes ComercioSaida
# ----------------------

def test_comercio_saida_valido_com_id():
    saida = ComercioSaida(id=7, ano=2023, pais="Portugal", categoria="Exportação", quantidade=2000, valor=90000)
    assert saida.id == 7

def test_comercio_saida_valido_sem_id():
    saida = ComercioSaida(ano=2023, pais="Espanha", categoria="Exportação", quantidade=1500, valor=70000)
    assert saida.id is None

def test_comercio_saida_quantidade_negativa():
    with pytest.raises(ValidationError):
        ComercioSaida(ano=2024, pais="Argentina", categoria="Importação", quantidade=-100, valor=3000)

def test_comercio_saida_valor_negativo():
    with pytest.raises(ValidationError):
        ComercioSaida(ano=2024, pais="Argentina", categoria="Importação", quantidade=100, valor=-3000)

def test_comercio_saida_ano_fora_do_limite():
    with pytest.raises(ValidationError):
        ComercioSaida(ano=2150, pais="Argentina", categoria="Importação", quantidade=100, valor=3000)

# ----------------------
# Testes ComercioExteriorBase
# ----------------------

def test_comercio_exterior_base_valido():
    base = ComercioExteriorBase(ano=2021, pais="Itália", categoria="Exportação", quantidade=500.0, valor=25000.0)
    assert base.categoria == "Exportação"
    assert base.quantidade == 500.0

def test_comercio_exterior_base_ano_invalido():
    with pytest.raises(ValidationError):
        ComercioExteriorBase(ano=1500, pais="Itália", categoria="Exportação", quantidade=500.0, valor=25000.0)
