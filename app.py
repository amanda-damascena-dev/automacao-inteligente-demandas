from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st

from classificador import classificar_demanda


BASE_DIR = Path(__file__).resolve().parent
ARQUIVO_DADOS = BASE_DIR / "dados" / "demandas.csv"

COLUNAS = [
    "id", "data", "solicitante", "titulo", "descricao", "categoria",
    "prioridade", "encaminhamento", "confianca", "revisao_humana",
    "motivo_revisao", "status",
]


def carregar_dados() -> pd.DataFrame:
    ARQUIVO_DADOS.parent.mkdir(parents=True, exist_ok=True)
    if not ARQUIVO_DADOS.exists():
        pd.DataFrame(columns=COLUNAS).to_csv(
            ARQUIVO_DADOS, index=False, encoding="utf-8-sig"
        )
    return pd.read_csv(ARQUIVO_DADOS)


def salvar_demanda(demanda: dict) -> None:
    dados = carregar_dados()
    novo_id = 1 if dados.empty else int(dados["id"].max()) + 1
    registro = {"id": novo_id, **demanda}
    dados = pd.concat([dados, pd.DataFrame([registro])], ignore_index=True)
    dados.to_csv(ARQUIVO_DADOS, index=False, encoding="utf-8-sig")


st.set_page_config(
    page_title="Automação Inteligente de Demandas",
    page_icon="⚙️",
    layout="wide",
)

st.title("⚙️ Automação Inteligente de Demandas")
st.caption(
    "Triagem de solicitações administrativas fictícias com classificação, "
    "priorização, encaminhamento e revisão humana."
)

aba_triagem, aba_dashboard, aba_historico = st.tabs(
    ["Nova demanda", "Dashboard", "Histórico"]
)

with aba_triagem:
    st.subheader("Cadastrar solicitação")
    with st.form("formulario_demanda", clear_on_submit=True):
        solicitante = st.text_input("Solicitante fictício")
        titulo = st.text_input("Título da demanda")
        descricao = st.text_area(
            "Descrição",
            placeholder="Ex.: Não consigo acessar o sistema e preciso concluir o trabalho hoje.",
        )
        enviar = st.form_submit_button("Classificar e registrar")

    if enviar:
        if not solicitante.strip() or not titulo.strip() or not descricao.strip():
            st.error("Preencha todos os campos antes de continuar.")
        else:
            resultado = classificar_demanda(titulo, descricao)
            demanda = {
                "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "solicitante": solicitante.strip(),
                "titulo": titulo.strip(),
                "descricao": descricao.strip(),
                **resultado,
                "status": "Aguardando revisão" if resultado["revisao_humana"] else "Triada",
            }
            salvar_demanda(demanda)

            st.success("Demanda registrada com sucesso!")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Categoria", resultado["categoria"])
            col2.metric("Prioridade", resultado["prioridade"])
            col3.metric("Confiança", f'{resultado["confianca"]}%')
            col4.metric(
                "Revisão humana",
                "Sim" if resultado["revisao_humana"] else "Não",
            )
            st.info(f'Encaminhamento sugerido: {resultado["encaminhamento"]}')
            if resultado["revisao_humana"]:
                st.warning(
                    "A classificação deve ser conferida por uma pessoa: "
                    f'{resultado["motivo_revisao"]}.'
                )

with aba_dashboard:
    st.subheader("Visão gerencial")
    dados = carregar_dados()
    if dados.empty:
        st.info("Cadastre uma demanda para visualizar os indicadores.")
    else:
        revisoes = dados["revisao_humana"].astype(str).str.lower().eq("true").sum()
        col1, col2, col3 = st.columns(3)
        col1.metric("Total de demandas", len(dados))
        col2.metric("Revisões humanas", int(revisoes))
        col3.metric(
            "Demandas urgentes",
            int((dados["prioridade"] == "Urgente").sum()),
        )

        col_esquerda, col_direita = st.columns(2)
        with col_esquerda:
            st.markdown("#### Demandas por categoria")
            st.bar_chart(dados["categoria"].value_counts())
        with col_direita:
            st.markdown("#### Demandas por prioridade")
            st.bar_chart(dados["prioridade"].value_counts())

with aba_historico:
    st.subheader("Demandas registradas")
    dados = carregar_dados()
    if dados.empty:
        st.info("Ainda não existem demandas registradas.")
    else:
        filtro = st.selectbox(
            "Filtrar por prioridade",
            ["Todas", "Urgente", "Alta", "Média", "Baixa"],
        )
        exibicao = dados if filtro == "Todas" else dados[dados["prioridade"] == filtro]
        st.dataframe(exibicao, use_container_width=True, hide_index=True)
        st.download_button(
            "Baixar histórico em CSV",
            data=exibicao.to_csv(index=False).encode("utf-8-sig"),
            file_name="historico_demandas.csv",
            mime="text/csv",
        )

st.divider()
st.caption(
    "Projeto demonstrativo com dados fictícios. A classificação automática "
    "apoia a triagem, mas não substitui a decisão humana."
)
