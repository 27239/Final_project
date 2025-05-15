import paramiko

servers = [

    {
        "name": "Ubuntu Server 1",
        "host": "192.168.50.141",
        "username": "yagnesh",
        "password": "cdac@123"
    },

    {
        "name": "Ubuntu Server 2",
        "host": "192.168.50.142",
        "username": "yagnesh",
        "password": "cdac@123"
    }

]


def execute_command(ssh, command):
    stdin, stdout, stderr = ssh.exec_command(command)

    output = stdout.read().decode().strip()

    return output


def get_server_status(server):

    ssh = paramiko.SSHClient()

    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # SSH connection test
    ssh.connect(
        hostname=server["host"],
        username=server["username"],
        password=server["password"],
        timeout=5,
        banner_timeout=5,
        auth_timeout=5
    )

    data = {}

    data["hostname"] = execute_command(
        ssh,
        "hostname"
    )

    data["cpu"] = execute_command(
        ssh,
        "top -bn1 | grep 'Cpu(s)' | awk '{print $2+$4}'"
    )

    data["memory"] = execute_command(
        ssh,
        "free | awk '/Mem:/ {printf(\"%.2f\", $3/$2 * 100)}'"
    )

    data["disk"] = execute_command(
        ssh,
        "df / | awk 'END{print $5}'"
    )

    data["uptime"] = execute_command(
        ssh,
        "uptime -p"
    )

    data["users"] = execute_command(
        ssh,
        "who"
    )

    data["ip"] = execute_command(
        ssh,
        "hostname -I"
    )

    ssh.close()

    return data



def monitor_all_servers():

    result = []

    for server in servers:

        try:

            data = get_server_status(server)

            result.append({
                "server": server["name"],
                "status": "ONLINE",
                "data": data
            })


        except (paramiko.AuthenticationException,
                paramiko.SSHException,
                TimeoutError,
                OSError) as e:

            result.append({
                "server": server["name"],
                "status": "OFFLINE",
                "error": str(e)
            })


        except Exception as e:

            result.append({
                "server": server["name"],
                "status": "OFFLINE",
                "error": str(e)
            })


    return result



if __name__ == "__main__":

    servers_status = monitor_all_servers()

    for server in servers_status:

        print("=" * 50)

        print(server["server"])
        print(server["status"])

        if server["status"] == "ONLINE":

            for key, value in server["data"].items():

                print(f"\n{key.upper()}")
                print(value)

        else:

            print(server["error"])

