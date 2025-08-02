# Funcionalidade de Vídeos Locais

## Nova funcionalidade implementada!

O Transcripter agora suporta transcrição de vídeos locais da sua máquina.

## Como usar

1. Execute o Transcripter:
   ```bash
   source .venv/bin/activate
   python transcripter/main.py
   ```

2. Selecione "1. Nova gravação"

3. Escolha "4. Arquivo local"

4. Uma janela de seleção de arquivos será aberta (ou você pode digitar o caminho manualmente)

5. Selecione qualquer arquivo de vídeo da sua máquina

6. O sistema irá:
   - Extrair o áudio do vídeo usando ffmpeg
   - Transcrever o áudio usando Groq/Whisper
   - Salvar a transcrição no histórico
   - Limpar arquivos temporários automaticamente

## Formatos suportados

- **MP4** - Formato mais comum
- **AVI** - Formato clássico
- **MOV** - Formato Apple
- **MKV** - Formato Matroska
- **WMV** - Formato Windows
- **FLV** - Flash Video
- **WebM** - Formato web

*Qualquer formato que o ffmpeg consiga processar será aceito.*

## Funcionalidades implementadas

### 1. Seleção de arquivos
- Interface gráfica usando tkinter
- Fallback para entrada manual se tkinter não estiver disponível
- Filtros para arquivos de vídeo
- Validação de existência do arquivo

### 2. Extração de áudio
- Usa ffmpeg para extrair áudio
- Converte para WAV 48kHz mono
- Tratamento de erros robusto
- Limpeza automática de arquivos temporários

### 3. Integração completa
- Menu atualizado com nova opção
- Fluxo integrado com transcrição existente
- Salvamento no histórico com origem "arquivo_local"
- Tratamento de erros em cada etapa

## Código adicionado

### Funções novas:
- `selecionar_arquivo_video()` - Interface para seleção
- `extrair_audio_video()` - Extração de áudio com ffmpeg

### Menu atualizado:
- Opção "4. Arquivo local" adicionada
- Lógica completa de processamento
- Tratamento de erros

## Dependências

A funcionalidade usa apenas dependências já existentes:
- `tkinter` (vem com Python)
- `subprocess` (biblioteca padrão)
- `ffmpeg` (já necessário para outras funcionalidades)

## Teste

Execute o script de teste:
```bash
source .venv/bin/activate
python test_video_local.py
```

## Próximos passos possíveis

1. **Suporte a legendas** - Extrair e sincronizar legendas
2. **Processamento em lote** - Transcrever múltiplos vídeos
3. **Detecção de idioma** - Identificar idioma automaticamente
4. **Timestamps** - Adicionar timestamps na transcrição
5. **Exportação** - Exportar transcrições em diferentes formatos

---

**Status**: ✅ Implementado e testado
**Compatibilidade**: macOS, Windows, Linux
**Dependências**: Apenas ffmpeg (já necessário) 