import re


CATEGORIAS = {
    "Financeiro": [
        "pagamento", "boleto", "nota fiscal", "reembolso", "cobranca",
        "cobrança", "financeiro", "fatura", "valor",
    ],
    "Recursos Humanos": [
        "ferias", "férias", "folha", "contratacao", "contratação",
        "beneficio", "benefício", "atestado", "rh", "colaborador",
    ],
    "Tecnologia": [
        "sistema", "acesso", "senha", "computador", "erro", "internet",
        "software", "login", "ti", "tecnologia",
    ],
    "Compras": [
        "compra", "fornecedor", "orcamento", "orçamento", "material",
        "estoque", "pedido", "cotacao", "cotação",
    ],
    "Atendimento": [
        "cliente", "reclamacao", "reclamação", "atendimento", "retorno",
        "duvida", "dúvida", "solicitacao", "solicitação",
    ],
}

ENCAMINHAMENTOS = {
    "Financeiro": "Equipe Financeira",
    "Recursos Humanos": "Equipe de Recursos Humanos",
    "Tecnologia": "Suporte de Tecnologia",
    "Compras": "Setor de Compras",
    "Atendimento": "Central de Atendimento",
    "Não classificada": "Triagem Administrativa",
}

TERMOS_URGENTES = [
    "urgente", "imediato", "imediatamente", "prazo hoje", "bloqueado",
    "parado", "vencido", "sem acesso", "falha critica", "falha crítica",
]

TERMOS_ALTOS = [
    "prazo", "atrasado", "erro", "problema", "indisponivel",
    "indisponível", "nao funciona", "não funciona", "vencimento",
]


def _normalizar(texto: str) -> str:
    return re.sub(r"\s+", " ", texto.lower().strip())


def classificar_demanda(titulo: str, descricao: str) -> dict:
    texto = _normalizar(f"{titulo} {descricao}")

    pontuacoes = {
        categoria: sum(termo in texto for termo in termos)
        for categoria, termos in CATEGORIAS.items()
    }

    maior_pontuacao = max(pontuacoes.values(), default=0)
    empatadas = [
        categoria
        for categoria, pontuacao in pontuacoes.items()
        if pontuacao == maior_pontuacao and pontuacao > 0
    ]

    if maior_pontuacao == 0:
        categoria = "Não classificada"
        confianca = 0
    else:
        categoria = empatadas[0]
        confianca = min(95, 55 + (maior_pontuacao * 15))

    if any(termo in texto for termo in TERMOS_URGENTES):
        prioridade = "Urgente"
    elif any(termo in texto for termo in TERMOS_ALTOS):
        prioridade = "Alta"
    elif len(descricao.strip()) >= 40:
        prioridade = "Média"
    else:
        prioridade = "Baixa"

    informacao_insuficiente = len(descricao.strip()) < 15
    ambiguidade = len(empatadas) > 1
    baixa_confianca = confianca < 60
    revisao_humana = informacao_insuficiente or ambiguidade or baixa_confianca

    motivos = []
    if informacao_insuficiente:
        motivos.append("descrição muito curta")
    if ambiguidade:
        motivos.append("mais de uma categoria possível")
    if baixa_confianca:
        motivos.append("baixa confiança na classificação")

    return {
        "categoria": categoria,
        "prioridade": prioridade,
        "encaminhamento": ENCAMINHAMENTOS[categoria],
        "confianca": confianca,
        "revisao_humana": revisao_humana,
        "motivo_revisao": ", ".join(motivos) if motivos else "Não necessária",
    }
