# 3-Resultado gerado pelo prompt (Resumo)

## 1) O que é

Exemplo prático de resultado gerado pelo prompt de auditoria de dependências em um codebase real.

## 2) Para que serve

Demonstrar como o prompt funciona na prática e como o relatório é estruturado. Mostra a aplicação real da estrutura de prompt aprendida.

## 3) Como é usado (como escrever / o que incluir no prompt e no comportamento)

O relatório gerado inclui:
- Dependency Audit Report com sumário executivo
- Key findings (vulnerabilidades críticas, dependências com problemas)
- Critical issues (bibliotecas específicas com problemas)
- Lista de dependências com status (atualizadas/desatualizadas)
- Análise de risco
- Dependências não verificadas
- Arquivos críticos afetados
- Integration notes
- Action plan

O relatório pode ser gerado em inglês (melhor resultado) ou português (se especificado no prompt).

## 4) Onde pode ser usado (casos de uso)

- Visualizar estado atual das dependências
- Identificar problemas críticos antes de produção
- Tomar decisões sobre upgrades
- Documentar estado do projeto

## 5) Limitações / quando evitar

Se não houver lockfiles, o risco de reproduzir em produção é maior. Versões misturadas (pinadas e não pinadas) podem causar problemas.

## 6) Observações de prática (coisas que dá pra notar quando testa no dia a dia)

O relatório mostra problemas reais encontrados (vulnerabilidades, dependências depreciadas, falta de lockfiles). É importante salvar o relatório em arquivo para análise posterior e tomada de decisão.
