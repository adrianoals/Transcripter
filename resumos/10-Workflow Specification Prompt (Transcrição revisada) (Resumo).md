# 10-Workflow Specification Prompt (Resumo)

## 1) O que é

Prompt que define um comando executável para coordenar múltiplos agentes especialistas em um workflow estruturado. Gera um snapshot completo e auditável de um projeto.

## 2) Para que serve

Coordenar agentes especialistas para gerar relatórios consolidados sobre um projeto. O Cloud Code executa o comando e coordena os agentes, enquanto um orquestrador mantém o tracking.

## 3) Como é usado (como escrever / o que incluir no prompt e no comportamento)

**Estrutura:**
- Nome do comando
- Descrição: "produza snapshot completo e auditável coordenando agentes especialistas"
- Definição semântica de agentes (Cloud Code = coordenador, orquestrador = tracking)
- Output template (readme com índice de todos os relatórios)

**Fases do Workflow:**
- Fase 1: Setup (orquestrador cria estrutura, manifesto.md)
- Fase 2: Análises paralelas (auditor de dependências + architecture analyzer)
- Fase 3: Análise de componentes (um agente por componente, em paralelo)
- Fase 4: Síntese (orquestrador finaliza manifesto)
- Fase 5: Geração de readme (Cloud Code valida e cria índice)

**Critical Constraints:**
- Orquestrador não chama subagentes (Cloud Code faz isso)
- Orquestrador só faz setup (fase 1) e síntese (fase 4)
- Cada agente em task separada
- Nunca escrever outputs fora das pastas especificadas
- Nunca dar recomendações ou planos de ação
- Não fabricar CVEs
- UltraThink para evitar duplicação de relatórios

**Parâmetros:**
- `--project-folder`: pasta específica para analisar
- `--output-folder`: pasta de saída
- `--ignore-folders`: pastas a ignorar

## 4) Onde pode ser usado (casos de uso)

- Análise completa de projetos
- Geração de documentação arquitetural
- Modernização de sistemas legados
- Análise antes de grandes refatorações

## 5) Limitações / quando evitar

Depende de ferramentas que suportam múltiplos agentes. IA é probabilística, não garante 100% de confiabilidade. Pode precisar de ajustes conforme o comportamento da IA.

## 6) Observações de prática (coisas que dá pra notar quando testa no dia a dia)

Separar por fases maximiza a chance de sucesso. O UltraThink ajuda a evitar duplicação de relatórios. Às vezes o Cloud Code não segue exatamente o workflow - pode precisar ser mais específico. O orquestrador mantém o tracking, mas se a sessão for interrompida, pode perder progresso se não tiver registrado.
