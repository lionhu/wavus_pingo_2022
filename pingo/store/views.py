from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
from store.models import Order, PingoOrder
import datetime
import tempfile
import logging

logger = logging.getLogger("error_logger")


def HelloPDFView(request, order_type, slug):
    if order_type == "regular":
        template_name = 'pdfs/order_invoice.html'
        order = Order.objects.get(slug=slug)
    else:
        template_name = "pdfs/test/letter.html"
        order = PingoOrder.objects.get(slug=slug)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "inline;attachment;filename=Expenses" + str(datetime.datetime.now()) + '.pdf'
    response["Content-Transfer-Encoding"] = "binary"

    html_string = render_to_string(template_name, {
        "order": order
    })

    result = HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(
        stylesheets=[
            CSS('staticfiles/css/invoice_pdf.css'),
        ])

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, "rb")
        response.write(output.read())

    return response
