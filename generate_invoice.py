from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


def create_invoice():

    output_dir = Path("data/input")
    output_dir.mkdir(parents=True, exist_ok=True)

    pdf_path = output_dir / "sample.pdf"

    doc = SimpleDocTemplate(str(pdf_path))

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph(
            "<font size=22><b>ABC Office Supplies Pvt. Ltd.</b></font>",
            styles["Title"],
        )
    )

    elements.append(
        Paragraph(
            "123 Business Park, Chennai, Tamil Nadu 600001",
            styles["Normal"],
        )
    )

    elements.append(Spacer(1, 0.25 * inch))

    elements.append(
        Paragraph("<b>Invoice No:</b> INV-2026-001", styles["Normal"])
    )

    elements.append(
        Paragraph("<b>Invoice Date:</b> 25-Jul-2026", styles["Normal"])
    )

    elements.append(
        Paragraph("<b>Due Date:</b> 08-Aug-2026", styles["Normal"])
    )

    elements.append(Spacer(1, 0.2 * inch))

    elements.append(Paragraph("<b>Bill To</b>", styles["Heading2"]))

    elements.append(
        Paragraph(
            "XYZ Technologies Pvt. Ltd.<br/>"
            "45 IT Expressway<br/>"
            "Bengaluru, Karnataka 560100",
            styles["Normal"],
        )
    )

    elements.append(Spacer(1, 0.25 * inch))

    data = [
        ["Item", "Qty", "Unit Price", "Amount"],
        ["Laptop Stand", "2", "1500", "3000"],
        ["Wireless Mouse", "5", "800", "4000"],
        ["Keyboard", "3", "1200", "3600"],
        ["", "", "Subtotal", "10600"],
        ["", "", "GST (18%)", "1908"],
        ["", "", "Total", "12508"],
    ]

    table = Table(
        data,
        colWidths=[3 * inch, 0.8 * inch, 1.3 * inch, 1.3 * inch],
    )

    table.setStyle(
        TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("ALIGN", (1, 1), (-1, -1), "CENTER"),
                ("BACKGROUND", (-2, -3), (-1, -1), colors.whitesmoke),
            ]
        )
    )

    elements.append(table)

    elements.append(Spacer(1, 0.25 * inch))

    elements.append(
        Paragraph(
            "<b>Payment Terms:</b> Net 14 Days",
            styles["Normal"],
        )
    )

    elements.append(
        Paragraph(
            "Thank you for your business!",
            styles["Normal"],
        )
    )

    doc.build(elements)

    print("=" * 60)
    print("Invoice PDF created successfully!")
    print(f"Location : {pdf_path.resolve()}")
    print("=" * 60)


if __name__ == "__main__":
    create_invoice()