from flask import Flask, render_template, send_file

from email_report import send_alert
from ssh_monitoring import monitor_all_servers
from database import create_database, insert_data
from pdf_report import generate_report

app = Flask(__name__)

# Create the database when the application starts
create_database()


@app.route("/")
def dashboard():
    servers = monitor_all_servers()

    for server in servers:
        if server["status"] == "ONLINE":
            # Store server data in the database
            insert_data(server)

            # Check CPU usage
            cpu = float(server["data"]["cpu"])
            if cpu > 5:
                send_alert(
                    server["server"],
                    f"CPU Usage is {cpu}%"
                )

            # Check Memory usage
            memory = float(server["data"]["memory"])
            if memory > 80:
                send_alert(
                    server["server"],
                    f"Memory Usage is {memory}%"
                )

            # Check Disk usage
            disk = int(server["data"]["disk"].replace("%", ""))
            if disk > 90:
                send_alert(
                    server["server"],
                    f"Disk Usage is {disk}%"
                )

    return render_template(
        "index.html",
        servers=servers
    )


@app.route("/report")
def report():
    servers = monitor_all_servers()
    filename = generate_report(servers)
    return send_file(filename, as_attachment=True)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
        use_reloader=False
    )

