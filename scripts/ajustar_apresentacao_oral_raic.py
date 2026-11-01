"""Ajustes de 29/10 sobre o _ENVIO que o Pedro editou à mão (a versão do WhatsApp).

Não regera o deck: abre o pptx editado e mexe só nisto.
- Slide 7: a barra passa a mostrar o lado inadequado (setores com ao menos um domicílio com o
  problema); o cartão da renda ganha a mediana e a média em reais.
- Slide 10: o grafo perde o lixo; fica só o triângulo renda × cor/raça × analfabetismo.
- Dois grafos novos depois do 10, no mesmo molde: esgoto com o triângulo, e o bloco
  cor/raça, razão de moradores, idosos, renda, crianças e analfabetismo.
- Slide 9 (matriz): os quadrados do Pedro saem e entram, no mesmo estilo, quadrados alinhados às
  células de todos os pares que aparecem nos grafos (triângulo inferior).

Revisão do council (30/10):
- título do 7 no número que a barra destaca; "também" sai do título do 6 (agora ele vem antes
  dos zeros);
- cores do 13 iguais às do grafo de idade (coral = negativa);
- rótulo cor/raça × moradores sai de cima da linha renda × crianças;
- digitação nos slides 3, 9 e 15.

Pente fino do council (30/10, à noite), com a Tabela 1 na fala (slide 8), como o Pedro decidiu:
- etiqueta RESULTADOS nos slides 8 e 9; "Assimetria" e legenda do negrito na Tabela 1;
- saem as remissões a reservas que não existem (R1, R6) e a "Figura 1 do relatório";
- sigilo descrito pelos dois casos (slides 5 e 7); "Objetivo específico" no slide 3; "Obrigado!";
- conclusões: o lixo vira meia frase da 1, o sigilo é o do analfabetismo e entra o 50 de 53.

Números: os mesmos do gerador (pecas.json para as correlações, T03 para os zeros, Tabela 1 para
a renda).

Uso:  ./.venv/bin/python scripts/ajustar_apresentacao_oral_raic.py ENTRADA.pptx SAIDA.pptx
"""
from __future__ import annotations

import copy
import sys
from pathlib import Path

from matplotlib.patches import Circle
from pptx import Presentation
from pptx.util import Cm, Emu

from gerar_apresentacao_oral_raic import (CINZA, CINZA_CLARO, CORAL, FIGURAS, LAVANDA, PECAS, R, T03, TAB1,
                                          TEAL, TEAL_CLARO, TEXTO, br, cor, plt)

RENDA, RACA, ANALF = 'renda_media_sem_extremo', 'pct_raca_pretpardind', 'pct_analfab'
ESGOTO, RAZAO = 'pct_esgoto_inad', 'razao_moradores'
IDOSO, CRIANCA = 'pct_idoso_60mais', 'pct_pop_0a14'
NOME = {RENDA: 'Renda\n(invertida)', RACA: 'Cor/raça\npreta, parda\nou indígena', ANALF: 'Analfabetismo',
        ESGOTO: 'Esgoto\ninadequado', RAZAO: 'Moradores\npor domicílio', IDOSO: 'Idosos\n(60+)',
        CRIANCA: 'Crianças\n(0–14)'}
POL_POR_UNIDADE = 1.96  # a escala do grafo original (10,4 pol para 5,3 unidades): nós e fontes iguais
AREA_GRAFO = (0.6, 4.7, 22.6, 13.0)  # x, y, largura, altura (cm) à esquerda do "Como ler"


# ---------------------------------------------------------------- figuras

def fig_inadequado() -> Path:
    """Slide 7: % de setores com ao menos um domicílio registrado com o problema (100 − pct_zeros)."""
    itens = [('Água inadequada', 'pct_agua_inad'), ('Esgoto inadequado', 'pct_esgoto_inad'),
             ('Lixo inadequado', 'pct_lixo_inad')]
    fig, ax = plt.subplots(figsize=(8.6, 4.6), dpi=200)
    for i, (rotulo, col) in enumerate(reversed(itens)):
        z = float(T03[col]['pct_zeros'])
        ax.barh(i, 100 - z, color=cor(CORAL), height=0.62)
        ax.barh(i, z, left=100 - z, color=cor(CINZA_CLARO), height=0.62)
        ax.text(100 - z - 2, i, f'{br(100 - z, 0)}%', va='center', ha='right', color='white', fontsize=30,
                weight='bold')
        ax.text(98, i, f'{br(z, 0)}% sem nenhum', va='center', ha='right', color=cor(CINZA), fontsize=17)
        ax.text(-2, i, rotulo, va='center', ha='right', fontsize=18, color=cor(TEXTO))
    ax.set_xlim(0, 100)
    ax.set_ylim(-0.6, 2.9)
    ax.axis('off')
    ax.text(0, 2.62, 'setores com ao menos um domicílio registrado com o problema', color=cor(CORAL),
            fontsize=14, weight='bold')
    fig.subplots_adjust(left=0.27, right=0.98, top=0.98, bottom=0.02)
    caminho = FIGURAS / 'oral_inadequado_saneamento.png'
    fig.savefig(caminho, transparent=True)
    plt.close(fig)
    return caminho


def fig_grafo(nome_arquivo: str, pos: dict, arestas: list, xlim, ylim, rotulo_pt=22, no_pt=14,
              destaque=()) -> Path:
    """Grafo de correlações de Spearman (Figura 1): espessura pela força, coral tracejado se negativa.

    arestas: (a, b) ou (a, b, fração) — a fração diz onde, na linha de a para b, fica o número.
    destaque: nós pintados de lavanda (o que entra de novo em relação ao triângulo).
    """
    w, h = (xlim[1] - xlim[0]) * POL_POR_UNIDADE, (ylim[1] - ylim[0]) * POL_POR_UNIDADE
    fig, ax = plt.subplots(figsize=(w, h), dpi=200)
    for a, b, *frac in arestas:
        r = R[a][b]
        t = frac[0] if frac else 0.5
        (x1, y1), (x2, y2) = pos[a], pos[b]
        linha = cor(TEAL) if r > 0 else cor(CORAL)
        ax.plot([x1, x2], [y1, y2], color=linha, lw=max(1.5, 4 + 14 * (abs(r) - 0.5)),
                linestyle='-' if r > 0 else (0, (3, 1.5)), solid_capstyle='round', zorder=1)
        ax.text(x1 + t * (x2 - x1), y1 + t * (y2 - y1), br(r, 2), ha='center', va='center',
                fontsize=rotulo_pt, weight='bold', color=cor(TEXTO) if r > 0 else cor(CORAL),
                bbox=dict(boxstyle='round,pad=0.2', fc='white', ec='none'), zorder=3)
    for n, (x, y) in pos.items():
        ax.add_patch(Circle((x, y), 0.4, facecolor=cor(LAVANDA if n in destaque else TEAL_CLARO),
                            edgecolor=cor(TEAL), linewidth=2, zorder=2))
        ax.text(x, y, NOME[n], ha='center', va='center', fontsize=no_pt, weight='bold', color=cor(TEXTO), zorder=4)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    caminho = FIGURAS / nome_arquivo
    fig.savefig(caminho, transparent=True)
    plt.close(fig)
    return caminho


TRIANGULO = {RENDA: (0.0, 1.0), RACA: (-0.95, -0.45), ANALF: (0.95, -0.45)}
GRAFOS = {
    # slide 10, sem o lixo: as mesmas posições do grafo original
    'triangulo': dict(nome_arquivo='oral_grafo_renda_raca_analfabetismo.png', pos=TRIANGULO,
                      arestas=[(RENDA, RACA), (RENDA, ANALF), (ANALF, RACA)],
                      xlim=(-1.7, 1.7), ylim=(-1.0, 1.55)),
    # esgoto no centro do triângulo, aberto o bastante para caber o número em cada raio
    'esgoto': dict(nome_arquivo='oral_grafo_esgoto.png',
                   pos={RENDA: (0.0, 1.75), RACA: (-1.65, -0.8), ANALF: (1.65, -0.8), ESGOTO: (0.0, 0.05)},
                   arestas=[(RENDA, RACA), (RENDA, ANALF), (ANALF, RACA),
                            (ESGOTO, RENDA), (ESGOTO, RACA), (ESGOTO, ANALF)],
                   xlim=(-2.15, 2.15), ylim=(-1.3, 2.25), no_pt=16, destaque=(ESGOTO,)),
    # hexágono: idosos e crianças nas pontas; o triângulo social em cima e à direita
    'idade': dict(nome_arquivo='oral_grafo_idade.png',
                  pos={IDOSO: (-2.3, 0.0), RENDA: (-1.15, 1.25), RACA: (1.15, 1.25), CRIANCA: (2.3, 0.0),
                       ANALF: (1.15, -1.25), RAZAO: (-1.15, -1.25)},
                  arestas=[(IDOSO, RENDA), (RENDA, RACA), (RACA, CRIANCA), (CRIANCA, ANALF), (ANALF, RAZAO),
                           (RAZAO, IDOSO),
                           (IDOSO, RACA, 0.3), (RENDA, CRIANCA, 0.7), (ANALF, RACA, 0.2), (CRIANCA, RAZAO, 0.3),
                           (ANALF, IDOSO, 0.7), (RAZAO, RENDA, 0.2),
                           (IDOSO, CRIANCA), (RENDA, ANALF, 0.25), (RACA, RAZAO, 0.35)],
                  xlim=(-2.75, 2.75), ylim=(-1.7, 1.7), rotulo_pt=17, destaque=(IDOSO, CRIANCA, RAZAO)),
}


# ---------------------------------------------------------------- pptx

def trocar_texto(shape, textos: list[str]) -> None:
    """Troca o texto parágrafo a parágrafo, mantendo a formatação do primeiro run de cada um."""
    paras = shape.text_frame.paragraphs
    for p, t in zip(paras, textos):
        p.runs[0].text = t
        for r in p.runs[1:]:
            r._r.getparent().remove(r._r)


def substituir(shape, velho: str, novo: str) -> None:
    """Troca um trecho dentro de um run, sem mexer na formatação; falha se o trecho não existir."""
    for p in shape.text_frame.paragraphs:
        for r in p.runs:
            if velho in r.text:
                r.text = r.text.replace(velho, novo)
                return
    raise ValueError(f'{velho!r} não está em {shape.name}')


def figura(slide):
    return next(sh for sh in slide.shapes if sh.shape_type == 13)


def trocar_figura(slide, caminho: Path, area=AREA_GRAFO) -> None:
    """Põe a figura no lugar da que existe (se houver); se `area`, encaixa e centraliza nela mantendo a
    proporção; sem `area`, ocupa a posição e a largura da antiga."""
    velha = next((sh for sh in slide.shapes if sh.shape_type == 13), None)
    if velha is not None:
        x, y, w = velha.left, velha.top, velha.width
        velha._element.getparent().remove(velha._element)
    if area is None:
        slide.shapes.add_picture(str(caminho), x, y, width=w)
        return
    nova = slide.shapes.add_picture(str(caminho), Cm(area[0]), Cm(area[1]))
    esc = min(Cm(area[2]) / nova.width, Cm(area[3]) / nova.height)
    nova.width, nova.height = int(nova.width * esc), int(nova.height * esc)
    nova.left = int(Cm(area[0]) + (Cm(area[2]) - nova.width) / 2)
    nova.top = int(Cm(area[1]))
    # a figura vai para o fundo da pilha, como estava (logo depois das formas fixas do layout)
    arvore = nova._element.getparent()
    arvore.remove(nova._element)
    arvore.insert(2, nova._element)


def duplicar(prs, slide, posicao: int):
    """Cópia do slide (só formas sem relação: a figura é trocada depois) na posição dada (0 = primeira)."""
    novo = prs.slides.add_slide(slide.slide_layout)
    for sh in list(novo.shapes):
        sh._element.getparent().remove(sh._element)
    for sh in slide.shapes:
        if sh.shape_type != 13:
            novo.shapes._spTree.append(copy.deepcopy(sh._element))
    lista = prs.slides._sldIdLst
    el = lista[-1]
    lista.remove(el)
    lista.insert(posicao, el)
    return novo


def forma(slide, nome: str):
    return next(sh for sh in slide.shapes if sh.name == nome)


# Pares dos grafos marcados na matriz (índices na ordem da Figura 1; linha > coluna = triângulo
# inferior). Cada entrada é um quadrado: (linha inicial, linha final, coluna inicial, coluna final).
ORDEM = PECAS['figura1']['indicadores']
QUADRADOS = [
    (4, 6, 1, 1),     # esgoto × analfabetismo, renda, cor/raça
    (4, 4, 3, 3),     # analfabetismo × moradores
    (5, 5, 3, 4),     # renda × moradores, analfabetismo
    (6, 6, 3, 5),     # cor/raça × moradores, analfabetismo, renda
    (10, 10, 3, 6),   # idosos × moradores, analfabetismo, renda, cor/raça
    (11, 11, 3, 6),   # crianças × moradores, analfabetismo, renda, cor/raça
    (11, 11, 10, 10),  # crianças × idosos
]
# Grade da fig1_correlacao.png (1490 × 1402 px), medida nas bordas pretas do imshow.
GRADE_X0, GRADE_Y0, CELULA_PX = 406.5, 18.5, (1470.0 - 406.5) / 12


def conferir_quadrados() -> None:
    """Todo par de todos os grafos tem um quadrado, e nenhum quadrado cobre par fora dos grafos."""
    pares = {frozenset(a[:2]) for g in GRAFOS.values() for a in g['arestas']}
    cobertos = {frozenset((ORDEM[i], ORDEM[j])) for i0, i1, j0, j1 in QUADRADOS
                for i in range(i0, i1 + 1) for j in range(j0, j1 + 1)}
    assert pares == cobertos, (pares - cobertos, cobertos - pares)


def marcar_matriz(slide) -> None:
    pic = figura(slide)
    px = pic.width / 1490
    modelo = next(sh for sh in slide.shapes if sh.name.startswith('Retângulo'))._element
    for sh in [sh for sh in slide.shapes if sh.name.startswith('Retângulo')]:
        sh._element.getparent().remove(sh._element)
    arvore = slide.shapes._spTree
    proximo = max(int(e.get('id')) for e in arvore.iter() if e.tag.endswith('}cNvPr')) + 1
    for k, (i0, i1, j0, j1) in enumerate(QUADRADOS):
        el = copy.deepcopy(modelo)
        nv = el.find('.//{*}cNvPr')
        nv.set('id', str(proximo + k))
        nv.set('name', f'Quadrado {k + 1}')
        for ext in nv.findall('{*}extLst'):
            nv.remove(ext)
        off, tam = el.find('.//{*}off'), el.find('.//{*}ext')
        off.set('x', str(int(pic.left + (GRADE_X0 + j0 * CELULA_PX) * px)))
        off.set('y', str(int(pic.top + (GRADE_Y0 + i0 * CELULA_PX) * px)))
        tam.set('cx', str(int((j1 - j0 + 1) * CELULA_PX * px)))
        tam.set('cy', str(int((i1 - i0 + 1) * CELULA_PX * px)))
        arvore.append(el)


def main(entrada: Path, saida: Path) -> None:
    conferir_quadrados()
    figs = {k: fig_grafo(**g) for k, g in GRAFOS.items()}
    inad = fig_inadequado()

    prs = Presentation(str(entrada))
    s3, s4, s5, s6, s7, s8, s9, s10, s13, s14, s15 = (prs.slides[i] for i in (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12))

    trocar_figura(s7, inad, area=None)
    t1 = {r['indicador']: r for r in TAB1}[RENDA]
    renda = forma(s7, 'Rectangle 5')
    # mediana e média em reais, entre a frase de destaque e a explicação
    for linha in (f'média R$ {t1["Média"]}', f'mediana R$ {t1["Mediana"]}'):
        extra = copy.deepcopy(renda.text_frame.paragraphs[2]._p)
        renda.text_frame.paragraphs[1]._p.addnext(extra)
        renda.text_frame.paragraphs[2].runs[0].text = linha
        renda.text_frame.paragraphs[2].runs[0].font.bold = True
        renda.text_frame.paragraphs[2].space_after = 0
    renda.height = Cm(6.6)
    forma(s7, 'Rectangle 6').top = Cm(11.7)

    trocar_figura(s10, figs['triangulo'])
    trocar_texto(forma(s10, 'Rectangle 2'), ['Renda, cor/raça e analfabetismo andam juntos'])

    como_ler = 'Correlação: 0 = nenhuma relação; 1 = as duas ordenam os setores do mesmo jeito.'
    s_esg = duplicar(prs, s10, 10)
    trocar_figura(s_esg, figs['esgoto'])
    trocar_texto(forma(s_esg, 'Rectangle 2'), ['O esgoto inadequado acompanha esse bloco, mas com força moderada'])
    trocar_texto(forma(s_esg, 'Rectangle 4'),
                 ['Como ler', como_ler, 'O esgoto se liga às três com cerca de 0,4, bem menos que elas entre si.'])

    s_idade = duplicar(prs, s10, 11)
    trocar_figura(s_idade, figs['idade'])
    trocar_texto(forma(s_idade, 'Rectangle 2'), ['Mais idosos onde a renda é maior; mais crianças onde ela é menor'])
    trocar_texto(forma(s_idade, 'Rectangle 4'),
                 ['Como ler', como_ler + ' Coral tracejado: relação inversa.',
                  'Crianças acompanham o bloco social; idosos vão no sentido oposto.'])
    for s in (s_esg, s_idade):
        forma(s, 'Rectangle 4').height = Cm(6.9)

    marcar_matriz(s9)
    rodape = forma(s9, 'Rectangle 3')
    rodape.text_frame.paragraphs[0].runs[-1].text += ' Quadrados: pares mostrados nos grafos dos slides 10 a 12.'

    # ---- revisão do council
    agua = 100 - float(T03['pct_agua_inad']['pct_zeros'])
    trocar_texto(forma(s7, 'Rectangle 2'),
                 [f'Só {br(agua, 0)}% dos setores têm algum domicílio registrado com água inadequada'])
    trocar_texto(forma(s6, 'Rectangle 2'), ['O dado que falta diz alguma coisa'])
    trocar_texto(forma(s9, 'Rectangle 1'), ['Matriz de correlação de Spearman entre os 12 indicadores'])
    forma(s3, 'Rectangle 7').text_frame.paragraphs[0].runs[2].text = 'obrigou'
    forma(s15, 'CaixaDeTexto 1').text_frame.paragraphs[2].runs[1].text = ': pedro3soares@gmail.com'
    cartao = forma(s13, 'Rectangle 4').text_frame.paragraphs
    cartao[2].runs[0].font.color.rgb, cartao[4].runs[0].font.color.rgb = (cartao[4].runs[0].font.color.rgb,
                                                                          cartao[2].runs[0].font.color.rgb)
    # ---- pente fino (30/10, à noite): a Tabela 1 fica na fala, como o Pedro deixou
    trocar_texto(forma(s8, 'Rectangle 1'), ['Estatísticas descritivas dos 12 indicadores (Tabela 1)'])
    secao = forma(s10, 'Rectangle 1')._element  # a etiqueta RESULTADOS dos grafos
    for s in (s8, s9):
        titulo_s = forma(s, 'Rectangle 1')
        titulo_s.top, titulo_s.height = Cm(2.85), Cm(1.7)
        s.shapes._spTree.append(copy.deepcopy(secao))
    substituir(forma(s4, 'Rectangle 7'), ' (reserva R1)', '')
    substituir(forma(s4, 'Rectangle 13'), ' (R6)', '')
    substituir(forma(s5, 'Rectangle 6'), 'dados sob sigilo tratados como ausentes',
               'indicador todo sob sigilo tratado como ausente')
    substituir(forma(s5, 'Rectangle 6'), ' (reserva R1)', '')
    substituir(forma(s3, 'Rectangle 3'), 'Meu objetivo 1', 'Objetivo específico 1')
    substituir(forma(s3, 'Rectangle 5'), 'Meu objetivo 2', 'Objetivo específico 2')
    substituir(forma(s7, 'Rectangle 4'), 'Parte dos zeros vem de parcelas pequenas suprimidas pelo IBGE, que entram como zero.',
               'Parte dos zeros vem do sigilo: quando o IBGE suprime só algumas parcelas, elas entram como zero.')
    tabela = next(sh for sh in s8.shapes if sh.has_table).table
    tabela.cell(0, 6).text_frame.paragraphs[0].runs[0].text = 'Assimetria'
    forma(s8, 'Rectangle 3').text_frame.paragraphs[0].runs[-1].text += (
        ' Em negrito: indicadores complementares, fora do IVS 2012.')
    substituir(forma(s9, 'Rectangle 3'), ' Figura 1 do relatório parcial.', '')
    for s in (s10, s_esg, s_idade):
        substituir(forma(s, 'Rectangle 6'), ' (Figura 1 do relatório)', '')
    substituir(forma(s15, 'CaixaDeTexto 1'), 'Obrigado(a)!', 'Obrigado!')
    conclusoes = forma(s14, 'Rectangle 3').text_frame.paragraphs
    conclusoes[1].runs[1].text = ('Montar o IVS com o Censo 2022 exige decisões explícitas sobre zeros, sigilo e valores '
                                  'extremos; o lixo, que quase não se liga aos outros indicadores, será testado na '
                                  'análise fatorial.')
    conclusoes[2].runs[1].text = 'O sigilo do analfabetismo se concentra nos setores mais ricos e precisa de tratamento próprio.'
    rob = PECAS['robustez_figura1']
    conclusoes[3].runs[1].text = (f'Em {rob["municipios_idoso_renda_negativa"]} de {rob["municipios_30mais"]} municípios, '
                                  'os setores de renda mais alta têm mais idosos (associação entre áreas).')

    prs.save(str(saida))
    print(f'{saida.name}: {len(prs.slides)} slides')


if __name__ == '__main__':
    main(Path(sys.argv[1]), Path(sys.argv[2]))
