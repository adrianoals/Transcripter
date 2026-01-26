# Transcrição em Lote de Arquivos de Vídeo

## Objetivo
Processar uma lista de arquivos de vídeo fornecida pelo usuário, transcrever cada um sequencialmente e salvar as transcrições como arquivos `.md` na pasta `transcricoes/`.

## ⚠️ IMPORTANTE: Código já implementado
- A função `processar_lista_arquivos()` já está implementada em `transcripter/main.py`
- **NÃO é necessário criar código novo**, apenas executar a função existente
- Chame diretamente: `processar_lista_arquivos(lista_de_arquivos)`
- O código já faz tudo descrito neste prompt automaticamente

## Quando executar
Quando o usuário fornecer uma lista de caminhos de arquivos de vídeo para transcrição em lote.

## Processo de execução

### 1. Validação inicial
- Verificar se todos os arquivos da lista existem
- Verificar se são arquivos de vídeo válidos (extensões: .mp4, .avi, .mov, .mkv, .wmv, .flv, .webm)
- Mostrar quantos arquivos serão processados
- Exibir lista dos arquivos que serão processados

### 2. Processamento sequencial (um arquivo por vez)
Para cada arquivo na lista:

**Passo 1: Extração de áudio**
- Usar função `extrair_audio_video(arquivo_video)` existente
- Extrair áudio para arquivo temporário
- Verificar se extração foi bem-sucedida
- Se falhar, registrar erro e continuar com próximo arquivo

**Passo 2: Transcrição**
- Usar função `transcrever(audio_path)` existente
- Obter texto transcrito do modelo (Groq/Whisper)
- Verificar se transcrição foi bem-sucedida
- Se falhar, registrar erro e continuar com próximo arquivo

**Passo 3: Salvamento no banco de dados**
- Usar função `salvar_transcricao(origem, titulo, texto)` existente
- Origem: "arquivo_local"
- Título: nome do arquivo original (ex: "video.mp4")
- Texto: transcrição completa exatamente como retornada pelo modelo

**Passo 4: Salvamento como arquivo .md**
- Criar arquivo `.md` na pasta `transcricoes/`
- Nome do arquivo: nome do arquivo original sem extensão + extensão `.md` (ex: "video.mp4" → "video.md")
- Conteúdo: transcrição completa exatamente como retornada pelo modelo (sem modificações)
- Salvar com encoding UTF-8

**Passo 5: Limpeza**
- Remover arquivo temporário de áudio
- Continuar para próximo arquivo

### 3. Feedback durante processamento
- Mostrar progresso: "Processando arquivo X de Y: nome_arquivo"
- Mostrar duração e custo estimado de cada transcrição
- Mostrar status: ✅ Sucesso ou ❌ Erro
- Se houver erro, mostrar mensagem de erro mas continuar processamento

### 4. Relatório final
Ao final do processamento, exibir:
- Total de arquivos processados
- Total de transcrições bem-sucedidas
- Total de erros (se houver)
- Lista de arquivos que falharam (se houver)
- Custo total estimado
- Localização dos arquivos salvos (pasta `transcricoes/`)

## Regras importantes

### Sobre a transcrição
- **NÃO modificar o texto** retornado pelo modelo
- Salvar exatamente como vem da API (texto puro, sem formatação adicional)
- Manter toda a pontuação, espaçamento e estrutura original
- Não adicionar cabeçalhos, títulos ou metadados no arquivo .md

### Sobre tratamento de erros
- Se um arquivo falhar, registrar erro mas continuar com os próximos
- Não interromper o processamento por causa de um arquivo
- Ao final, informar quais arquivos falharam e por quê

### Sobre o nome dos arquivos
- Usar o nome original do arquivo de vídeo sem extensão + extensão `.md`
- Exemplo: `video-aula.mp4` → `transcricoes/video-aula.md`
- Se houver caracteres especiais no nome, manter como está

### Sobre o salvamento
- Salvar sempre na pasta `transcricoes/` (criar pasta se não existir)
- Manter salvamento no JSON (`transcricoes.json`) também (compatibilidade)
- Cada transcrição = um arquivo .md separado

## Formato de entrada esperado
Lista de caminhos absolutos ou relativos para arquivos de vídeo:
```
[
  "/caminho/para/video1.mp4",
  "/caminho/para/video2.avi",
  "video3.mov"
]
```

## Exemplo de execução
```
Arquivos para processar: 3
1. video-aula-1.mp4
2. video-aula-2.mp4
3. video-aula-3.mp4

Processando arquivo 1 de 3: video-aula-1.mp4
✅ Transcrição concluída! Custo: $0.0123
Salvo em: transcricoes/video-aula-1.md

Processando arquivo 2 de 3: video-aula-2.mp4
✅ Transcrição concluída! Custo: $0.0156
Salvo em: transcricoes/video-aula-2.md

Processando arquivo 3 de 3: video-aula-3.mp4
✅ Transcrição concluída! Custo: $0.0098
Salvo em: transcricoes/video-aula-3.md

--- Relatório Final ---
Total processado: 3
Sucessos: 3
Erros: 0
Custo total: $0.0377
```
