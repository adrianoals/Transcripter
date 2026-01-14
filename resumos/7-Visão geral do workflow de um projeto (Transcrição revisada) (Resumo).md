# 7-Visão geral do workflow de um projeto (Resumo)

## 1) O que é

Visão geral de como funciona um workflow multi-agentes para gerar um Project State (snapshot do projeto). Inclui arquitetura, dependências, componentes e análises específicas.

## 2) Para que serve

Gerar um snapshot completo do estado atual de um projeto: arquitetura, dependências, componentes com análises detalhadas. Útil para modernização de sistemas legados ou análise de projetos.

## 3) Como é usado (como escrever / o que incluir no prompt e no comportamento)

**Componentes do sistema:**
- Cloud Code: agente principal/coordenador
- Orquestrador: mantém tracking do progresso
- Agentes especialistas: fazem análises específicas (dependências, arquitetura, componentes)

**Fluxo:**
1. Comando é executado (prompt de workflow)
2. Cloud Code entende o passo a passo
3. Orquestrador faz setup (cria pastas, manifesto)
4. Agentes especialistas são chamados (em paralelo quando possível)
5. Orquestrador registra progresso no manifesto
6. Relatórios são gerados e consolidados

**Desafios:**
- Context window limitada (Cloud Code tenta compactar quando enche)
- Agentes não compartilham contexto entre si
- Gerenciamento de estado é crítico

## 4) Onde pode ser usado (casos de uso)

- Análise de projetos grandes
- Modernização de sistemas legados
- Documentação de arquitetura
- Análise de componentes críticos

## 5) Limitações / quando evitar

IA trabalha de forma probabilística, não determinística. Mesmo com orquestrador, não garante 100% de confiabilidade. Pode precisar de frameworks mais determinísticos (como LangGraph) para casos críticos.

## 6) Observações de prática (coisas que dá pra notar quando testa no dia a dia)

O manifesto ajuda a saber onde parou se a execução for interrompida. Agentes em paralelo são mais rápidos, mas o tracking pode ser menos em tempo real. É um trade-off: tracking mais frequente = execução mais lenta, mas mais seguro.
