# Listar Arquivos de uma Pasta e Salvar Caminhos

## Objetivo
Listar todos os arquivos de uma pasta fornecida pelo usuário e escrever o caminho completo de cada arquivo em um arquivo de texto (por padrão `file.txt`), um caminho por linha, com aspas simples.

## Quando executar
Quando o usuário fornecer um caminho de pasta e solicitar que os caminhos dos arquivos sejam salvos em um arquivo.

## Processo de execução

### 1. Validação inicial
- Verificar se o caminho da pasta fornecido existe
- Verificar se é realmente uma pasta (não um arquivo)
- Mostrar quantos arquivos foram encontrados

### 2. Listar arquivos
- Listar todos os arquivos da pasta (não incluir subpastas)
- Ordenar os arquivos por nome (ordem alfabética)
- Mostrar lista dos arquivos encontrados

### 3. Preparar caminhos
- Para cada arquivo, criar caminho completo: `{caminho_da_pasta}/{nome_arquivo}`
- Formatar cada caminho com aspas simples: `'{caminho_completo}'`
- Um caminho por linha

### 4. Salvar no arquivo
- Salvar todos os caminhos no arquivo especificado (ou `file.txt` por padrão)
- Sobrescrever o arquivo se já existir
- Salvar com encoding UTF-8
- Cada caminho em uma linha separada

### 5. Feedback
- Mostrar quantos arquivos foram listados
- Mostrar onde os caminhos foram salvos
- Mostrar nome do arquivo de saída

## Regras importantes

### Sobre o formato dos caminhos
- **Formato obrigatório**: `'{caminho_completo_do_arquivo}'`
- Usar aspas simples ao redor de cada caminho
- Um caminho por linha
- Caminho completo desde a raiz (absoluto)
- Exemplo:
  ```
  '/Users/adriano/Desktop/pasta/arquivo1.mp4'
  '/Users/adriano/Desktop/pasta/arquivo2.mp4'
  ```

### Sobre o arquivo de saída
- Por padrão, salvar em `file.txt` na raiz do projeto
- Se o usuário especificar outro arquivo, usar o especificado
- Sobrescrever conteúdo anterior se o arquivo já existir
- Salvar com encoding UTF-8

### Sobre o que listar
- Listar apenas arquivos (não subpastas)
- Incluir todos os tipos de arquivo (sem filtro de extensão)
- Ordenar alfabeticamente por nome
- Não incluir arquivos ocultos (que começam com ponto) a menos que especificado

### Sobre tratamento de erros
- Se a pasta não existir, informar erro e não criar arquivo
- Se a pasta estiver vazia, criar arquivo vazio ou informar
- Se não tiver permissão de leitura, informar erro

## Formato de entrada esperado
Caminho de uma pasta:
```
'/Users/adriano/Desktop/pasta/Vídeo Aulas'
```

## Exemplo de execução
```
Pasta fornecida: /Users/adriano/Desktop/pasta/Vídeo Aulas
Arquivos encontrados: 11

Listando arquivos:
1. 1-Analisando estruturas de prompts.mp4
2. 2-Dependency Auditor Agent Prompt.mp4
3. 3-Resultado gerado pelo prompt.mp4
...

✅ Caminhos salvos em: file.txt
Total de arquivos: 11
```

## Exemplo de saída no arquivo
```
'/Users/adriano/Desktop/pasta/Vídeo Aulas/1-Analisando estruturas de prompts.mp4'
'/Users/adriano/Desktop/pasta/Vídeo Aulas/2-Dependency Auditor Agent Prompt.mp4'
'/Users/adriano/Desktop/pasta/Vídeo Aulas/3-Resultado gerado pelo prompt.mp4'
...
```

## Observações
- Este prompt lista apenas arquivos na pasta raiz, não recursivamente em subpastas
- Se precisar listar recursivamente, o usuário deve especificar
- O formato com aspas simples facilita uso em scripts Python
- Arquivos são ordenados alfabeticamente para facilitar leitura
