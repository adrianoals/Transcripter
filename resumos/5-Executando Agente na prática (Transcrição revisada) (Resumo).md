# 5-Executando Agente na prática (Resumo)

## 1) O que é

Prompt de comando que chama um agente especialista. É um prompt que executa outro prompt (agente), evitando que as instruções se misturem.

## 2) Para que serve

Fazer chamada direta para um agente sem que o Cloud Code misture as instruções do comando com as do agente. Garante que o agente seja executado exatamente como especificado.

## 3) Como é usado (como escrever / o que incluir no prompt e no comportamento)

**Estrutura do comando:**
- Nome do comando
- Instrução clara: "Use o dependency auditor agent para rodar a auditoria"
- Variáveis de entrada (ex: `$PROJECT_FOLDER`)
- Instruções condicionais (se não passar pasta, auditar projeto inteiro)

**Pontos importantes:**
- "Siga a especificação do agente" - reforça seguir o prompt do agente
- "UltraThink" - palavra-chave para fazer a IA pensar mais profundamente
- "Do not forget" - reforça pontos importantes
- Copiar instruções negativas do agente para evitar comportamentos indesejados

**Workflow:**
- Fazer UltraThink de cada passo da especificação do agente
- Rodar auditoria estritamente seguindo as instruções
- Após produzir report, perguntar se quer salvar (se não foi especificado)

## 4) Onde pode ser usado (casos de uso)

- Executar agentes especializados via comandos
- Automatizar chamadas de agentes
- Garantir execução correta sem misturar instruções

## 5) Limitações / quando evitar

Específico para ferramentas que suportam comandos (como Cloud Code). Em outras ferramentas, pode precisar de adaptação.

## 6) Observações de prática (coisas que dá pra notar quando testa no dia a dia)

Ser repetitivo nas instruções ajuda a garantir que sejam seguidas. Usar formatação (maiúsculas, negrito, exclamações) ajuda a IA a entender a importância. O UltraThink força a IA a pensar mais profundamente antes de executar. É importante reforçar instruções do agente no comando para evitar que sejam ignoradas.
