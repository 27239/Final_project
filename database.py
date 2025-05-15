import sqlite3

DATABASE = "monitoring.db"


def create_database():

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("""

        CREATE TABLE IF NOT EXISTS monitoring (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            server_name TEXT,

            status TEXT,

            hostname TEXT,

            cpu TEXT,

            memory TEXT,

            disk TEXT,

            uptime TEXT,

            users TEXT,

            ip TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )

    """)

    conn.commit()

    conn.close()


def insert_data(server):

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("""

        INSERT INTO monitoring(

        server_name,

        status,

        hostname,

        cpu,

        memory,

        disk,

        uptime,

        users,

        ip

        )

        VALUES(?,?,?,?,?,?,?,?,?)

    """,

    (

        server["server"],

        server["status"],

        server["data"].get("hostname",""),

        server["data"].get("cpu",""),

        server["data"].get("memory",""),

        server["data"].get("disk",""),

        server["data"].get("uptime",""),

        server["data"].get("users",""),

        server["data"].get("ip","")

    )

    )

    conn.commit()

    conn.close()
