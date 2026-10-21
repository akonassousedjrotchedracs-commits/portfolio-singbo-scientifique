from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    HRFlowable,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


OUTPUT = "portfolio_summary.pdf"
NAVY = colors.HexColor("#173B53")
TEAL = colors.HexColor("#078A95")
PALE = colors.HexColor("#EDF4F6")
INK = colors.HexColor("#253744")
MUTED = colors.HexColor("#5C6D77")
LINE = colors.HexColor("#D5E0E4")

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="Name", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=25, leading=29, textColor=NAVY, alignment=TA_LEFT, spaceAfter=5))
styles.add(ParagraphStyle(name="Subtitle", parent=styles["Normal"], fontName="Helvetica", fontSize=11, leading=15, textColor=MUTED, spaceAfter=12))
styles.add(ParagraphStyle(name="Section", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=15, leading=18, textColor=NAVY, spaceBefore=9, spaceAfter=7, keepWithNext=True))
styles.add(ParagraphStyle(name="Subsection", parent=styles["Heading3"], fontName="Helvetica-Bold", fontSize=10.5, leading=13, textColor=TEAL, spaceBefore=4, spaceAfter=4, keepWithNext=True))
styles.add(ParagraphStyle(name="Body2", parent=styles["BodyText"], fontName="Helvetica", fontSize=9.2, leading=13, textColor=INK, spaceAfter=6))
styles.add(ParagraphStyle(name="Small2", parent=styles["BodyText"], fontName="Helvetica", fontSize=8, leading=10.5, textColor=MUTED, spaceAfter=4))
styles.add(ParagraphStyle(name="Cell", parent=styles["BodyText"], fontName="Helvetica", fontSize=8.2, leading=10.5, textColor=INK))
styles.add(ParagraphStyle(name="CellBold", parent=styles["Cell"], fontName="Helvetica-Bold", textColor=NAVY))
styles.add(ParagraphStyle(name="Callout", parent=styles["BodyText"], fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=NAVY, backColor=PALE, borderColor=LINE, borderWidth=0.6, borderPadding=8, spaceBefore=3, spaceAfter=8))


def P(text, style="Body2"):
    return Paragraph(text, styles[style])


def table(rows, widths, header=True):
    converted = []
    for row_index, row in enumerate(rows):
        converted.append([P(value, "CellBold" if header and row_index == 0 else "Cell") for value in row])
    result = Table(converted, colWidths=widths, repeatRows=1 if header else 0, hAlign="LEFT")
    commands = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("GRID", (0, 0), (-1, -1), 0.4, LINE),
    ]
    if header:
        commands.extend([("BACKGROUND", (0, 0), (-1, 0), PALE), ("LINEBELOW", (0, 0), (-1, 0), 1, TEAL)])
    for row_index in range(1 if header else 0, len(rows)):
        if (row_index if header else row_index) % 2 == 0:
            commands.append(("BACKGROUND", (0, row_index), (-1, row_index), colors.HexColor("#F8FAFB")))
    result.setStyle(TableStyle(commands))
    return result


def decorate(canvas, doc):
    canvas.saveState()
    width, height = letter
    left = 0.62 * inch
    right = width - 0.62 * inch
    canvas.setStrokeColor(TEAL)
    canvas.setLineWidth(1.1)
    canvas.line(left, height - 0.42 * inch, right, height - 0.42 * inch)
    canvas.setFont("Helvetica-Bold", 7.2)
    canvas.setFillColor(NAVY)
    canvas.drawString(left, height - 0.32 * inch, "AKONASSOU SEDJRO TCHÉDRAC SINGBO")
    canvas.setFont("Helvetica", 7.2)
    canvas.setFillColor(MUTED)
    canvas.drawRightString(right, height - 0.32 * inch, "SCIENTIFIC PORTFOLIO")
    canvas.setStrokeColor(LINE)
    canvas.line(left, 0.42 * inch, right, 0.42 * inch)
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(MUTED)
    canvas.drawString(left, 0.27 * inch, "Medical Biotechnology · Laboratory practice · Biomedical data")
    canvas.drawRightString(right, 0.27 * inch, str(doc.page))
    canvas.restoreState()


doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=letter,
    rightMargin=0.62 * inch,
    leftMargin=0.62 * inch,
    topMargin=0.63 * inch,
    bottomMargin=0.62 * inch,
    title="Scientific Portfolio — Akonassou Sedjro Tchédrac Singbo",
    author="Akonassou Sedjro Tchédrac Singbo",
    subject="Scientific portfolio summary and thesis evidence",
)

story = []

story.extend([
    P("SCIENTIFIC PORTFOLIO", "Small2"),
    P("AKONASSOU SEDJRO<br/>TCHÉDRAC SINGBO", "Name"),
    P("Medical Biotechnology · Laboratory practice · Biomedical data", "Subtitle"),
    HRFlowable(width="100%", thickness=1, color=LINE, spaceAfter=10),
    P("Profile", "Section"),
    P("Biomedical laboratory professional in Cotonou, Benin. The portfolio brings together reported laboratory experience, an undergraduate thesis, and reproducible technical demonstrations on clearly labelled synthetic data. The technical projects are not clinical results and are not presented as hospital work.", "Body2"),
    P("Education and thesis", "Section"),
    P("Medical Biotechnology programme, École Nationale Supérieure des Biosciences et Biotechnologies Appliquées (ENSBBA–UNSTIM), Benin. The supplied thesis cover identifies a professional-degree thesis and records a defence on 23 July 2024. The issued diploma itself was not supplied.", "Body2"),
    P("Contact: akonassousedjrotchedracs@gmail.com · Cotonou, Benin", "Small2"),
    P("Professional experience", "Section"),
    table([
        ["Period", "Experience reported in the portfolio material"],
        ["Since Jul 2026", "Biomedical laboratory activity · CHU de la Mère et de l’Enfant (CHU-MEL), Cotonou. The exact job title is not stated here."],
        ["Jun–Sep 2025", "Medical laboratory internship · CHUD Ouémé-Plateau, Porto-Novo."],
        ["Mar–Jun 2024", "Thesis work · CHUD Ouémé-Plateau; the thesis documents the study and its laboratory analyses."],
        ["Jul–Aug 2023", "Academic internship · Centre de Santé d’Adjarra."],
    ], [1.18 * inch, 5.5 * inch]),
    Spacer(1, 5),
    P("Experience dates and descriptions above are carried over from the supplied portfolio material; employment certificates were not included for independent verification. The official CHU-MEL job title remains to be confirmed.", "Small2"),
    PageBreak(),
    P("TECHNICAL PORTFOLIO", "Small2"),
    P("Reproducible demonstrations", "Name"),
    P("Projects 01–04 use synthetic datasets. Each project includes source files and scripts; its outputs illustrate computation and data checks, not clinical or surveillance findings.", "Body2"),
    table([
        ["Project", "Scope and evidence", "Status"],
        ["01 · Antimicrobial resistance", "100 synthetic observations; 10 organism–antibiotic pairs, 10 observations each. S/I/R categories remain separate; R proportions use S+I+R as denominator.", "Synthetic demonstration"],
        ["02 · Sequence quality control", "Three synthetic FASTA sequences (191 bases total; 8 ambiguous bases) and three short synthetic FASTQ reads. Reports sequence/read quality indicators and exploratory ORFs.", "Synthetic demonstration"],
        ["03 · SQL and ETL", "191 source rows; 191 curated rows, 6 groups and no anomalies in the main fixture. A separate five-row test fixture checks missing, invalid and duplicate records.", "Synthetic demonstration"],
        ["04 · Statistical analysis", "300 synthetic records in six groups (n=50 each). Reports resistance proportions and 95% Wilson intervals; denominator is valid S+I+R results.", "Synthetic demonstration"],
    ], [1.45 * inch, 4.25 * inch, 0.98 * inch]),
    P("Skills demonstrated by the repository", "Section"),
    P("Standard-library Python for CSV/JSON processing and validation; FASTA/FASTQ parsing and basic quality metrics; SQL and SQLite relational constraints/aggregations; descriptive proportions and Wilson intervals; SHA-256 file fingerprinting; SVG chart generation; and static HTML/CSS project pages.", "Body2"),
    P("Tools not demonstrated in delivered project code", "Subsection"),
    P("No operational Power BI dashboard or .pbix file is included. The project scripts do not demonstrate pandas, Biopython or Matplotlib. Hospital practice and the technical portfolio are kept distinct.", "Body2"),
    P("Open project pages", "Section"),
    P("01 · project_01_antimicrobial_resistance &nbsp;&nbsp; 02 · project_02_bacterial_sequence<br/>03 · project_03_sql_advanced &nbsp;&nbsp; 04 · project_04_advanced_biomedical_analysis<br/>05 · project_05_memoire_soutenance_prostate", "Small2"),
    PageBreak(),
    P("THESIS SUMMARY", "Small2"),
    P("Evaluation of inflammation in prostatic dysfunction", "Name"),
    P("Thesis title translated from the supplied French document · CHUD-OP · defence: 23 July 2024", "Subtitle"),
    P("Study description reported in the thesis", "Section"),
    P("The document describes 81 men aged 40 years or older: 61 retrospective records (1 January 2023–20 March 2024) and 20 prospective participants recruited from dialysis care (25 March–22 June 2024). The assessed markers were total PSA, C-reactive protein (CRP) and complete blood count (CBC/NFS), including leucocytes, neutrophils and lymphocytes. No cytokine assay is reported; cytokines appear only in the literature discussion.", "Body2"),
    P("The thesis reports means ± standard error of the mean, Mann–Whitney comparisons and a 5% significance threshold. The underlying individual-level dataset and source tables were not supplied, so the analysis cannot be independently reproduced.", "Body2"),
    P("Aggregate results as stated in the thesis", "Section"),
    table([
        ["Marker", "Normal PSA (n=69)", "Elevated PSA (n=12)", "Reported comparison"],
        ["Leucocytes (G/L)", "5.39 ± 0.46", "5.61 ± 0.92", "Not significant"],
        ["Neutrophils (G/L)", "2.73 ± 0.25", "2.94 ± 0.67", "Not significant"],
        ["Lymphocytes (G/L)", "1.87 ± 0.09", "2.12 ± 0.17", "p < 0.05"],
        ["CRP (mg/L)", "4.61 ± 0.63", "4.48 ± 1.50", "Not significant"],
    ], [1.35 * inch, 1.45 * inch, 1.45 * inch, 2.43 * inch]),
    Spacer(1, 8),
    P("Interpretation and limits", "Section"),
    P("These are values and significance labels reported by the thesis, not recalculated results. Exact p-values, confidence intervals, correlation outputs and individual distributions are unavailable. The reported association between PSA group and lymphocyte count does not establish an inflammatory mechanism or causality. No academic mark or honours classification is included because the supplied source does not document one.", "Callout"),
])

doc.build(story, onFirstPage=decorate, onLaterPages=decorate)
