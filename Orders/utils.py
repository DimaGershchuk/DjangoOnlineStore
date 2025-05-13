import io
from reportlab.pdfgen import canvas


def generate_pdf_order(order):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)

    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, 800, f"Order Confirmation — #{order.pk}")

    # Дані користувача
    p.setFont("Helvetica", 12)
    p.drawString(50, 770, f"Customer: {order.user.username} ({order.user.email})")
    p.drawString(50, 750, f"Date: {order.created_at}")

    y = 720

    for item in order.items.all():
        line = f"{item.product.name} x {item.quantity} ${item.price}"
        p.drawString(50, y, line)
        y -= 20

    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y - 10, f"TOTAL: ${order.total_price:.2f}")

    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer.read()

