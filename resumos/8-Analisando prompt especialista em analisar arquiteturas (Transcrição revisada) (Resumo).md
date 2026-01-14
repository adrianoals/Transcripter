# 8-Analisando prompt especialista em analisar arquiteturas (Resumo)

## 1) O que é

Prompt estruturado para criar um agente especialista em análise arquitetural de aplicações. Foca em visão de alto nível sem precisar ler 100% do codebase.

## 2) Para que serve

Fazer análise arquitetural completa: mapear estrutura, componentes, dependências, padrões, riscos, dívidas técnicas. Gera relatório estruturado sem modificar código.

## 3) Como é usado (como escrever / o que incluir no prompt e no comportamento)

**Persona e Escopo:**
- Arquiteto de software com expertise em análise de código
- Papel estritamente analítico: não modifica, não refatora, não altera codebase

**Objetivo:**
- Mapear arquitetura e componentes
- Entender relações entre componentes
- Identificar componentes críticos e principais módulos
- Análise de acoplamento (aferente e eferente)
- Compreender documentações e pontos de integração
- Verificar riscos arquiteturais e pontos únicos de falha
- Identificar dívidas técnicas
- Análise de segurança em nível arquitetural

**Inputs:**
- Código fonte de todos os diretórios
- Dockerfile, Docker Compose, Kubernetes
- Arquivos de variáveis de ambiente
- Makefiles, gerenciamento de pacotes
- Esquemas de bancos de dados, migrações
- Instruções opcionais do usuário

**Output:**
- Markdown report com: executive summary, system overview, critical component analysis, dependency mapping, technology stack, security critical points, infrastructure (se houver arquivos), salvar como "architecture-report-{timestamp}.md"

**Critérios:**
- Passar por todos os diretórios para entender estrutura
- Focar no que é significativo para arquitetura
- Calcular métricas críticas (aferente/eferente)
- Mapear fluxo de dados
- Identificar infraestrutura
- Verificar limites de componentes e integrações
- Analisar escalabilidade e bottlenecks
- Identificar antipatterns e dívidas técnicas
- Priorizar componentes por importância no negócio
- Sempre usar caminho relativo

**Instruções Negativas:**
- Nunca modificar arquivos
- Não trazer sugestões
- Não criar diagramas
- Não assumir padrões sem evidência
- Não incluir tempo estimado
- Não usar emojis
- Não fabricar informações

## 4) Onde pode ser usado (casos de uso)

- Análise de projetos grandes
- Documentação de arquitetura
- Identificação de problemas arquiteturais
- Análise antes de refatoração
- Onboarding de novos desenvolvedores

## 5) Limitações / quando evitar

Depende do tamanho do projeto e da context window disponível. Para projetos muito grandes, pode precisar de múltiplas execuções ou análise por partes.

## 6) Observações de prática (coisas que dá pra notar quando testa no dia a dia)

Não precisa ler 100% do codebase para entender arquitetura. Objetivos claros ajudam a IA a escolher a melhor estratégia de leitura. O workflow no final ajuda a IA a seguir o passo a passo. Quanto mais detalhado o output esperado, melhor o resultado.
