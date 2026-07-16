from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    KeepTogether, ListFlowable, ListItem
)
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "pdf" / "Nota_Latihan_MPE_Hub.pdf"
OUT.parent.mkdir(parents=True, exist_ok=True)

for name, path in {
    "Inter": "/System/Library/Fonts/Supplemental/Arial.ttf",
    "Inter-Bold": "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "Inter-Italic": "/System/Library/Fonts/Supplemental/Arial Italic.ttf",
}.items():
    if Path(path).exists():
        pdfmetrics.registerFont(TTFont(name, path))

NAVY = colors.HexColor("#17324D")
BLUE = colors.HexColor("#1976D2")
SKY = colors.HexColor("#EAF4FF")
YELLOW = colors.HexColor("#F4C542")
GREEN = colors.HexColor("#208A63")
INK = colors.HexColor("#17212B")
MUTED = colors.HexColor("#5B6874")
LIGHT = colors.HexColor("#F4F7FA")
RULE = colors.HexColor("#D5DEE7")

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="CoverKicker", fontName="Helvetica-Bold", fontSize=10, leading=14, textColor=BLUE, spaceAfter=12))
styles.add(ParagraphStyle(name="CoverTitle", fontName="Helvetica-Bold", fontSize=28, leading=33, textColor=NAVY, spaceAfter=16))
styles.add(ParagraphStyle(name="CoverSub", fontName="Helvetica", fontSize=13, leading=19, textColor=MUTED, spaceAfter=8))
styles.add(ParagraphStyle(name="H1x", fontName="Helvetica-Bold", fontSize=20, leading=25, textColor=NAVY, spaceBefore=6, spaceAfter=12))
styles.add(ParagraphStyle(name="H2x", fontName="Helvetica-Bold", fontSize=13, leading=18, textColor=BLUE, spaceBefore=10, spaceAfter=6))
styles.add(ParagraphStyle(name="Bodyx", fontName="Helvetica", fontSize=9.5, leading=14.5, textColor=INK, spaceAfter=7))
styles.add(ParagraphStyle(name="Smallx", fontName="Helvetica", fontSize=8, leading=11.5, textColor=MUTED, spaceAfter=4))
styles.add(ParagraphStyle(name="Callout", fontName="Helvetica-Bold", fontSize=10, leading=15, textColor=NAVY, backColor=SKY, borderColor=colors.HexColor("#B9DCF8"), borderWidth=0.7, borderPadding=9, spaceBefore=7, spaceAfter=9))
styles.add(ParagraphStyle(name="Codex", fontName="Courier", fontSize=7.8, leading=11, textColor=colors.HexColor("#DDEBFA"), backColor=colors.HexColor("#10283F"), borderPadding=8, spaceAfter=8))
styles.add(ParagraphStyle(name="TableHead", fontName="Helvetica-Bold", fontSize=8, leading=10, textColor=colors.white, alignment=TA_LEFT))
styles.add(ParagraphStyle(name="TableCell", fontName="Helvetica", fontSize=7.7, leading=10.5, textColor=INK))

def P(text, style="Bodyx"):
    return Paragraph(text, styles[style])

def bullets(items):
    return ListFlowable(
        [ListItem(P(x), leftIndent=12) for x in items],
        bulletType="bullet", start="circle", leftIndent=18, bulletFontName="Helvetica", bulletFontSize=7,
        bulletColor=BLUE, spaceAfter=6
    )

def numbered(items):
    return ListFlowable(
        [ListItem(P(x), leftIndent=15) for x in items],
        bulletType="1", leftIndent=22, bulletFontName="Helvetica-Bold", bulletFontSize=8,
        bulletColor=BLUE, spaceAfter=6
    )

def table(rows, widths):
    data=[]
    for ri,row in enumerate(rows):
        data.append([P(str(x), "TableHead" if ri == 0 else "TableCell") for x in row])
    t=Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),NAVY), ("TEXTCOLOR",(0,0),(-1,0),colors.white),
        ("GRID",(0,0),(-1,-1),0.45,RULE), ("VALIGN",(0,0),(-1,-1),"TOP"),
        ("LEFTPADDING",(0,0),(-1,-1),6), ("RIGHTPADDING",(0,0),(-1,-1),6),
        ("TOPPADDING",(0,0),(-1,-1),5), ("BOTTOMPADDING",(0,0),(-1,-1),5),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white,LIGHT]),
    ]))
    return t

def chapter(title, lead):
    return [P(title,"H1x"), P(lead,"Callout")]

def header_footer(canvas, doc):
    canvas.saveState()
    if doc.page > 1:
        canvas.setStrokeColor(RULE); canvas.setLineWidth(0.5)
        canvas.line(18*mm, 17*mm, 192*mm, 17*mm)
        canvas.setFont("Helvetica", 7); canvas.setFillColor(MUTED)
        canvas.drawString(18*mm, 10*mm, "MPE Hub · Nota Latihan Transformasi Digital Makmal MPE")
        canvas.drawRightString(192*mm, 10*mm, f"{doc.page}")
    canvas.restoreState()

doc = SimpleDocTemplate(str(OUT), pagesize=A4, rightMargin=18*mm, leftMargin=18*mm,
                        topMargin=17*mm, bottomMargin=21*mm,
                        title="Nota Latihan MPE Hub", author="Prof. Madya Dr. Mohd Murtadha Mohamad")
story=[]

story += [Spacer(1,20*mm), P("BENGKEL TRANSFORMASI DIGITAL · 28–29 JULAI 2026","CoverKicker"),
          P("MPE Hub<br/>Daripada Idea kepada Aplikasi Web Operasi Makmal","CoverTitle"),
          P("Panduan lengkap membina aplikasi mudah alih untuk Buku Log Makmal, KEW.PA-9 dan MCCB Test Report; menyimpan data di Google Drive; serta menerbitkannya melalui GitHub Pages.","CoverSub"),
          Spacer(1,10*mm)]
cover=Table([[P("PENCERAMAH / FASILITATOR","Smallx"),P("SLOT LATIHAN","Smallx")],
             [P("<b>Prof. Madya Dr. Mohd Murtadha Mohamad</b>","Bodyx"),P("Kajian kes praktikal merentas Modul 1–5","Bodyx")],
             [P("Fakulti Komputeran, Universiti Teknologi Malaysia","Smallx"),P("Makmal Energy Efficiency, CREaTE JKR, Alor Gajah","Smallx")]],
            colWidths=[82*mm,82*mm])
cover.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),LIGHT),("BOX",(0,0),(-1,-1),0.7,RULE),
                           ("INNERGRID",(0,0),(-1,-1),0.4,RULE),("VALIGN",(0,0),(-1,-1),"TOP"),
                           ("LEFTPADDING",(0,0),(-1,-1),10),("RIGHTPADDING",(0,0),(-1,-1),10),
                           ("TOPPADDING",(0,0),(-1,-1),8),("BOTTOMPADDING",(0,0),(-1,-1),8)]))
story += [cover, Spacer(1,14*mm), P("HASIL AKHIR","CoverKicker"),
          P("Satu sistem web responsif, satu storan berpusat, tiga modul operasi dan satu dokumentasi yang boleh diguna semula.","CoverSub"), PageBreak()]

story += chapter("1. Kedudukan dalam Bengkel", "MPE Hub ialah kajian kes menyeluruh yang menghubungkan produktiviti, automasi dokumen, analisis rekod teknikal, penambahbaikan aliran kerja serta penyediaan bahan projek.")
story += [table([
    ["Masa / Modul", "Fokus rasmi", "Hubungan dengan MPE Hub"],
    ["28 Jul · 9.00–10.30 · Modul 1", "Pengenalan aplikasi pintar", "Masalah operasi, pengalaman pengguna mudah alih dan demo tiga modul."],
    ["28 Jul · 11.00–1.00 · Modul 2", "Automasi dokumen rasmi", "Pendigitalan Buku Log, KEW.PA-9 dan laporan ujian."],
    ["28 Jul · 2.30–4.30 · Modul 3", "Analisis data & rekod teknikal", "Skema Google Sheets, ringkasan dashboard dan kualiti rekod."],
    ["29 Jul · 9.00–10.30 · Modul 3", "Sambungan Modul 3", "Latihan membaca, menyemak dan menjejak rekod."],
    ["29 Jul · 11.00–1.00 · Modul 4", "Automasi aliran kerja", "Apps Script, lampiran Drive, validasi dan maklum balas status."],
    ["29 Jul · 2.30–4.30 · Modul 5", "Dokumen projek & pembentangan", "GitHub Pages, nota PDF, slaid dan dokumentasi web."],
], [31*mm,55*mm,79*mm]), Spacer(1,5*mm), P("Hasil pembelajaran","H2x"), bullets([
    "Memetakan borang dan rekod manual kepada medan data yang konsisten.",
    "Membina antara muka responsif menggunakan HTML, CSS dan JavaScript tanpa proses build.",
    "Menyediakan API ringkas melalui Google Apps Script dan menyimpan data ke Google Sheets/Drive.",
    "Menerbitkan aplikasi dan dokumentasi melalui GitHub Pages serta menilai implikasi akses awam.",
    "Melaksanakan ujian fungsi, pengesahan data dan penyelenggaraan versi."
]), PageBreak()]

story += chapter("2. Gambaran Sistem", "Reka bentuk ini memisahkan antara muka awam daripada storan milik organisasi. GitHub Pages menghantar data kepada Apps Script; Apps Script menulis rekod ke Sheets dan fail ke Drive.")
story += [table([
    ["Lapisan", "Komponen", "Tanggungjawab"],
    ["Paparan", "GitHub Pages", "Dashboard, navigasi tab, borang responsif, validasi asas dan mesej status."],
    ["Logik klien", "app.js + config.js", "Mengumpul medan, mengira nilai MCCB, menukar lampiran kepada Base64 dan memanggil API."],
    ["API", "Google Apps Script", "Menerima GET/POST, mengesahkan modul, menjana ID rekod, mengunci penulisan dan memberi respons JSON."],
    ["Data", "Google Sheets", "Tab logbook, asset dan mccb; satu baris bagi setiap rekod."],
    ["Fail", "Google Drive", "Menyimpan lampiran Buku Log serta menyediakan URL fail."],
], [31*mm,45*mm,89*mm]), Spacer(1,5*mm), P("Aliran data","H2x"),
    P("Pengguna → GitHub Pages → permintaan HTTPS → Apps Script → Google Sheets / Drive → respons JSON → dashboard dikemas kini."),
    P("Prinsip penting: GitHub Pages hanya hos fail statik. Kredensial pemilik Drive tidak pernah diletakkan dalam kod pelayar; Apps Script melaksanakan operasi sebagai pemilik deployment.","Callout"),
    P("Struktur repositori","H2x"), P("README.md · index.html · styles.css · app.js · config.js · apps-script/Code.gs · docs.html · docs.css · downloads/"), PageBreak()]

story += chapter("3. Fasa 1 — Takrif Keperluan", "Mulakan dengan aliran kerja sebenar, bukan dengan kod. Setiap medan mesti mempunyai tujuan, pemilik dan kaedah semakan.")
story += [P("3.1 Tiga modul operasi","H2x"), table([
    ["Modul", "Rekod utama", "Keluaran"],
    ["Buku Log Makmal", "Kehadiran, masa masuk/keluar, aktiviti, pegawai, status, lampiran", "Rekod LOG-YYYYMMDD-HHMMSS"],
    ["KEW.PA-9", "Pemohon, tujuan, tempat, tarikh, status dan senarai aset", "Rekod PA9-YYYYMMDD-HHMMSS"],
    ["MCCB Test Report", "Butiran MCCB, keadaan ujian, arus, trip time, bacaan dan pengesahan", "Rekod TR-YYYYMMDD-HHMMSS"],
], [35*mm,90*mm,40*mm]),
    P("3.2 Soalan reka bentuk","H2x"), bullets([
        "Siapa mengisi, siapa menyemak dan siapa membetulkan rekod?",
        "Medan mana wajib, mana pilihan dan mana dikira secara automatik?",
        "Adakah lampiran mengandungi data sensitif atau maklumat peribadi?",
        "Berapa lama rekod disimpan dan siapa dibenarkan melihatnya?",
        "Apakah definisi Lulus/Gagal serta tindakan susulan?"
    ]), P("Senarai semak siap fasa","H2x"), bullets([
        "Borang sumber dan istilah teknikal disahkan pemilik proses.",
        "Nama medan, jenis data dan peraturan validasi didokumenkan.",
        "Tahap akses awam/dalaman diputuskan sebelum deployment."
    ]), PageBreak()]

story += chapter("4. Fasa 2 — Bina Antara Muka", "Versi pertama sengaja menggunakan HTML, CSS dan JavaScript tulen: mudah diajar, mudah diaudit dan boleh terus dihos di GitHub Pages.")
story += [P("4.1 Kerangka HTML","H2x"), P("index.html menyediakan sidebar/navigation tab, halaman dashboard dan tiga borang. Setiap panel menggunakan pengenal yang stabil supaya JavaScript boleh menukar paparan tanpa memuat semula halaman."),
    P("4.2 Reka bentuk responsif","H2x"), bullets([
        "Gunakan susun atur grid yang bertukar kepada satu lajur pada skrin kecil.",
        "Pastikan sasaran sentuh sekurang-kurangnya sekitar 44 px dan label kekal kelihatan.",
        "Paparkan unit teknikal pada label, contohnya Rated Current (A) dan Short Circuit (kA).",
        "Gunakan warna status secara konsisten dan jangan bergantung pada warna semata-mata."
    ]), P("4.3 Corak navigasi","H2x"), P("Dashboard ialah halaman utama. Tab Buku Log, KEW.PA-9 dan MCCB membuka borang masing-masing. Pautan Dokumentasi Latihan membawa pengguna kepada panduan web."),
    P("Contoh struktur ringkas","H2x"), P("&lt;nav&gt;…&lt;/nav&gt;<br/>&lt;main&gt;<br/>&nbsp;&nbsp;&lt;section id='dashboard'&gt;…&lt;/section&gt;<br/>&nbsp;&nbsp;&lt;section id='logbook'&gt;…&lt;/section&gt;<br/>&lt;/main&gt;","Codex"), PageBreak()]

story += chapter("5. Fasa 3 — Logik Klien", "app.js menghubungkan tindakan pengguna dengan borang, pengiraan dan API. Pastikan setiap kegagalan mempunyai mesej yang boleh difahami.")
story += [P("5.1 Penghantaran rekod","H2x"), numbered([
        "Tangkap acara submit dan hentikan penghantaran HTML biasa.",
        "Semak medan wajib serta format nombor/tarikh.",
        "Bina objek data mengikut modul.",
        "Jika ada lampiran, baca sebagai Base64 dan semak saiz/jenis fail.",
        "POST JSON kepada URL Apps Script dalam config.js.",
        "Paparkan ID rekod apabila berjaya; kekalkan data borang jika gagal."
    ]), P("5.2 MCCB","H2x"), P("Nilai rated-at-test dikira daripada Rated Current × TCD. Arus ujian ialah rated-at-test × 1.05 dan × 1.30. Simpan input mentah dan nilai terbitan supaya audit boleh dibuat."),
    P("5.3 Dashboard","H2x"), P("GET action=dashboard mendapatkan jumlah Buku Log, pinjaman aktif, kadar lulus, tindakan belum selesai dan aktiviti terkini. Jika API tidak tersedia, aplikasi perlu memaparkan keadaan ralat yang jelas."),
    P("Jangan letak kata laluan, token peribadi atau kunci API di config.js. Fail GitHub Pages boleh dibaca oleh sesiapa sahaja.","Callout"), PageBreak()]

story += chapter("6. Fasa 4 — Google Apps Script", "Apps Script ialah lapisan perantara yang mempunyai kuasa menulis ke Drive pemilik deployment. Ia mesti ringkas, berjejak dan dikawal.")
story += [P("6.1 Fungsi utama","H2x"), table([
    ["Fungsi", "Peranan"],
    ["doGet / doPost", "Menerima permintaan dan memulangkan JSON."],
    ["ensureSetup", "Mencipta atau membuka spreadsheet, tiga tab dan folder lampiran."],
    ["saveRecord", "Mengunci penulisan, menjana ID dan menambah satu baris."],
    ["saveAttachment", "Menyahkod Base64, membersihkan nama fail dan menyimpan ke Drive."],
    ["getDashboardSummary", "Mengira metrik serta lima aktiviti terkini."],
    ["getStorageLinks", "Mencetak URL spreadsheet dan folder untuk pentadbir."],
], [48*mm,117*mm]),
    P("6.2 Penyediaan deployment","H2x"), numbered([
        "Buka script.google.com dan cipta projek baharu.",
        "Salin apps-script/Code.gs ke editor.",
        "Pilih Deploy → New deployment → Web app.",
        "Tetapkan Execute as: Me. Pilih tahap akses mengikut polisi organisasi.",
        "Benarkan Sheets dan Drive apabila diminta.",
        "Salin URL /exec ke config.js dan uji action=dashboard."
    ]), PageBreak()]

story += chapter("7. Fasa 5 — Google Sheets & Drive", "Storan yang mudah tidak bermaksud tadbir urus boleh diabaikan. Struktur helaian, pemilikan dan perkongsian perlu disenggara.")
story += [P("7.1 Struktur data","H2x"), bullets([
        "logbook: satu baris bagi satu sesi/aktiviti; lampiran disimpan sebagai URL.",
        "asset: satu baris bagi permohonan; senarai aset disimpan sebagai JSON.",
        "mccb: satu baris bagi laporan; peralatan dan bacaan disimpan sebagai JSON."
    ]), P("7.2 Akses","H2x"), table([
        ["Komponen", "Keadaan lazim", "Cadangan"],
        ["GitHub Pages", "Awam", "Jangan paparkan data rekod atau rahsia dalam kod."],
        ["Apps Script /exec", "Anyone untuk borang awam", "Tambah token aplikasi, allow-list/domain atau identiti Workspace jika risiko lebih tinggi."],
        ["Google Sheets", "Private kepada pemilik/editor", "Kongsi hanya dengan petugas yang memerlukan."],
        ["Folder Drive", "Private kepada pemilik/editor", "Semak polisi lampiran dan tempoh simpanan."],
    ], [38*mm,54*mm,73*mm]),
    P("7.3 Sandaran","H2x"), P("Eksport berkala helaian kepada XLSX/CSV, gunakan sejarah versi Drive, rekodkan pemilik sistem dan simpan salinan kod Apps Script dalam repositori."), PageBreak()]

story += chapter("8. Fasa 6 — GitHub & GitHub Pages", "Repositori ialah rekod versi aplikasi dan dokumentasi. GitHub Pages menerbitkan kandungan statik terus daripada cawangan main.")
story += [P("8.1 Terbit kali pertama","H2x"), P("git init<br/>git add .<br/>git commit -m 'initial MPE Hub'<br/>gh repo create mpe-hub --public --source=. --push<br/>gh api -X POST repos/OWNER/mpe-hub/pages -f source[branch]=main -f source[path]=/","Codex"),
    P("8.2 Kemas kini","H2x"), P("git status<br/>git add index.html styles.css app.js docs.html downloads/<br/>git commit -m 'add training documentation'<br/>git push origin main","Codex"),
    P("8.3 Pautan hasil","H2x"), bullets([
        "Aplikasi: https://drmurtadha.github.io/mpe-hub/",
        "Dokumentasi: https://drmurtadha.github.io/mpe-hub/docs.html",
        "Repositori: https://github.com/drMurtadha/mpe-hub"
    ]), P("GitHub Pages bagi repositori awam boleh dilihat oleh sesiapa sahaja yang mengetahui URL, dan boleh diindeks enjin carian. Kawalan data mesti dibuat pada API/storan, bukan pada anggapan bahawa URL sukar ditemui.","Callout"), PageBreak()]

story += chapter("9. Ujian & Penerimaan", "Ujian perlu membuktikan tiga perkara: borang boleh digunakan di telefon, data sampai dengan tepat, dan kegagalan tidak menyebabkan pengguna kehilangan konteks.")
story += [table([
    ["ID", "Senario", "Hasil dijangka"],
    ["T01", "Buka pada telefon", "Tiada skrol mendatar; navigasi dan butang mudah disentuh."],
    ["T02", "Hantar Buku Log lengkap", "ID LOG dipaparkan; baris dan lampiran wujud."],
    ["T03", "Hantar KEW.PA-9 dengan beberapa aset", "ID PA9 dipaparkan; items JSON lengkap."],
    ["T04", "Masukkan data MCCB", "Nilai 1.05/1.30 betul; keputusan disimpan."],
    ["T05", "Putuskan rangkaian", "Mesej gagal jelas; pengguna boleh cuba semula."],
    ["T06", "Muat semula dashboard", "Metrik sepadan dengan helaian sumber."],
    ["T07", "Fail terlalu besar/jenis tidak sah", "Lampiran ditolak sebelum dihantar."],
    ["T08", "Input berniat jahat", "Nama fail dibersihkan; formula/HTML tidak dilaksanakan."],
], [15*mm,67*mm,83*mm]), P("Kriteria siap","H2x"), bullets([
    "Semua senario kritikal lulus pada sekurang-kurangnya satu telefon Android/iOS dan satu desktop.",
    "Pemilik proses mengesahkan medan serta pengiraan MCCB.",
    "Tahap akses dan pemilikan Drive direkodkan.",
    "Pautan produksi, repositori dan dokumentasi diserahkan kepada pentadbir."
]), PageBreak()]

story += chapter("10. Keselamatan & Privasi", "Versi semasa sesuai sebagai demonstrasi/operasi terkawal. Untuk penggunaan organisasi, perlindungan API perlu diperkukuh sebelum menerima data sensitif.")
story += [P("Risiko utama","H2x"), table([
    ["Risiko", "Kesan", "Mitigasi"],
    ["Endpoint Anyone", "Orang luar boleh menghantar rekod", "Identity Workspace, token sementara, allow-list atau backend berautentikasi."],
    ["Spam/automasi", "Helaian dipenuhi rekod", "Rate limit, CAPTCHA, kuota dan log audit."],
    ["Lampiran", "Fail berbahaya/terlalu besar", "Had MIME/saiz, pengimbasan dan folder kuarantin."],
    ["Data peribadi", "Pendedahan identiti pekerja", "Minimumkan medan, hadkan perkongsian, polisi retensi."],
    ["Pemilik tunggal", "Risiko kesinambungan", "Gunakan akaun fungsi/Shared Drive dan sekurang-kurangnya dua pentadbir."],
], [34*mm,52*mm,79*mm]),
    P("Keputusan akses yang disyorkan","H2x"), P("Jika peserta hanya warga JKR/Google Workspace, gunakan deployment yang terhad kepada domain. Jika aplikasi mesti awam, jangan terima data sensitif sehingga lapisan pengesahan dan pencegahan penyalahgunaan disediakan."), PageBreak()]

story += chapter("11. Operasi & Penyelesaian Masalah", "Dokumentasi operasi perlu membolehkan petugas lain mengesan punca tanpa mengubah data secara sembarangan.")
story += [table([
    ["Gejala", "Semakan", "Tindakan"],
    ["Dashboard offline", "URL /exec, status deployment, console rangkaian", "Pastikan URL betul dan deployment aktif."],
    ["Data tidak muncul", "Execution log Apps Script, tab dan header", "Semak kuota, kebenaran dan nama helaian."],
    ["Lampiran gagal", "Saiz/jenis fail, kuota Drive", "Kecilkan fail dan semak akses folder."],
    ["Perubahan kod belum kelihatan", "Commit terkini dan Pages build", "Tunggu deployment; hard refresh/cache clear."],
    ["CORS/redirect", "Respons /exec dan kaedah POST", "Gunakan deployment URL terkini; elakkan URL /dev."],
    ["ID bertindih", "Penghantaran dalam saat sama", "Tambah UUID jika volum meningkat."],
], [40*mm,58*mm,67*mm]), P("Rutin bulanan","H2x"), bullets([
    "Semak kuota Drive/Sheets dan rekod gagal.",
    "Semak pengguna yang mempunyai akses editor.",
    "Eksport sandaran dan uji pemulihan sampel.",
    "Kemas kini dokumentasi apabila medan atau polisi berubah."
]), PageBreak()]

story += chapter("12. Latihan Amali", "Peserta membina kefahaman melalui satu rekod bagi setiap modul, satu semakan data dan satu perubahan kecil yang diterbitkan.")
story += [table([
    ["Masa", "Aktiviti", "Bukti"],
    ["15 min", "Kenal pasti medan dan risiko bagi satu borang", "Peta medan ringkas."],
    ["20 min", "Isi Buku Log, KEW.PA-9 dan MCCB", "Tiga ID rekod."],
    ["15 min", "Semak helaian, lampiran dan dashboard", "Padanan data disahkan."],
    ["20 min", "Ubah teks/validasi kecil dan commit", "Commit GitHub."],
    ["10 min", "Semak Pages dan dokumentasi", "Pautan boleh dicapai."],
], [25*mm,80*mm,60*mm]), P("Soalan refleksi","H2x"), numbered([
    "Medan mana boleh dikira automatik dan medan mana mesti disahkan manusia?",
    "Apakah data yang tidak patut dihantar melalui aplikasi awam?",
    "Bagaimana rekod salah dibetulkan tanpa memadam jejak audit?",
    "Siapa pemilik sistem selepas latihan dan bagaimana akses dipindahkan?"
]), PageBreak()]

story += chapter("13. Checklist Serahan", "Gunakan halaman ini sebagai senarai semak sebelum sistem diserahkan kepada pemilik operasi.")
story += [bullets([
    "☐ URL aplikasi GitHub Pages direkodkan dan diuji.",
    "☐ URL dokumentasi serta fail nota/slaid boleh dimuat turun.",
    "☐ Repositori mempunyai README, sejarah commit dan pemilik yang jelas.",
    "☐ Deployment Apps Script menggunakan versi terkini.",
    "☐ Spreadsheet dan folder Drive dimiliki akaun yang sesuai.",
    "☐ Tiga rekod ujian berjaya dan boleh dijejaki melalui ID.",
    "☐ Polisi akses, retensi, sandaran dan pemulihan dipersetujui.",
    "☐ Pentadbir kedua memahami cara deploy semula dan semak log."
]), P("Rujukan sistem","H2x"), table([
    ["Sumber", "Lokasi"],
    ["Aplikasi", "https://drmurtadha.github.io/mpe-hub/"],
    ["Dokumentasi web", "https://drmurtadha.github.io/mpe-hub/docs.html"],
    ["Repositori", "https://github.com/drMurtadha/mpe-hub"],
    ["Kod backend", "apps-script/Code.gs"],
    ["Konfigurasi endpoint", "config.js"],
], [43*mm,122*mm]), Spacer(1,5*mm), P("Sumber rasmi latihan","H2x"), P("Surat lantikan penceramah/fasilitator dan Lampiran A bagi Bengkel Transformasi Digital dan Pemerkasaan Operasi Pintar Makmal Penyelidikan Elektrik (MPE), CREaTE JKR, 28–29 Julai 2026. Kandungan nota ini disusun sebagai kajian kes praktikal yang melengkapi lima modul dalam atur cara tersebut.","Smallx"),
    Spacer(1,10*mm), P("Penutup","H1x"), P("MPE Hub menunjukkan bahawa transformasi digital bukan sekadar menukar borang kertas kepada skrin. Nilai sebenar datang daripada data yang konsisten, aliran kerja yang boleh dijejaki, kawalan akses yang betul dan dokumentasi yang membolehkan sistem diselenggara oleh pasukan.","Callout")]

doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
print(OUT)
