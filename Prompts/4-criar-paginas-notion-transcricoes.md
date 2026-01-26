# Criar Páginas no Notion para Transcrições Revisadas

## Objetivo
Criar páginas no Notion para cada arquivo de transcrição da pasta `transcricoes/`, usando o conteúdo completo de cada arquivo e nomeando as páginas com o nome do arquivo sem extensão (já normalizado).

## Quando executar
Quando o usuário solicitar a criação de páginas no Notion para os arquivos de transcrição revisados da pasta `transcricoes/`.

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

**Passo 2: Preparar nome da página**
- Extrair o nome do arquivo sem a extensão `.md`
- Se o nome **já** terminar com " (Transcrição revisada)", manter como está
- Caso contrário, adicionar " (Transcrição revisada)" ao final do nome
- Exemplo: `1-Estruturação de Prompts.md` → `1-Estruturação de Prompts (Transcrição revisada)`
- Exemplo: `1-Estruturação de Prompts (Transcrição revisada).md` → `1-Estruturação de Prompts (Transcrição revisada)`

**Passo 3: Criar página no Notion**
- Usar a API do Notion para criar uma nova página
- Título da página: nome preparado no Passo 2
- Conteúdo da página: conteúdo completo do arquivo `.md` (texto puro)
- Salvar exatamente como está no arquivo, sem modificações

**Passo 4: Feedback**
- Mostrar status: ✅ Sucesso ou ❌ Erro
- Se houver erro, mostrar mensagem de erro mas continuar com próximo arquivo

### 3. Relatório final
Ao final do processamento, exibir:
- Total de arquivos processados
- Total de páginas criadas com sucesso
- Total de erros (se houver)
- Lista de arquivos que falharam (se houver)
- Links ou IDs das páginas criadas (se disponível)

## Regras importantes

### Sobre o nome das páginas
- **Formato obrigatório**: `{nome_arquivo_sem_extensão_normalizado}`
- Remover apenas a extensão `.md` do nome do arquivo
- Se já terminar com " (Transcrição revisada)", não duplicar o sufixo
- Manter todo o resto do nome original (incluindo números, hífens, espaços, caracteres especiais)
- Exemplos:
  - `1-Estruturação de Prompts.md` → `1-Estruturação de Prompts (Transcrição revisada)`
  - `2-Uma simples correção de Bug.md` → `2-Uma simples correção de Bug (Transcrição revisada)`
  - `8-Exemplo estruturado de prompts.md` → `8-Exemplo estruturado de prompts (Transcrição revisada)`
  - `1-Estruturação de Prompts (Transcrição revisada).md` → `1-Estruturação de Prompts (Transcrição revisada)`

### Sobre o conteúdo
- **NÃO modificar o conteúdo** do arquivo
- Salvar exatamente como está no arquivo `.md`
- Manter toda a formatação, parágrafos e estrutura original
- O conteúdo deve ser inserido como texto na página do Notion

### Sobre tratamento de erros
- Se um arquivo falhar, registrar erro mas continuar com os próximos
- Não interromper o processamento por causa de um arquivo
- Ao final, informar quais arquivos falharam e por quê

### Sobre a API do Notion
- Usar as ferramentas MCP do Notion disponíveis
- Verificar se há autenticação/configuração necessária
- Se não houver parent especificado, criar como páginas standalone (workspace-level)

## Formato de entrada esperado
Lista de arquivos da pasta `transcricoes/`:
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
✅ Página criada: "1-Estruturação de Prompts (Transcrição revisada)"

Processando: 2-Uma simples correção de Bug.md
✅ Página criada: "2-Uma simples correção de Bug (Transcrição revisada)"

...

--- Relatório Final ---
Total processado: 9
Sucessos: 9
Erros: 0
```

## Observações
- Este prompt assume que as transcrições já foram limpas/revisadas anteriormente
- As páginas serão criadas no workspace do Notion do usuário
- Se necessário especificar um parent (página pai ou database), o usuário deve informar
