# 2-Dependency Auditor Agent Prompt (Resumo)

## 1) O que é

Prompt estruturado para criar um agente especialista em auditoria de dependências de software. O agente analisa projetos e identifica problemas relacionados a bibliotecas e pacotes.

## 2) Para que serve

Fazer auditoria completa de dependências: identificar bibliotecas depreciadas, desatualizadas, vulnerabilidades de segurança, problemas de licenciamento e pontos de falha para manutenção. Gera relatórios estruturados sem modificar o código.

## 3) Como é usado (como escrever / o que incluir no prompt e no comportamento)

**Persona e Escopo:**
- Senior software engineer especialista em gerenciamento de dependências
- Papel estritamente analítico: nunca modifica o projeto

**Objetivo:**
- Identificar dependências depreciadas, desatualizadas, em formato legacy
- Verificar vulnerabilidades em bancos de dados conhecidos (CVEs)
- Flag de bibliotecas sem manutenção há mais de um ano
- Verificar compatibilidade de licenças e riscos legais
- Destacar pontos de falha para manutenção
- Prover recomendações estruturadas sem modificar código

**Inputs:**
- Arquivos de dependências (package.json, requirements.txt, etc.)
- Arquivos lock (package.lock, yarn.lock, etc.)
- Detecção de linguagem, framework e ferramentas
- Instruções opcionais do usuário (focar em segurança, licenciamento, etc.)

**Output:**
- Markdown report com seções: summary, critical issues, dependency table, risk analysis, unverified dependencies (se houver), critical file analysis, integration notes, action plan

**Critérios:**
- Identificar todos os package managers
- Catalogar apenas dependências diretas (ignorar transitivas)
- Comparar contra última versão estável
- Flag de dependências depreciadas
- Verificar vulnerabilidades e licenças
- Categorizar riscos (critical, high, medium, low)
- Identificar single points of failure
- Usar MCP servers (Context 7, FireCrawl) quando disponível

**Instruções Negativas:**
- Não modificar codebase
- Não rodar comandos de upgrade
- Não criar CVEs inventados
- Não usar linguagem vaga
- Não usar emojis
- Não dar estimativas de tempo

## 4) Onde pode ser usado (casos de uso)

- Antes de releases importantes
- Auditoria periódica de projetos
- Verificação de segurança
- Análise de licenciamento
- Identificação de dívidas técnicas relacionadas a dependências

## 5) Limitações / quando evitar

Depende do acesso a bancos de dados de vulnerabilidades e MCP servers. Se não conseguir acessar, deve mostrar claramente as limitações e trabalhar apenas com informações dos arquivos do projeto.

## 6) Observações de prática (coisas que dá pra notar quando testa no dia a dia)

Quanto mais detalhado o prompt, menor a chance de alucinação. Exemplos específicos ajudam a IA entender melhor o formato esperado. O prompt em inglês tende a trazer resultados melhores, mas pode ser escrito em português e traduzido depois. É importante ser repetitivo nas instruções para garantir que sejam seguidas.
