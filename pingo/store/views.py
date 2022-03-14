from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
from store.models import Order, PingoOrder, OrderItem
from core.charts import objects_to_csv
import datetime
import tempfile
import logging

logger = logging.getLogger("error_logger")


def download_csv(request, supplier_id, ordered_at__gte, ordered_at__lte):
    if supplier_id > 0:
        csv_file = objects_to_csv(OrderItem, exclude_fields=["type"],
                                  order__supplier_id=supplier_id,
                                  ordered_at__gte=ordered_at__gte,
                                  ordered_at__lte=ordered_at__lte,
                                  order__status__in=["PROCESSING", "DELIVERING", "FINISHED"])
    else:
        csv_file = objects_to_csv(OrderItem, exclude_fields=["type"])

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="orderitems.csv"'

    response.write(csv_file.encode('utf_8_sig'))
    return response

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
