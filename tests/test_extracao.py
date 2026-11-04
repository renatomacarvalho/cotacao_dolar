from cotacao_dolar.extraction.extracao import extrair_cotacao


def test_extrair_cotacao():

    dados = extrair_cotacao()

    assert dados is not None
    assert len(dados) > 0
