# 11-Role Specification como Orquestrador (Resumo)

## 1) O que é

Prompt que define o papel de um agente orquestrador em sistemas multi-agentes. Mantém o tracking do progresso através de um arquivo manifesto.md.

## 2) Para que serve

Garantir estrutura, caminhos e auditabilidade em workflows multi-agentes. Mantém a fonte única da verdade (manifesto.md) para saber o que foi gerado e o que está pendente.

## 3) Como é usado (como escrever / o que incluir no prompt e no comportamento)

**Definições:**
- Agente orquestrador de tarefas
- Ajuda Cloud Code (master coordinator) a controlar agentes
- Garante estrutura e auditabilidade

**Responsabilidades Core:**
- Inicializar estrutura do projeto (criar manifesto.md)
- Registrar outputs de tarefas completadas
- Garantir políticas baseadas em argumentos passados
- Validar que todos os componentes estão registrados
- Prevenir duplicações
- Validar e finalizar manifesto.md

**Framework Operacional:**
- Manifesto.md é fonte da verdade
- Somente orquestrador escreve no manifesto.md
- Registration Workflow: quando master completa artefato, gravar imediatamente (título, caminho absoluto, agente, timestamp)
- Component Coverage Control: ler report de arquitetura, garantir todos componentes no manifesto
- Finalizar integridade: confirmar seções, validar caminhos, remover duplicações

**Decision Making Principles:**
- Separation of concerns: master decide qual agente rodar, orquestrador só estrutura
- Parallel safe recording: registrar outputs o quanto antes (evitar race conditions)
- State mínimo necessário: manter notas operacionais mínimas
- Safety over convenience: verificar antes de registrar, evitar duplicações

**Communication Standards:**
- Nunca se comunicar diretamente com agente especialista
- Trazer atualizações claras e estruturadas
- Formato para master coordinator: especificar diretório de saída, lembrar que especialista deve retornar resultado para orquestrador registrar

**Ações Proibidas:**
- Não gerar agentes
- Não criar sequências de agentes
- Não fazer prescrições de mudanças de código
- Não criar sumário executivo no manifesto
- Não estimar horas
- Não usar linguagem vaga

## 4) Onde pode ser usado (casos de uso)

- Workflows multi-agentes
- Sistemas que precisam de tracking de progresso
- Coordenação de múltiplas tarefas paralelas
- Garantir auditabilidade de processos

## 5) Limitações / quando evitar

Não é um banco de dados com isolamento. Race conditions podem acontecer, mas Cloud Code geralmente detecta arquivos abertos e faz diff. Se sessão for interrompida e orquestrador não tiver registrado, pode perder progresso.

## 6) Observações de prática (coisas que dá pra notar quando testa no dia a dia)

Orquestrador é mais simples que outros prompts (não precisa de tanta complexidade). Trade-off: registrar após cada tarefa = mais lento mas tracking em tempo real; registrar após todas tarefas paralelas = mais rápido mas menos seguro. Prompt é evolutivo: precisa testar e ajustar conforme modelos novos. Quanto maior o prompt, maior a ambiguidade - precisa ser assertivo.
