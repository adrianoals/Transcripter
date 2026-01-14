# 9-Analisando prompt de analise de componentes (Resumo)

## 1) O que é

Prompt estruturado para análise detalhada de componentes individuais de uma aplicação. Foca em compreensão em nível de componente (diferente da análise arquitetural que é de alto nível).

## 2) Para que serve

Analisar cada componente listado no relatório de arquitetura de forma específica. Extrai lógicas de negócio, regras de validação, use cases, algoritmos, dependências, padrões de design e dívidas técnicas de cada componente.

## 3) Como é usado (como escrever / o que incluir no prompt e no comportamento)

**Persona e Escopo:**
- Especialista em análise de código e lógicas de negócio
- Extração de lógicas de negócio

**Objetivo:**
- Mapear estrutura e organização do componente
- Extrair regras de negócio, lógicas de validação, use cases, regras de domínio
- Analisar implementações, algoritmos e data flow
- Identificar dependências internas e externas
- Documentar design patterns e decisões arquiteturais
- Entender acoplamento, coesão e limites arquiteturais
- Identificar pontos de segurança, padrões de resiliência, dívidas técnicas

**Inputs:**
- Componente específico (serviços, diretórios do report de arquitetura)
- Arquivos e implementações
- Interfaces, testes, documentações
- Arquivos de configuração
- Dependências e imports
- Opcional: arquivo de arquitetura para ver componentes críticos

**Output:**
- Executive summary
- Data flow (passo a passo do componente)
- Business rules overview (tabela: tipo, descrição, arquivo, linha)
- Business rules detail (nome, visão geral, descrição detalhada, workflow)
- Component structure
- Dependency analysis (nível baixo, aferente/eferente)
- Endpoints (se existir: REST, GraphQL, gRPC)
- Integration points
- Patterns utilizados
- Technical risks
- Test coverage analysis

**Critérios:**
- Análise específica do componente passado
- Extração detalhada de regras de negócio
- Análise de dependências em nível baixo
- Documentação de padrões e decisões

**Instruções Negativas:**
- Não modificar código
- Não sugerir melhorias
- Não criar diagramas
- Não assumir informações sem evidência

## 4) Onde pode ser usado (casos de uso)

- Análise detalhada de componentes críticos
- Extração de regras de negócio
- Documentação de componentes
- Análise antes de refatoração de componentes específicos

## 5) Limitações / quando evitar

Para componentes muito grandes, pode precisar de sub-análises ou divisão em subcomponentes. Depende do tamanho e complexidade do componente.

## 6) Observações de prática (coisas que dá pra notar quando testa no dia a dia)

Pode ser mais agressivo na leitura de arquivos porque está analisando apenas um componente (menos arquivos que o projeto todo). O workflow ajuda a organizar a análise. Usar XML ou placeholders ajuda a IA a entender onde escrever cada seção. Quanto mais específico o componente, melhor a análise.
