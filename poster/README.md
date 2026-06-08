# Painel A1

Fonte LaTeX do painel acadêmico (A1, retrato, tikzposter).

Arquivo principal: `painel.tex`. Imagens consumidas: `metrics/graph.png`, `metrics/confusion_matrix.png`, `metrics/qrcode_repo.png`.

## Antes de compilar

Os PNGs são gerados pelos scripts do projeto:

```powershell
python evals.py
python scripts/generate_diagram.py
python scripts/generate_qrcode.py
```

## Overleaf

1. Cria projeto em branco.
2. Sobe o `painel.tex` na raiz e os três PNGs dentro de uma pasta `metrics/`.
3. Garante que o compilador está em pdfLaTeX.
4. Recompile. Baixa o PDF, renomeia pra `painel_A1.pdf`, joga em `painel/` na raiz do repo.

## Local

Se tiver TeX Live ou MiKTeX:

```powershell
cd poster
pdflatex painel.tex
pdflatex painel.tex
```

Duas passadas pra referências internas se acertarem.

## Antes de mandar pra gráfica

- Os seis blocos cabem sem estouro?
- Diagrama do grafo nítido?
- QR escaneia (testar com o celular)?
- Nome de todo mundo correto?
- URL do rodapé bate com o QR?

## Ajustes comuns

Mudar URL do QR: roda `python scripts/generate_qrcode.py <URL>` e recompila o painel.

Cores: alterar `lgPrimary` e `lgAccent` no preâmbulo.

Logo da faculdade: `\titlegraphic{\includegraphics[height=2cm]{logo.png}}` antes do `\maketitle`.
