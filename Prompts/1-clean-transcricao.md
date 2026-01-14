# Limpar Transcrições da Pasta transcricoes/

## Objetivo
Aplicar limpeza de ortografia, pontuação e formatação em todos os arquivos `.md` da pasta `transcricoes/`, e renomear os arquivos adicionando " (Transcrição revisada)" antes da extensão `.md`.

## Instruções de limpeza
Para cada arquivo, pegue o texto e faça isso:

1. Manter o texto integral, sem resumir nem alterar o conteúdo/ideias; apenas corrigir ortografia, pontuação e formatação (parágrafos, títulos, ênfases).

2. Preservar termos técnicos e exemplos; não adicionar nem remover informações — só limpar o texto para ficar legível.

## Processo de execução

### 1. Identificar arquivos
- Listar todos os arquivos `.md` na pasta `transcricoes/`
- Verificar se os arquivos existem e são legíveis
- Mostrar quantos arquivos serão processados

### 2. Processamento sequencial (um arquivo por vez)
Para cada arquivo `.md` na pasta `transcricoes/`:

**Passo 1: Ler conteúdo**
- Ler o conteúdo completo do arquivo `.md`
- Verificar se o arquivo não está vazio
- Se estiver vazio, pular e registrar aviso

**Passo 2: Limpar texto**
- Aplicar as instruções de limpeza acima diretamente no texto
- Corrigir ortografia, pontuação e formatação
- Manter todo o conteúdo e ideias originais

**Passo 3: Preparar nome do arquivo revisado**
- Extrair o nome do arquivo sem a extensão `.md`
- Adicionar " (Transcrição revisada)" antes da extensão
- Exemplo: `1-Analisando estruturas de prompts.md` → `1-Analisando estruturas de prompts (Transcrição revisada).md`

**Passo 4: Salvar arquivo revisado e remover original**
- Salvar o texto limpo no novo arquivo com o nome preparado no Passo 3
- Salvar na mesma pasta `transcricoes/` com encoding UTF-8
- Deletar o arquivo original após salvar o revisado (renomear, não criar cópia)

**Passo 5: Feedback**
- Mostrar status: ✅ Sucesso ou ❌ Erro
- Se houver erro, mostrar mensagem de erro mas continuar com próximo arquivo

### 3. Relatório final
Ao final do processamento, exibir:
- Total de arquivos processados
- Total de arquivos limpos com sucesso
- Total de erros (se houver)
- Lista de arquivos que falharam (se houver)
- Localização dos arquivos salvos (pasta `transcricoes/`)

## Regras importantes

### Sobre o nome dos arquivos
- **Formato obrigatório**: `{nome_arquivo_original_sem_extensão} (Transcrição revisada).md`
- Remover apenas a extensão `.md` do nome do arquivo original
- Manter todo o resto do nome original (incluindo números, hífens, espaços, caracteres especiais)
- Exemplos:
  - `1-Analisando estruturas de prompts.md` → `1-Analisando estruturas de prompts (Transcrição revisada).md`
  - `2-Dependency Auditor Agent Prompt.md` → `2-Dependency Auditor Agent Prompt (Transcrição revisada).md`

### Sobre o conteúdo
- **NÃO modificar o conteúdo/ideias**: apenas corrigir ortografia, pontuação e formatação
- Preservar termos técnicos e exemplos
- Não adicionar nem remover informações
- Manter parágrafos, títulos e ênfases originais (apenas corrigir formatação)

### Sobre tratamento de erros
- Se um arquivo falhar, registrar erro mas continuar com os próximos
- Não interromper o processamento por causa de um arquivo
- Ao final, informar quais arquivos falharam e por quê

### Sobre o salvamento
- Salvar sempre na pasta `transcricoes/` (mesma pasta dos originais)
- **Deletar o arquivo original após salvar o revisado** (renomear, não criar cópia)
- Cada arquivo limpo = substitui o arquivo original com o novo nome " (Transcrição revisada)"