// Folha de contato de um PDF (as páginas em miniatura, numeradas, numa imagem só).
//
//     swift scripts/folha_contato.swift <deck.pdf> <saida.png> [colunas] [largura] [páginas]
//     swift scripts/folha_contato.swift <deck.pdf> <pasta>/ [1] [largura]      (uma imagem por página)
//
// `páginas` é opcional ("3,7,12"): sem ela, entram todas. Com a saída terminada em "/", grava
// pagina_001.png, pagina_002.png… na pasta, uma por página, na largura pedida. Usa o PDFKit do macOS, porque o
// computador do projeto não tem pdftoppm nem ImageMagick.
import AppKit
import PDFKit

let a = CommandLine.arguments
guard a.count >= 3, let doc = PDFDocument(url: URL(fileURLWithPath: a[1])) else {
    print("uso: swift folha_contato.swift <deck.pdf> <saida.png> [colunas] [largura] [páginas]"); exit(1)
}
if a[2].hasSuffix("/") {
    let tw = CGFloat(a.count > 4 ? Double(a[4])! : 1400)
    try? FileManager.default.createDirectory(atPath: a[2], withIntermediateDirectories: true)
    for p in 0..<doc.pageCount {
        let pg = doc.page(at: p)!
        let cx = pg.bounds(for: .mediaBox)
        let th = tw * cx.height / cx.width
        let img = pg.thumbnail(of: NSSize(width: tw, height: th), for: .mediaBox)
        let r = NSBitmapImageRep(data: img.tiffRepresentation!)!
        try! r.representation(using: .png, properties: [:])!.write(to: URL(fileURLWithPath: a[2] + String(format: "pagina_%03d.png", p + 1)))
    }
    print("\(a[2]): \(doc.pageCount) páginas")
    exit(0)
}
let cols = a.count > 3 ? Int(a[3])! : 8
let tw = CGFloat(a.count > 4 ? Double(a[4])! : 260)
let pags = a.count > 5 ? a[5].split(separator: ",").map { Int($0)! - 1 } : Array(0..<doc.pageCount)
let caixa = doc.page(at: 0)!.bounds(for: .mediaBox)
let th = tw * caixa.height / caixa.width
let linhas = (pags.count + cols - 1) / cols
let W = Int(CGFloat(cols) * (tw + 8) + 8), H = Int(CGFloat(linhas) * (th + 24) + 8)
let rep = NSBitmapImageRep(bitmapDataPlanes: nil, pixelsWide: W, pixelsHigh: H, bitsPerSample: 8,
                           samplesPerPixel: 4, hasAlpha: true, isPlanar: false, colorSpaceName: .deviceRGB,
                           bytesPerRow: 0, bitsPerPixel: 0)!
NSGraphicsContext.saveGraphicsState()
NSGraphicsContext.current = NSGraphicsContext(bitmapImageRep: rep)
NSColor(white: 0.8, alpha: 1).setFill()
NSRect(x: 0, y: 0, width: W, height: H).fill()
for (k, p) in pags.enumerated() {
    let x = 8 + CGFloat(k % cols) * (tw + 8)
    let y = CGFloat(H) - CGFloat(k / cols + 1) * (th + 24)
    doc.page(at: p)!.thumbnail(of: NSSize(width: tw, height: th), for: .mediaBox)
        .draw(in: NSRect(x: x, y: y, width: tw, height: th))
    ("\(p + 1)" as NSString).draw(at: NSPoint(x: x, y: y + th + 3),
        withAttributes: [.font: NSFont.boldSystemFont(ofSize: 13), .foregroundColor: NSColor.black])
}
NSGraphicsContext.restoreGraphicsState()
try! rep.representation(using: .png, properties: [:])!.write(to: URL(fileURLWithPath: a[2]))
print("\(a[2]): \(pags.count) páginas")
