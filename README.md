# Automação Inteligente de Demandas

Aplicação desenvolvida em Python para realizar a triagem de demandas administrativas fictícias, classificando solicitações, identificando prioridades, sugerindo encaminhamentos e alimentando um dashboard gerencial.

O fluxo mantém revisão humana nos casos com informações insuficientes, classificação ambígua ou baixa confiança.

## Funcionalidades

- Cadastro de demandas administrativas fictícias
- Classificação automática por categoria
- Identificação de prioridade
- Sugestão de encaminhamento
- Sinalização de casos para revisão humana
- Histórico de solicitações
- Dashboard com indicadores e gráficos
- Exportação do histórico em CSV

## Tecnologias utilizadas

- Python
- Streamlit
- Pandas
- CSV

## Critérios de classificação

A aplicação utiliza regras e palavras-chave para demonstrar o processo de triagem. Casos com descrição muito curta, categorias ambíguas ou baixa confiança são encaminhados para revisão humana.

> Este é um projeto demonstrativo. Todos os dados utilizados são fictícios e a classificação automática não substitui a decisão humana.

## Como executar

1. Clone este repositório.
2. Abra a pasta no VS Code.
3. Crie e ative um ambiente virtual.
4. Instale as dependências:

```bash
pip install -r requirements.txt
```

5. Execute a aplicação:

```bash
streamlit run app.py
```

## Estrutura do projeto

```text
automacao-inteligente-demandas/
├── dados/
│   └── demandas.csv
├── app.py
├── classificador.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Autora

**Amanda Gomes Damascena**

Estudante de Engenharia de Software e Técnica em Informática.
