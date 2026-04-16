import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox
import threading
import sys
import os
import pdf_translator


# ─────────────────────────────────────────────
# REDIRECIONAR PRINT
# ─────────────────────────────────────────────
class RedirectOutput:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        self.text_widget.insert("end", message)
        self.text_widget.see("end")

    def flush(self):
        pass


# ─────────────────────────────────────────────
# AÇÕES
# ─────────────────────────────────────────────
def escolher_pdf(entry):
    caminho = filedialog.askopenfilename(
        title="Selecionar PDF",
        filetypes=[("PDF", "*.pdf")]
    )
    if caminho:
        entry.delete(0, "end")
        entry.insert(0, caminho)


def executar_traducao(entry, combo_origem, combo_destino, btn, progress, status):
    caminho_pdf = entry.get()

    if not caminho_pdf or not os.path.exists(caminho_pdf):
        messagebox.showerror("Erro", "Selecione um PDF válido.")
        return

    # Obter códigos ISO a partir dos nomes exibidos
    nome_origem = combo_origem.get()
    nome_destino = combo_destino.get()
    codigo_origem = pdf_translator.LANGUAGES.get(nome_origem, "auto")
    codigo_destino = pdf_translator.LANGUAGES.get(nome_destino, "pt")

    if codigo_destino == "auto":
        messagebox.showerror(
            "Erro",
            "Selecione um idioma de DESTINO válido (não pode ser 'Detectar automaticamente')."
        )
        return

    caminho_saida = os.path.splitext(caminho_pdf)[0] + "_traduzido.txt"

    def tarefa():
        try:
            btn.config(state=DISABLED)
            progress.start()
            status.config(text="🔄 Processando...")

            print(f"📄 Lendo PDF...")
            print(f"🌐 Idioma: {nome_origem}  →  {nome_destino}\n")
            paginas = pdf_translator.ler_pdf(caminho_pdf)

            resultado = []

            for pg in paginas:
                print(f"\n── Página {pg['pagina']} ──")

                texto_limpo = pdf_translator.limpar_texto(pg["texto"])

                if not texto_limpo:
                    print("(sem texto)")
                    resultado.append({**pg, "texto_traduzido": "[sem texto]"})
                    continue

                blocos = pdf_translator.dividir_em_blocos(texto_limpo)
                traducoes = pdf_translator.traduzir_blocos(
                    blocos,
                    origem=codigo_origem,
                    destino=codigo_destino,
                )

                resultado.append({
                    **pg,
                    "texto_traduzido": "\n\n".join(traducoes)
                })

            print("\n💾 Salvando...")
            pdf_translator.salvar_resultado(resultado, caminho_saida)

            print("\n✅ Finalizado!")
            status.config(text="✅ Concluído")

            messagebox.showinfo(
                "Sucesso",
                f"Tradução concluída!\n\nArquivo salvo em:\n{caminho_saida}"
            )

        except Exception as e:
            messagebox.showerror("Erro", str(e))
            status.config(text="❌ Erro")

        finally:
            progress.stop()
            btn.config(state=NORMAL)

    threading.Thread(target=tarefa, daemon=True).start()


# ─────────────────────────────────────────────
# GUI
# ─────────────────────────────────────────────
def card(parent, titulo: str):
    """Retorna um Frame com título simulado, compatível com qualquer versão do ttkbootstrap."""
    outer = ttk.Frame(parent, padding=(0, 0, 0, 8))
    outer.pack(fill=X)
    ttk.Label(outer, text=titulo, font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(0, 4))
    inner = ttk.Frame(outer, padding=10, bootstyle="secondary")
    inner.pack(fill=X)
    return inner


def criar_interface():
    app = ttk.Window(themename="superhero")
    app.title("Tradutor de PDF")
    app.geometry("820x660")
    app.resizable(True, True)

    container = ttk.Frame(app, padding=20)
    container.pack(fill=BOTH, expand=True)

    # ── HEADER ───────────────────────────────
    ttk.Label(
        container,
        text="📄 Tradutor de PDF",
        font=("Segoe UI", 20, "bold"),
        bootstyle=INFO,
    ).pack(anchor="center", pady=(0, 4))

    ttk.Label(
        container,
        text="Traduza PDFs automaticamente para qualquer idioma",
        font=("Segoe UI", 10),
    ).pack(anchor="center", pady=(0, 16))

    # ── CARD: ARQUIVO ────────────────────────
    c_arquivo = card(container, "📂  Arquivo PDF")

    row_pdf = ttk.Frame(c_arquivo)
    row_pdf.pack(fill=X)

    entry = ttk.Entry(row_pdf, font=("Segoe UI", 10))
    entry.pack(side=LEFT, fill=X, expand=True, padx=(0, 6))

    ttk.Button(
        row_pdf,
        text="Escolher",
        bootstyle=PRIMARY,
        command=lambda: escolher_pdf(entry)
    ).pack(side=LEFT)

    # ── CARD: IDIOMAS ────────────────────────
    nomes_idiomas = list(pdf_translator.LANGUAGES.keys())
    nomes_destino = [n for n in nomes_idiomas if n != "Detectar automaticamente"]

    c_idiomas = card(container, "🌐  Idiomas")

    c_idiomas.columnconfigure(0, weight=1)
    c_idiomas.columnconfigure(1, weight=0)
    c_idiomas.columnconfigure(2, weight=1)

    # Origem
    ttk.Label(
        c_idiomas,
        text="Idioma de Origem",
        font=("Segoe UI", 9, "bold"),
    ).grid(row=0, column=0, sticky="w", pady=(0, 4))

    combo_origem = ttk.Combobox(
        c_idiomas,
        values=nomes_idiomas,
        state="readonly",
        font=("Segoe UI", 10),
    )
    combo_origem.set("Detectar automaticamente")
    combo_origem.grid(row=1, column=0, sticky="ew")

    # Seta
    ttk.Label(
        c_idiomas,
        text=" → ",
        font=("Segoe UI", 14, "bold"),
    ).grid(row=1, column=1, padx=10)

    # Destino
    ttk.Label(
        c_idiomas,
        text="Idioma de Destino",
        font=("Segoe UI", 9, "bold"),
    ).grid(row=0, column=2, sticky="w", pady=(0, 4))

    combo_destino = ttk.Combobox(
        c_idiomas,
        values=nomes_destino,
        state="readonly",
        font=("Segoe UI", 10),
    )
    combo_destino.set("Português")
    combo_destino.grid(row=1, column=2, sticky="ew")

    # ── BOTÃO ───────────────────────────────
    btn = ttk.Button(
        container,
        text="🚀 Iniciar Tradução",
        bootstyle="success-outline",
        width=28,
    )
    btn.pack(pady=12)

    # ── PROGRESSO ───────────────────────────
    progress = ttk.Progressbar(container, mode="indeterminate", bootstyle=SUCCESS)
    progress.pack(fill=X, pady=(0, 4))

    status = ttk.Label(container, text="⏳ Aguardando...", font=("Segoe UI", 9))
    status.pack(anchor="center", pady=(0, 8))

    # ── LOG ─────────────────────────────────
    ttk.Label(container, text="📋  Log", font=("Segoe UI", 9, "bold")).pack(anchor="w")

    log_outer = ttk.Frame(container, bootstyle="secondary", padding=6)
    log_outer.pack(fill=BOTH, expand=True)

    text = ttk.Text(
        log_outer,
        wrap="word",
        font=("Consolas", 10),
    )
    text.pack(fill=BOTH, expand=True)

    # Redireciona print para o widget de log
    sys.stdout = RedirectOutput(text)
    sys.stderr = RedirectOutput(text)

    # Conecta botão
    btn.config(
        command=lambda: executar_traducao(
            entry, combo_origem, combo_destino, btn, progress, status
        )
    )

    return app


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
if __name__ == "__main__":
    app = criar_interface()
    app.mainloop()