# 📄 PDF Translator

Tradutor automático de PDFs com interface gráfica intuitiva e suporte a múltiplos idiomas.

## 🏗️ Arquitetura do Projeto

### Estrutura de Arquivos
```
PDF_translator/
├── README.md                     # Documentação do projeto
├── Projeto PdfTranslator/        # Diretório principal da aplicação
│   ├── pdf_translator.py         # Módulo principal de tradução
│   ├── gui.py                    # Interface gráfica (GUI)
│   ├── artigo.pdf               # Arquivo PDF de exemplo
│   ├── artigo_traduzido.txt     # Arquivo traduzido de exemplo
│   ├── .venv/                   # Ambiente virtual
│   └── __pycache__/             # Cache do Python
└── .git/                        # Controle de versão
```

### Componentes Principais

#### 1. **pdf_translator.py** - Motor de Tradução
- **Extração de Texto**: Utiliza PyMuPDF (fitz) para extrair texto de PDFs mantendo estrutura
- **Limpeza de Texto**: Remove hifenação, corrige formatação e normaliza espaços
- **Divisão Inteligente**: Divide o texto em blocos otimizados para APIs de tradução
- **Tradução**: Integração com Google Translator via deep-translator
- **Gerenciamento de Erros**: Retry automático e tratamento de falhas

#### 2. **gui.py** - Interface Gráfica
- **Framework**: ttkbootstrap para interface moderna e responsiva
- **Seleção de Arquivos**: File dialog intuitivo para escolha de PDFs
- **Configuração de Idiomas**: Combobox com 26 idiomas suportados
- **Progresso em Tempo Real**: Barra de progresso e log detalhado
- **Threading**: Processamento assíncrono para não bloquear a interface

### Fluxo de Processamento

```
PDF Entrada → Extração de Texto → Limpeza → Divisão em Blocos → Tradução → Salvamento
```

1. **Extração**: Lê PDF página por página preservando estrutura de parágrafos
2. **Limpeza**: Remove quebras de linha inadequadas e normaliza texto
3. **Divisão**: Cria blocos de até 4500 caracteres respeitando limites da API
4. **Tradução**: Processa cada bloco com retry automático em falhas
5. **Salvamento**: Gera arquivo .txt com separadores de página

## 🚀 Como Rodar o Projeto

### Pré-requisitos
- Python 3.7 ou superior
- pip (gerenciador de pacotes Python)

### Instalação de Dependências

#### Via pip (recomendado):
```bash
pip install pymupdf deep-translator ttkbootstrap
```

#### Ou via requirements.txt:
```bash
# Criar arquivo requirements.txt
echo "pymupdf
deep-translator
ttkbootstrap" > requirements.txt

# Instalar dependências
pip install -r requirements.txt
```

### Execução

#### 1. Interface Gráfica (Recomendado)
```bash
cd "Projeto PdfTranslator"
python gui.py
```

#### 2. Linha de Comando
```bash
cd "Projeto PdfTranslator"
python pdf_translator.py
```

#### 3. Modo Programático
```python
from pdf_translator import main

# Traduzir PDF específico
main(
    caminho_pdf="meu_documento.pdf",
    caminho_saida="documento_traduzido.txt",
    origem="en",           # inglês
    destino="pt"           # português
)
```

## 🌐 Idiomas Suportados

O projeto suporta 26 idiomas com detecção automática:

| Idioma | Código |
|--------|--------|
| Detectar automaticamente | auto |
| Afrikaans | af |
| Alemão | de |
| Árabe | ar |
| Chinês (simplificado) | zh-CN |
| Chinês (tradicional) | zh-TW |
| Coreano | ko |
| Dinamarquês | da |
| Espanhol | es |
| Finlandês | fi |
| Francês | fr |
| Grego | el |
| Hindi | hi |
| Holandês | nl |
| Húngaro | hu |
| Indonésio | id |
| Inglês | en |
| Italiano | it |
| Japonês | ja |
| Norueguês | no |
| Persa | fa |
| Polonês | pl |
| Português | pt |
| Romeno | ro |
| Russo | ru |
| Sueco | sv |
| Tailandês | th |
| Tcheco | cs |
| Turco | tr |
| Ucraniano | uk |
| Vietnamita | vi |

## ✨ Principais Funcionalidades

### 🎯 Funcionalidades Principais
- **Tradução Automática**: Tradução completa de PDFs com um clique
- **Interface Intuitiva**: GUI moderna com design responsivo
- **Múltiplos Idiomas**: Suporte a 26 idiomas diferentes
- **Detecção Automática**: Identificação automática do idioma de origem
- **Preservação de Estrutura**: Mantém formatação e separação por páginas

### 🔧 Funcionalidades Técnicas
- **Processamento Assíncrono**: Interface não bloqueia durante tradução
- **Gerenciamento de Erros**: Retry automático em falhas de API
- **Otimização de Blocos**: Divisão inteligente para maximizar eficiência
- **Log Detalhado**: Acompanhamento em tempo real do progresso
- **Tratamento de Imagens**: Identifica e pula páginas baseadas em imagens

### 📊 Funcionalidades de Saída
- **Formato Estruturado**: Arquivo .txt com separadores de página
- **Preservação de Conteúdo**: Mantém texto original em caso de falha
- **Nomenclatura Automática**: Gera nome de arquivo baseado no original

## 👤 Autor

**Desenvolvido por: Davi Silva**

- Desenvolvedor Python especializado em automação e processamento de texto
- Foco em soluções práticas para tradução e processamento de documentos

## 🙏 Créditos e Agradecimentos

### Orientação Acadêmica
**Professor Orientador:** [Nome do Professor]

Agradecimento especial ao professor pela orientação, suporte técnico e compartilhamento de conhecimento que foram fundamentais para o desenvolvimento deste projeto.

### Bibliotecas e Ferramentas
- **PyMuPDF (fitz)**: Para extração eficiente de texto de PDFs
- **deep-translator**: Para integração com serviços de tradução online
- **ttkbootstrap**: Para interface gráfica moderna e responsiva
- **Python**: Linguagem principal do projeto

### Comunidade
Agradecimento à comunidade open source por fornecer as ferramentas e bibliotecas que tornaram este projeto possível.

## 📝 Licença

Este projeto está disponível sob licença MIT. Sinta-se à vontade para contribuir, modificar e utilizar conforme suas necessidades.

## 🤝 Como Contribuir

1. Fork este repositório
2. Crie sua feature branch (`git checkout -b feature/NovaFuncionalidade`)
3. Commit suas mudanças (`git commit -m 'Adicionando nova funcionalidade'`)
4. Push para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abra um Pull Request

## 📞 Suporte

Para dúvidas, sugestões ou report de bugs:
- Abra uma issue no repositório
- Entre em contato através do email: [seu-email@exemplo.com]

---

**Versão:** 1.0.0  
**Última Atualização:** Abril 2026