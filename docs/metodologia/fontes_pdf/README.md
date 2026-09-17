# Fontes dos PDFs de metodologia

Os dois PDFs sobre análise fatorial em `docs/` são **gerados**, não editados à mão —
mesma política da pasta `docs/Apresentacoes_IVS`. Mudanças permanentes vão nestes
arquivos-fonte, nunca no PDF.

| Fonte | PDF gerado |
|---|---|
| `Guia_Leitura_Analise_Fatorial_Enap2019.html` | `../Guia_Leitura_Analise_Fatorial_Enap2019.pdf` |
| `Implementacao_Fatorial_NB04_Brainstorm_e_Prompt.html` | `../Implementacao_Fatorial_NB04_Brainstorm_e_Prompt.pdf` |
| `estilo.css` | folha comum aos dois |

## Como regerar

Qualquer Chromium/Chrome em modo headless serve:

```bash
chromium --headless --disable-gpu --allow-file-access-from-files \
  --no-pdf-header-footer \
  --print-to-pdf="docs/metodologia/Guia_Leitura_Analise_Fatorial_Enap2019.pdf" \
  "file://$PWD/docs/fontes_pdf/Guia_Leitura_Analise_Fatorial_Enap2019.html"
```

`--allow-file-access-from-files` é necessário para que o HTML carregue o `estilo.css`
ao lado. Repita trocando os dois nomes para o segundo documento.

## Identidade visual

O `estilo.css` reproduz a identidade já usada pelos geradores do projeto
(`scripts/gerar_pdf_outliers_renda.py`, `scripts/gerar_resumo_eda_central.py`,
`scripts/gerar_deck_eda_central.js`):

- paleta de papel — tinta `#1A1A1A`, petrol `#1F4E4A`, clay `#A83A2C`,
  cinza `#666666`, linha `#C8C8C8`, fundo `#F2F0EC`;
- serifada nos títulos, sans no corpo;
- tabelas no padrão *booktabs*: três filetes, sem preenchimento nem cor de cabeçalho.

As fontes Cambria e Calibri usadas nos `.docx`/`.pptx` não existem em ambiente Linux;
o CSS usa Liberation Serif e Liberation Sans, que são métricamente compatíveis com
Times e Arial e mantêm a mesma leitura de página impressa.
