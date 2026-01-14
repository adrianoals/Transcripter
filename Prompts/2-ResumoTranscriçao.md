# Criar Resumo de Transcrições

## Objetivo
Criar resumos dos arquivos de transcrição da pasta `transcricoes/` como se fosse EU anotando no caderno, salvando os resumos na pasta `resumos/`.

## Quando executar
Quando o usuário solicitar a criação de resumos para os arquivos de transcrição da pasta `transcricoes/`.

## Processo de execução

### 1. Identificar arquivos
- Listar todos os arquivos `.md` na pasta `transcricoes/`
- Verificar se os arquivos existem e são legíveis
- Mostrar quantos arquivos serão processados

### 2. Processamento sequencial (um arquivo por vez)
Para cada arquivo `.md` na pasta `transcricoes/`:

**Passo 1: Ler conteúdo**
- Ler o conteúdo completo do arquivo `.md` da pasta `transcricoes/`
- Verificar se o arquivo não está vazio
- Se estiver vazio, pular e registrar aviso

**Passo 2: Criar resumo**
- Aplicar o prompt de resumo abaixo ao conteúdo lido
- Gerar resumo seguindo a estrutura obrigatória

**Passo 3: Preparar nome do arquivo**
- Extrair o nome do arquivo sem a extensão `.md`
- Adicionar " (Resumo)" ao final do nome
- Exemplo: `1-Estruturação de Prompts.md` → `1-Estruturação de Prompts (Resumo).md`

**Passo 4: Salvar arquivo**
- Criar pasta `resumos/` se não existir
- Salvar o resumo como arquivo `.md` na pasta `resumos/`
- Nome do arquivo: nome preparado no Passo 3
- Salvar com encoding UTF-8

**Passo 5: Feedback**
- Mostrar status: ✅ Sucesso ou ❌ Erro
- Se houver erro, mostrar mensagem de erro mas continuar com próximo arquivo

### 3. Relatório final
Ao final do processamento, exibir:
- Total de arquivos processados
- Total de resumos criados com sucesso
- Total de erros (se houver)
- Lista de arquivos que falharam (se houver)
- Localização dos arquivos salvos (pasta `resumos/`)

## Prompt de Resumo

Quero que você crie um resumo do conteúdo abaixo como se fosse EU anotando no caderno.

**Objetivo:**
- Quem NÃO assistiu a aula precisa conseguir entender o assunto só lendo esse resumo.

**Estilo:**
- Tem que soar como anotação prática (curta, clara, útil).
- Nada de "na aula", "no vídeo", "o professor disse".
- Sem floreio e sem "cara de resumo de aula".
- Explicação didática, fácil de entender, frases curtas.
- Use bullets/tópicos quando fizer sentido (sem textão).

**Estrutura obrigatória (com esses títulos):**
1) O que é
2) Para que serve
3) Como é usado (como escrever / o que incluir no prompt e no comportamento)
4) Onde pode ser usado (casos de uso)
5) Limitações / quando evitar
6) Observações de prática (coisas que dá pra notar quando testa no dia a dia)

**Regras:**
- Não invente nada: use somente o que estiver no texto.
- Se houver exemplos no texto, use eles só para ilustrar as "Observações de prática", mas escreva de um jeito que o leitor entenda sem ter visto o exemplo.
- Se tiver termos importantes, explique em 1 linha (bem simples).

## Regras importantes

### Sobre o nome dos arquivos
- **Formato obrigatório**: `{nome_arquivo_sem_extensão} (Resumo).md`
- Remover apenas a extensão `.md` do nome do arquivo original
- Manter todo o resto do nome original (incluindo números, hífens, espaços, caracteres especiais)
- Adicionar " (Resumo)" antes da extensão `.md`
- Exemplos:
  - `1-Estruturação de Prompts.md` → `resumos/1-Estruturação de Prompts (Resumo).md`
  - `2-Uma simples correção de Bug.md` → `resumos/2-Uma simples correção de Bug (Resumo).md`
  - `8-Exemplo estruturado de prompts.md` → `resumos/8-Exemplo estruturado de prompts (Resumo).md`

### Sobre o salvamento
- Salvar sempre na pasta `resumos/` (criar pasta se não existir)
- Cada resumo = um arquivo `.md` separado
- Salvar com encoding UTF-8

### Sobre tratamento de erros
- Se um arquivo falhar, registrar erro mas continuar com os próximos
- Não interromper o processamento por causa de um arquivo
- Ao final, informar quais arquivos falharam e por quê

## Formato de entrada esperado
Arquivos da pasta `transcricoes/`:
```
transcricoes/
  - 1-Estruturação de Prompts.md
  - 2-Uma simples correção de Bug.md
  - 3-Minha IA produziu um lixo.md
  ...
```

## Exemplo de execução
```
Arquivos para processar: 9

Processando: 1-Estruturação de Prompts.md
✅ Resumo criado: resumos/1-Estruturação de Prompts (Resumo).md

Processando: 2-Uma simples correção de Bug.md
✅ Resumo criado: resumos/2-Uma simples correção de Bug (Resumo).md

...

--- Relatório Final ---
Total processado: 9
Sucessos: 9
Erros: 0
Localização dos arquivos salvos: resumos/
```