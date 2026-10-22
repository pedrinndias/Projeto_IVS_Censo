"""Lista o que o Pedro mudou à mão nas tabelas dos decks das 108 versões da análise fatorial.

O deck é regerado do zero a cada lote ou correção, e isso apagaria edições feitas no
PowerPoint. Este script compara, slide a slide e célula a célula, as tabelas da cópia
editada com as do deck gerado e grava cada diferença com o ID do slide, para a mudança ser
levada à origem (protocolo de correção, seção 5 do prompt) antes de regerar.

A comparação é a de `comparar_edicoes_relatorio.py` (`relatar`); aqui só mudam a pasta e os IDs.

Uso:  ./.venv/bin/python scripts/comparar_edicoes_versoes.py principal|caderno [deck_editado.pptx]
      (sem o segundo argumento, compara o deck da pasta com dados/ultimo_gerado_<deck>.pptx)
Saída: versoes_fatorial/dados/edicoes_do_pedro_<deck>.csv
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from comparar_edicoes_relatorio import RAIZ, relatar

PASTA = RAIZ / 'versoes_fatorial'
ARQ = {'principal': 'Versoes_Fatorial_Principal.pptx', 'caderno': 'Caderno_Fichas_108.pptx'}
ID = re.compile(r'^(V\d{3}|VF\d{2}|VP\d{2}(-\d+)?)$')


def main() -> None:
    if len(sys.argv) < 2 or sys.argv[1] not in ARQ:
        sys.exit(__doc__)
    deck = sys.argv[1]
    editado = Path(sys.argv[2]) if len(sys.argv) > 2 else PASTA / ARQ[deck]
    relatar(PASTA / 'dados' / f'ultimo_gerado_{deck}.pptx', editado, ID, PASTA / 'dados' / f'edicoes_do_pedro_{deck}.csv')


if __name__ == '__main__':
    main()
