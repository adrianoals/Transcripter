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

db = TinyDB("transcricoes.json")
client = Groq()
console = Console()

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
        
        with open(audio_path, "rb") as file:
            transcription = client.audio.transcriptions.create(
                file=(audio_path, file.read()),
                model="whisper-large-v3-turbo",
                response_format="verbose_json",
                timestamp_granularities=["word"],
            )
            texto = transcription.text
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

    while True:
        pergunta = questionary.text("Você:").ask()
        
        if not pergunta:
            continue
        
        if pergunta.strip().lower() == "sair":
            console.print("\n[bold red]Conversa encerrada.[/bold red]")
            input("Pressione ENTER para voltar.")
            break
        
        # prompt = f"""\n\nContexto da transcrição:\n" + transcricao + "\n\n" + {pergunta}"""
        # memory_agent.print_response(pergunta, stream=True)
        response = memory_agent.run(pergunta, stream=True)
        for msg in response:
            print(msg.content, end="", flush=True)
        print("\n")
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


def main():
    
    while True:
        console.clear()
        escolha = questionary.select(
            "O que deseja fazer?",
            choices=[
                "1. Nova gravação",
                "2. Análise de transcrições",
                "3. Sair"
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
        else:
            break


if __name__ == "__main__":
    main()