import io

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas

from .models import ResourceMetric


def build_resource_metric_pdf(queryset, title='Resource Metrics Report'):
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    pdf.setTitle(title)

    pdf.setFont('Helvetica-Bold', 14)
    pdf.drawString(2 * cm, height - 2 * cm, title)

    y = height - 3 * cm
    pdf.setFont('Helvetica', 10)
    headers = ['Country', 'Type', 'Metric', 'Value', 'Unit', 'Year']
    pdf.drawString(2 * cm, y, ' | '.join(headers))
    y -= 0.8 * cm

    for metric in queryset[:40]:
        row = [
            metric.country.iso3,
            metric.resource_type,
            metric.metric,
            f"{metric.value}",
            metric.unit,
            str(metric.year or ''),
        ]
        pdf.drawString(2 * cm, y, ' | '.join(row))
        y -= 0.6 * cm
        if y < 2 * cm:
            pdf.showPage()
            y = height - 2 * cm

    pdf.showPage()
    pdf.save()
    buffer.seek(0)
    return buffer
