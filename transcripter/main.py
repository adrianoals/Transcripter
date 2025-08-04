import os, tempfile, uuid
from datetime import datetime
from tinydb import TinyDB
from groq import Groq
import sounddevice as sd
import soundfile as sf
from pytubefix import YouTube
import numpy as np
import subprocess

import questionary
from rich.console import Console
from rich.table import Table

from agno.agent import Agent
from agno.models.openai import OpenAIChat

from dotenv import load_dotenv
load_dotenv()

# Usar caminho absoluto para o banco de dados
import os
db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "transcricoes.json")
db = TinyDB(db_path)
client = Groq()
console = Console()

# Preços das APIs (em USD)
GROQ_WHISPER_PRICE_PER_MINUTE = 0.006  # $0.006 por minuto
OPENAI_GPT4_INPUT_PRICE_PER_1K = 0.03   # $0.03 por 1K tokens entrada
OPENAI_GPT4_OUTPUT_PRICE_PER_1K = 0.06  # $0.06 por 1K tokens saída

def calcular_custo_transcricao(duracao_minutos):
    """Calcula o custo da transcrição baseado na duração"""
    return duracao_minutos * GROQ_WHISPER_PRICE_PER_MINUTE

def calcular_custo_analise_ia(tokens_entrada, tokens_saida):
    """Calcula o custo da análise com IA baseado nos tokens"""
    custo_entrada = (tokens_entrada / 1000) * OPENAI_GPT4_INPUT_PRICE_PER_1K
    custo_saida = (tokens_saida / 1000) * OPENAI_GPT4_OUTPUT_PRICE_PER_1K
    return custo_entrada + custo_saida

def obter_duracao_audio(audio_path):
    """Obtém a duração do arquivo de áudio em minutos"""
    try:
        cmd = [
            'ffprobe', '-v', 'quiet', '-show_entries', 'format=duration',
            '-of', 'csv=p=0', audio_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        duracao_segundos = float(result.stdout.strip())
        return duracao_segundos / 60  # Converter para minutos
    except:
        return None

def selecionar_arquivo_video():
    """Seleciona um arquivo de vídeo usando interface gráfica"""
    try:
        import tkinter as tk
        from tkinter import filedialog
        
        root = tk.Tk()
        root.withdraw()  # Esconde a janela principal
        
        arquivo = filedialog.askopenfilename(
            title="Selecione um arquivo de vídeo",
            filetypes=[
                ("Vídeos", "*.mp4 *.avi *.mov *.mkv *.wmv *.flv *.webm"),
                ("Todos os arquivos", "*.*")
            ]
        )
        root.destroy()
        return arquivo if arquivo else None
    except ImportError:
        # Fallback para sistemas sem tkinter
        console.print("[yellow]Interface gráfica não disponível. Digite o caminho do arquivo:[/yellow]")
        arquivo = questionary.text("Caminho do arquivo de vídeo:").ask()
        # Limpar aspas se houver
        if arquivo:
            arquivo = arquivo.strip().strip("'\"")
        return arquivo

def extrair_audio_video(arquivo_video):
    """Extrai áudio de um arquivo de vídeo usando ffmpeg"""
    try:
        audio_temp = tempfile.mktemp(suffix=".mp3")
        
        cmd = [
            'ffmpeg', '-i', arquivo_video, 
            '-vn', '-acodec', 'mp3', 
            '-ar', '16000', '-ac', '1', 
            '-b:a', '64k', '-y', audio_temp
        ]
        
        console.print(f"[blue]Extraindo áudio de: {os.path.basename(arquivo_video)}[/blue]")
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        if os.path.exists(audio_temp) and os.path.getsize(audio_temp) > 0:
            # Verificar tamanho do arquivo
            size_mb = os.path.getsize(audio_temp) / (1024 * 1024)
            console.print(f"[blue]Tamanho do áudio: {size_mb:.1f} MB[/blue]")
            
            # Se for muito grande, comprimir mais
            if size_mb > 20:  # Limite da API Groq é ~25MB
                console.print("[yellow]Arquivo muito grande, comprimindo...[/yellow]")
                audio_compressed = tempfile.mktemp(suffix=".mp3")
                cmd_compress = [
                    'ffmpeg', '-i', audio_temp,
                    '-acodec', 'mp3', '-ar', '8000', '-ac', '1',
                    '-b:a', '32k', '-y', audio_compressed
                ]
                subprocess.run(cmd_compress, check=True, capture_output=True, text=True)
                os.remove(audio_temp)
                audio_temp = audio_compressed
                
                size_mb = os.path.getsize(audio_temp) / (1024 * 1024)
                console.print(f"[blue]Tamanho após compressão: {size_mb:.1f} MB[/blue]")
            
            return audio_temp
        else:
            console.print("[red]Erro: Não foi possível extrair áudio do vídeo.[/red]")
            return None
            
    except subprocess.CalledProcessError as e:
        console.print(f"[red]Erro ao extrair áudio: {e.stderr}[/red]")
        return None
    except Exception as e:
        console.print(f"[red]Erro inesperado: {e}[/red]")
        return None


def baixar_youtube(url):
    yt = YouTube(url)
    f = f"{uuid.uuid4()}.wav"
    yt.streams.filter(only_audio=True).first().download(filename=f)
    return f, yt.title

def gravar_audio(msg):
    print(msg)
    grava = []
    try:
        with sd.InputStream(samplerate=48000, channels=1) as s:
            while True: 
                grava.append(s.read(1024)[0])
    except KeyboardInterrupt:
        print("\nGravação interrompida.")

    f = tempfile.mktemp(suffix=".wav")
    if grava: 
        sf.write(f, np.vstack(grava), 48000)
    return f

def gravar_tela():
    print("Gravando áudio do sistema (BlackHole)... pressione Ctrl+C para pausar.")
    import subprocess, time
    audio = tempfile.mktemp(suffix=".wav")
    cmd = [
        'ffmpeg', '-f', 'avfoundation', '-i', ':1', '-ac', '1', '-ar', '48000', '-y', audio
    ]
    proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        proc.wait()
    except KeyboardInterrupt:
        print("\nGravação interrompida pelo usuário.")
        proc.terminate()
        proc.wait()
    try:
        time.sleep(0.2)
    except KeyboardInterrupt:
        pass
    return audio

def transcrever(audio_path):
    print("Enviando áudio para transcrição, aguarde...")
    try:
        # Verificar tamanho do arquivo
        file_size = os.path.getsize(audio_path)
        size_mb = file_size / (1024 * 1024)
        console.print(f"[blue]Enviando arquivo de {size_mb:.1f} MB para transcrição...[/blue]")
        
        # Obter duração do áudio
        duracao_minutos = obter_duracao_audio(audio_path)
        if duracao_minutos:
            custo_estimado = calcular_custo_transcricao(duracao_minutos)
            console.print(f"[yellow]Duração: {duracao_minutos:.1f} minutos | Custo estimado: ${custo_estimado:.4f}[/yellow]")
        
        with open(audio_path, "rb") as file:
            transcription = client.audio.transcriptions.create(
                file=(audio_path, file.read()),
                model="whisper-large-v3-turbo",
                response_format="verbose_json",
                timestamp_granularities=["word"],
            )
            texto = transcription.text
            
            # Mostrar custo final
            if duracao_minutos:
                custo_final = calcular_custo_transcricao(duracao_minutos)
                console.print(f"[green]✅ Transcrição concluída! Custo: ${custo_final:.4f}[/green]")
            
            print("\n[Transcrição]")
            console.rule("Transcrição")
            console.print(texto)
            input("\nPressione ENTER para continuar...")
            return texto
    except KeyboardInterrupt:
        print("\nTranscrição interrompida pelo usuário.")
        return ""
    except Exception as e:
        if "request_too_large" in str(e):
            console.print("[red]Arquivo muito grande para a API. Tentando comprimir mais...[/red]")
            # Tentar comprimir ainda mais
            try:
                audio_compressed = tempfile.mktemp(suffix=".mp3")
                cmd_compress = [
                    'ffmpeg', '-i', audio_path,
                    '-acodec', 'mp3', '-ar', '8000', '-ac', '1',
                    '-b:a', '16k', '-y', audio_compressed
                ]
                subprocess.run(cmd_compress, check=True, capture_output=True, text=True)
                
                if os.path.exists(audio_compressed):
                    size_mb = os.path.getsize(audio_compressed) / (1024 * 1024)
                    console.print(f"[blue]Tentando novamente com arquivo de {size_mb:.1f} MB...[/blue]")
                    
                    with open(audio_compressed, "rb") as file:
                        transcription = client.audio.transcriptions.create(
                            file=(audio_compressed, file.read()),
                            model="whisper-large-v3-turbo",
                            response_format="verbose_json",
                            timestamp_granularities=["word"],
                        )
                        texto = transcription.text
                        print("\n[Transcrição]")
                        console.rule("Transcrição")
                        console.print(texto)
                        input("\nPressione ENTER para continuar...")
                        os.remove(audio_compressed)
                        return texto
            except Exception as e2:
                console.print(f"[red]Erro na segunda tentativa: {e2}[/red]")
                return ""
        else:
            console.print(f"[red]Erro na transcrição: {e}[/red]")
            return ""

def salvar_transcricao(origem, titulo, texto):
    db.insert({
        "origem": origem,
        "titulo": titulo,
        "texto": texto,
        "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

def ver_historico():
    table = Table(title="Histórico de Transcrições")
    table.add_column("Nº", style="bold yellow")
    table.add_column("Data", style="cyan")
    table.add_column("Origem", style="magenta")
    table.add_column("Título/Nome", style="green")
    table.add_column("Trecho", style="white")
    transcricoes = db.all()
    
    for i, item in enumerate(transcricoes):
        trecho = (item["texto"][:40] + "...") if len(item["texto"]) > 40 else item["texto"]
        table.add_row(str(i+1), item.get("data", ""), item.get("origem", ""), item.get("titulo", ""), trecho)
    console.print(table)

    if transcricoes:
        idx = questionary.text("Digite o número da transcrição para ver completa (ou ENTER para sair):").ask()
        if idx and idx.isdigit() and 1 <= int(idx) <= len(transcricoes):
            item = transcricoes[int(idx)-1]
            console.rule(item.get("titulo", ""))
            console.print(item["texto"])

def chat_ia(transcricao):
    console.clear()
    console.print("""[bold green]Iniciando análise com IA. 
                  Digite sua pergunta sobre a transcrição. 
                  Digite 'sair' para encerrar a conversa.[/bold green]""")
    console.rule("Transcrição Selecionada")
    console.print(transcricao)

    memory_agent = Agent(
        model=OpenAIChat(id="gpt-4.1"),
        add_history_to_messages=True,
        num_history_runs=3,
        markdown=True,
        instructions=f"""
        Você é um assistente de análise de transcrições de vídeos.
        O usuário lhe fornecerá uma transcrição de um vídeo/áudio e você deve analisá-la e
        responder as perguntas do usuário.

        Transcrição: 
        {transcricao}
        """
    )

    # Contadores de custo
    total_custo = 0
    num_perguntas = 0

    while True:
        pergunta = questionary.text("Você:").ask()
        
        if not pergunta:
            continue
        
        if pergunta.strip().lower() == "sair":
            console.print(f"\n[bold red]Conversa encerrada. Total: {num_perguntas} perguntas | Custo total: ${total_custo:.4f}[/bold red]")
            input("Pressione ENTER para voltar.")
            break
        
        # Estimativa de tokens (aproximada)
        tokens_entrada = len(transcricao + pergunta) // 4  # ~4 chars por token
        tokens_saida_estimado = 200  # Estimativa conservadora
        
        custo_estimado = calcular_custo_analise_ia(tokens_entrada, tokens_saida_estimado)
        console.print(f"[yellow]Custo estimado desta pergunta: ${custo_estimado:.4f}[/yellow]")
        
        response = memory_agent.run(pergunta, stream=True)
        resposta_completa = ""
        for msg in response:
            print(msg.content, end="", flush=True)
            resposta_completa += msg.content
        
        print("\n")
        
        # Calcular custo real (aproximado)
        tokens_saida_real = len(resposta_completa) // 4
        custo_real = calcular_custo_analise_ia(tokens_entrada, tokens_saida_real)
        total_custo += custo_real
        num_perguntas += 1
        
        console.print(f"[green]✅ Resposta gerada! Custo: ${custo_real:.4f} | Total: ${total_custo:.4f}[/green]")
        # console.print(f"[bold blue]IA:[/bold blue] {resposta.content if hasattr(resposta, 'content') else resposta}")

def analise_transcricoes():
    while True:
        console.clear()
        transcricoes = db.all()
        if not transcricoes:
            console.print("[yellow]Nenhuma transcrição encontrada.[/yellow]")
            input("Pressione ENTER para voltar.")
            return
        # Mostra tabela
        table = Table(title="Histórico de Transcrições")
        table.add_column("Nº", style="bold yellow")
        table.add_column("Data", style="cyan")
        table.add_column("Origem", style="magenta")
        table.add_column("Título/Nome", style="green")
        table.add_column("Trecho", style="white")
        for i, item in enumerate(transcricoes):
            trecho = (item["texto"][:40] + "...") if len(item["texto"]) > 40 else item["texto"]
            table.add_row(str(i+1), item.get("data", ""), item.get("origem", ""), item.get("titulo", ""), trecho)
        console.print(table)
        acao = questionary.select(
            "O que deseja fazer?",
            choices=[
                "1. Análise com IA",
                "2. Acessar transcrição",
                "3. Deletar transcrição",
                "4. Voltar"
            ]).ask()
        if acao.startswith("4."):
            break
        idx = questionary.text("Digite o número da transcrição:").ask()
        if not idx or not idx.isdigit() or not (1 <= int(idx) <= len(transcricoes)):
            console.print("[red]Número inválido![/red]")
            continue
        item = transcricoes[int(idx)-1]
        if acao.startswith("1."):
            chat_ia(item["texto"])
        elif acao.startswith("2."):
            console.clear()
            console.rule(item.get("titulo", ""))
            console.print(item["texto"])
            input("Pressione ENTER para voltar.")
        elif acao.startswith("3."):
            db.remove(doc_ids=[item.doc_id])
            console.print("[red]Transcrição deletada![/red]")
            input("Pressione ENTER para voltar.")

def mostrar_estatisticas_custo():
    """Mostra estatísticas de custo das APIs"""
    console.clear()
    console.rule("📊 Estatísticas de Custo")
    
    # Tabela de preços
    table = Table(title="Preços das APIs")
    table.add_column("Serviço", style="bold cyan")
    table.add_column("Modelo", style="green")
    table.add_column("Preço", style="yellow")
    table.add_column("Exemplo", style="white")
    
    table.add_row(
        "Transcrição", 
        "Whisper Large v3 Turbo", 
        "$0.006/min", 
        "10 min = $0.06"
    )
    table.add_row(
        "Análise IA", 
        "GPT-4.1", 
        "$0.03/1K tokens", 
        "1 pergunta = ~$0.03"
    )
    
    console.print(table)
    
    # Dicas de economia
    console.print("\n[bold green]💡 Dicas para economizar:[/bold green]")
    console.print("• Use áudio comprimido (já implementado)")
    console.print("• Faça perguntas específicas na análise")
    console.print("• Monitore seus gastos regularmente")
    console.print("• Configure alertas nas dashboards das APIs")
    
    input("\nPressione ENTER para voltar.")

def consolidar_bancos_dados():
    """Consolida os dois bancos de dados se existirem"""
    import os
    from tinydb import TinyDB
    
    # Caminhos dos bancos
    db_raiz = os.path.join(os.path.dirname(os.path.dirname(__file__)), "transcricoes.json")
    db_transcripter = os.path.join(os.path.dirname(__file__), "transcricoes.json")
    
    # Verificar se ambos existem
    if os.path.exists(db_raiz) and os.path.exists(db_transcripter):
        console.print("[yellow]Encontrados dois bancos de dados. Consolidando...[/yellow]")
        
        # Ler dados de ambos
        db1 = TinyDB(db_raiz)
        db2 = TinyDB(db_transcripter)
        
        dados1 = db1.all()
        dados2 = db2.all()
        
        # Combinar dados únicos
        todos_dados = dados1 + dados2
        
        # Remover duplicatas baseado em título e data
        dados_unicos = []
        titulos_vistos = set()
        
        for item in todos_dados:
            chave = f"{item.get('titulo', '')}_{item.get('data', '')}"
            if chave not in titulos_vistos:
                dados_unicos.append(item)
                titulos_vistos.add(chave)
        
        # Salvar no banco principal
        db1.truncate()  # Limpar
        for item in dados_unicos:
            db1.insert(item)
        
        # Remover o banco duplicado
        os.remove(db_transcripter)
        
        console.print(f"[green]✅ Consolidados {len(dados_unicos)} registros únicos![/green]")
        return True
    
    return False


def main():
    # Consolidar bancos de dados no início
    consolidar_bancos_dados()
    
    while True:
        console.clear()
        escolha = questionary.select(
            "O que deseja fazer?",
            choices=[
                "1. Nova gravação",
                "2. Análise de transcrições",
                "3. Estatísticas de Custo",
                "4. Consolidar Dados",
                "5. Sair"
            ]).ask()
        
        if escolha.startswith("1."):
            console.clear()
            fonte = questionary.select(
                "Escolha a fonte do áudio:",
                choices=["1. YouTube", "2. Microfone", "3. Tela", "4. Arquivo local", "5. Voltar"]).ask()
            
            if fonte.startswith("1."):
                url = questionary.text("URL do vídeo:").ask()
                audio, titulo = baixar_youtube(url)
                texto = transcrever(audio)
                salvar_transcricao("youtube", titulo, texto)
                os.remove(audio)

            elif fonte.startswith("2."):
                audio = gravar_audio("Gravando... Ctrl+C para pausar.")
                texto = transcrever(audio)
                nome = texto[:50] + "..." if len(texto) > 50 else texto
                salvar_transcricao("microfone", nome, texto)
                os.remove(audio)

            elif fonte.startswith("3."):
                audio = gravar_tela()
                texto = transcrever(audio)
                nome = texto[:50] + "..." if len(texto) > 50 else texto
                salvar_transcricao("tela", nome, texto)
                os.remove(audio)

            elif fonte.startswith("4."):
                arquivo = selecionar_arquivo_video()
                # Debug: mostrar o que foi recebido
                console.print(f"[blue]Caminho recebido: '{arquivo}'[/blue]")
                if arquivo and os.path.exists(arquivo):
                    audio = extrair_audio_video(arquivo)
                    if audio:
                        texto = transcrever(audio)
                        nome = os.path.basename(arquivo)
                        salvar_transcricao("arquivo_local", nome, texto)
                        os.remove(audio)
                    else:
                        console.print("[red]Não foi possível processar o arquivo de vídeo.[/red]")
                        input("Pressione ENTER para continuar...")
                elif arquivo:
                    console.print("[red]Arquivo não encontrado.[/red]")
                    input("Pressione ENTER para continuar...")
                else:
                    console.print("[yellow]Nenhum arquivo selecionado.[/yellow]")
                    input("Pressione ENTER para continuar...")

            else:
                continue

        elif escolha.startswith("2."):
            analise_transcricoes()
        elif escolha.startswith("3."):
            mostrar_estatisticas_custo()
        elif escolha.startswith("4."):
            consolidar_bancos_dados()
            input("Pressione ENTER para continuar...")
        else:
            break


if __name__ == "__main__":
    main()