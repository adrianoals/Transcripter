# 4-Arquivo declarativo do Agent e Prompt como Metadados (Resumo)

## 1) O que é

Formato de arquivo usado pelo Cloud Code para definir agentes. Combina metadados (nome, descrição, exemplos de trigger) com o prompt completo do agente.

## 2) Para que serve

Permitir que o Cloud Code identifique quando chamar um agente especialista. Os metadados ajudam a IA a entender quando usar cada agente, e o prompt define o comportamento do agente.

## 3) Como é usado (como escrever / o que incluir no prompt e no comportamento)

**Metadados:**
- Nome do agente
- Descrição do agente
- Exemplos de quando usar (em formato XML com contexto, user, assistant)
- Modelo a ser usado
- Cor de identificação

**Estrutura:**
- Metadados no topo (três tracinhos)
- Prompt completo abaixo (persona, objetivo, inputs, outputs, critérios, etc.)

**Exemplos de trigger:**
- Formatados em XML mostrando contexto, pergunta do usuário e resposta do assistente
- Ajudam a IA a identificar quando chamar o agente

## 4) Onde pode ser usado (casos de uso)

- Cloud Code (formato específico)
- Outras ferramentas que suportam agentes com metadados
- Organização de prompts especializados

## 5) Limitações / quando evitar

Formato específico do Cloud Code. Pode não funcionar diretamente em outras ferramentas, mas a estrutura do prompt pode ser adaptada.

## 6) Observações de prática (coisas que dá pra notar quando testa no dia a dia)

Os exemplos de trigger são cruciais: se o agente não está sendo chamado, adicione mais exemplos similares à sua necessidade. O Cloud Code usa XML para estruturar os exemplos, facilitando o entendimento pela IA. Mesmo com metadados, o prompt completo ainda é necessário.
