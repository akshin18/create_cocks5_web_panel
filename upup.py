# импортируем библиотеки
import paramiko
import time


def main_deploy(host, user, secret, pport, proxy_pass):  # функция разворачивает Socks5 proxy на сервер, используя
    # стандартный порт 1080, подключаться пожно под пользователем root или proxy
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=user, password=secret, port=22)
    ssh = client.invoke_shell()
    time.sleep(2)
    out = ssh.recv(60000)
    # print(out)
    name = str(out[-16:])
    print("Server user:" + name)
    print("Work starting")
    ssh.send("sudo apt update" + "\n")
    time.sleep(1)
    while True:
        out = ssh.recv(60000)
        # print(out)
        if str(out[-16:]) == name:
            print("Update complete")
            break
        else:
            print("Wait fo it!")
            time.sleep(5)
    time.sleep(2)
    ssh.send("sudo apt install dante-server" + "\n")
    time.sleep(10)
    print("Dante installed")
    print("Config started")
    ssh.send("echo logoutput: stderr > /etc/danted.conf" + "\n")
    ssh.send("ifacer=`ip r | grep default | grep -Po '(?<=dev )(\S+)'`" + "\n")
    ssh.send("echo internal: ${ifacer} port = " + pport + "  >> /etc/danted.conf" + "\n")
    ssh.send("echo external: ${ifacer} >> /etc/danted.conf" + "\n")
    ssh.send("echo method: username >> /etc/danted.conf" + "\n")
    ssh.send("echo user.privileged: root >> /etc/danted.conf" + "\n")
    ssh.send("echo user.notprivileged: nobody >> /etc/danted.conf" + "\n")
    ssh.send("echo user.libwrap: nobody >> /etc/danted.conf" + "\n")
    ssh.send("echo  client pass { >> /etc/danted.conf" + "\n")
    ssh.send('echo  -e "\\tfrom: 0.0.0.0/0 to: 0.0.0.0/0" >> /etc/danted.conf' + "\n")
    ssh.send('echo  -e "\\tlog: error connect disconnect">> /etc/danted.conf' + "\n")
    ssh.send("echo  } >> /etc/danted.conf" + "\n")
    ssh.send("echo  client block { >> /etc/danted.conf" + "\n")
    ssh.send('echo  -e "\\tfrom: 0.0.0.0/0 to: 0.0.0.0/0" >> /etc/danted.conf' + "\n")
    ssh.send('echo  -e "\\tlog: connect error" >> /etc/danted.conf' + "\n")
    ssh.send("echo  } >> /etc/danted.conf" + "\n")
    ssh.send("echo  pass { >> /etc/danted.conf" + "\n")
    ssh.send('echo  -e "\\tfrom: 0.0.0.0/0 to: 0.0.0.0/0" >> /etc/danted.conf' + "\n")
    ssh.send('echo  -e "\\tlog: error connect disconnect" >> /etc/danted.conf' + "\n")
    ssh.send("echo  } >> /etc/danted.conf" + "\n")
    ssh.send("echo  block { >> /etc/danted.conf" + "\n")
    ssh.send('echo  -e "\\tfrom: 0.0.0.0/0 to: 0.0.0.0/0" >> /etc/danted.conf' + "\n")
    ssh.send('echo  -e "\\tlog: connect error" >> /etc/danted.conf' + "\n")
    ssh.send("echo  } >> /etc/danted.conf" + "\n")
    print("Config file created")
    ssh.send("service danted restart" + "\n")
    time.sleep(5)
    print("Dante restarted")
    ssh.send('passwd proxy' + "\n")
    print("Password changing to ", proxy_pass)
    ssh.send(proxy_pass + "\n")
    time.sleep(3)
    ssh.send(proxy_pass + "\n")
    print("Password changed")
    print("Done")


# main_deploy("0.0.0.0", "root", "pass", "22", "123456789987456321") #пример запуска функции

def proxy_restart(host, user, secret):  # функция перезагружает сервис проски
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=user, password=secret, port=22)
    ssh = client.invoke_shell()
    time.sleep(2)
    print("Work starting")
    ssh.send("id" + "\n")
    time.sleep(1)
    ssh.send("service danted restart" + "\n")
    time.sleep(1)
    print("Work complete")


def proxy_stop(host, user, secret):  # функция останавливает сервис проски
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=user, password=secret, port=22)
    ssh = client.invoke_shell()
    time.sleep(2)
    print("Work starting")
    ssh.send("id" + "\n")
    time.sleep(1)
    ssh.send("service danted stop" + "\n")
    time.sleep(1)
    print("Work complete")

#proxy_stop("0.0.0.0", "root", "pass", "22") #пример запуска функции

def server_restart(host, user, secret, port):  # функция перезагружает сервер
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=user, password=secret, port=port)
    ssh = client.invoke_shell()
    time.sleep(2)
    print("Work starting")
    ssh.send("id" + "\n")
    time.sleep(1)
    ssh.send("reboot" + "\n")
    time.sleep(1)
    print("Work complete")


# server_restart("0.0.0.0", "root", "pass", "22") #пример запуска функции

def proxy_port_ch(host, user, secret, port, pport):  # функция меняет порт прокси на заданный
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=user, password=secret, port=port)
    ssh = client.invoke_shell()
    time.sleep(2)
    out = ssh.recv(60000)
    name = str(out[-16:])
    print("Work starting")
    ssh.send("sudo apt update" + "\n")
    time.sleep(1)
    while True:
        out = ssh.recv(60000)
        if str(out[-16:]) == name:
            print("Update complete")
            break
        else:
            print("Wait fo it!")
            time.sleep(5)
    ssh.send("echo logoutput: stderr > /etc/danted.conf" + "\n")
    ssh.send("ifacer=`ip r | grep default | grep -Po '(?<=dev )(\S+)'`" + "\n")
    ssh.send("echo internal: ${ifacer} port = " + pport + "  >> /etc/danted.conf" + "\n")
    ssh.send("echo external: ${ifacer} >> /etc/danted.conf" + "\n")
    ssh.send("echo method: username >> /etc/danted.conf" + "\n")
    ssh.send("echo user.privileged: root >> /etc/danted.conf" + "\n")
    ssh.send("echo user.notprivileged: nobody >> /etc/danted.conf" + "\n")
    ssh.send("echo user.libwrap: nobody >> /etc/danted.conf" + "\n")
    ssh.send("echo  client pass { >> /etc/danted.conf" + "\n")
    ssh.send('echo  -e "\\tfrom: 0.0.0.0/0 to: 0.0.0.0/0" >> /etc/danted.conf' + "\n")
    ssh.send('echo  -e "\\tlog: error connect disconnect">> /etc/danted.conf' + "\n")
    ssh.send("echo  } >> /etc/danted.conf" + "\n")
    ssh.send("echo  client block { >> /etc/danted.conf" + "\n")
    ssh.send('echo  -e "\\tfrom: 0.0.0.0/0 to: 0.0.0.0/0" >> /etc/danted.conf' + "\n")
    ssh.send('echo  -e "\\tlog: connect error" >> /etc/danted.conf' + "\n")
    ssh.send("echo  } >> /etc/danted.conf" + "\n")
    ssh.send("echo  pass { >> /etc/danted.conf" + "\n")
    ssh.send('echo  -e "\\tfrom: 0.0.0.0/0 to: 0.0.0.0/0" >> /etc/danted.conf' + "\n")
    ssh.send('echo  -e "\\tlog: error connect disconnect" >> /etc/danted.conf' + "\n")
    ssh.send("echo  } >> /etc/danted.conf" + "\n")
    ssh.send("echo  block { >> /etc/danted.conf" + "\n")
    ssh.send('echo  -e "\\tfrom: 0.0.0.0/0 to: 0.0.0.0/0" >> /etc/danted.conf' + "\n")
    ssh.send('echo  -e "\\tlog: connect error" >> /etc/danted.conf' + "\n")
    ssh.send("echo  } >> /etc/danted.conf" + "\n")
    print("Config file created")
    ssh.send("service danted restart" + "\n")
    time.sleep(5)
    print("Dante restarted")
    print("Done")

# proxy_port_ch("0.0.0.0", "root", "pass", "22", "5579") #пример запуска функции
