from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

REPORT_FOLDER = "reports"

if not os.path.exists(REPORT_FOLDER):
    os.makedirs(REPORT_FOLDER)


def generate_report(servers):

    filename = os.path.join(REPORT_FOLDER, "Monitoring_Report.pdf")

    c = canvas.Canvas(filename, pagesize=letter)

    width, height = letter

    y = height - 50

    c.setFont("Helvetica-Bold", 18)
    c.drawString(150, y, "Infrastructure Monitoring Report")

    y -= 40

    c.setFont("Helvetica", 12)

    for server in servers:

        c.drawString(50, y, f"Server : {server['server']}")
        y -= 20

        c.drawString(70, y, f"Status : {server['status']}")
        y -= 20

        if server["status"] == "ONLINE":

            c.drawString(70, y, f"Hostname : {server['data']['hostname']}")
            y -= 20

            c.drawString(70, y, f"IP : {server['data']['ip']}")
            y -= 20

            c.drawString(70, y, f"CPU : {server['data']['cpu']} %")
            y -= 20

            c.drawString(70, y, f"Memory : {server['data']['memory']} %")
            y -= 20

            c.drawString(70, y, f"Disk : {server['data']['disk']}")
            y -= 20

            c.drawString(70, y, f"Uptime : {server['data']['uptime']}")
            y -= 30

        else:

            c.drawString(70, y, "Server Offline")
            y -= 30

        if y < 100:
            c.showPage()
            y = height - 50

    c.save()

    return filename
