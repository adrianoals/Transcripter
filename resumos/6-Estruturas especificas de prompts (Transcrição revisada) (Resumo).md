# 6-Estruturas especificas de prompts (Resumo)

## 1) O que é

Dois tipos de prompts para trabalhar com múltiplos agentes: Workflow Specification Prompt (comando) e Role Specification (orquestrador). Permitem coordenar agentes de forma sequencial ou paralela.

## 2) Para que serve

Criar workflows complexos onde múltiplos agentes trabalham juntos. O comando define o fluxo de trabalho, e o orquestrador mantém o tracking do que foi feito.

## 3) Como é usado (como escrever / o que incluir no prompt e no comportamento)

**Workflow Specification Prompt:**
- Define comandos específicos para execução
- Tem templates claros do que deve ser gerado
- Segue step-by-step mas pensa em workflow completo

**Role Specification (Orquestrador):**
- Papel extremamente específico com responsabilidades claras
- Framework operacional (como trabalhar)
- Decision making (princípios para tomar decisões)
- Communication standards (padronização de comunicação)

**Aplicação:**
- Comando executa o workflow
- Orquestrador mantém tracking do progresso
- Agentes especialistas fazem tarefas específicas

## 4) Onde pode ser usado (casos de uso)

- Sistemas multi-agentes
- Workflows complexos de análise
- Coordenação de múltiplas tarefas
- Geração de relatórios consolidados

## 5) Limitações / quando evitar

Depende de ferramentas que suportam múltiplos agentes (como Cloud Code). Em outras ferramentas, pode precisar de adaptação ou frameworks como LangGraph.

## 6) Observações de prática (coisas que dá pra notar quando testa no dia a dia)

O gerenciamento de estado é um desafio grande. O orquestrador ajuda a manter o tracking, mas não garante 100% de confiabilidade (IA é probabilística). É importante ter um arquivo de manifesto para saber onde parou se a execução for interrompida.
