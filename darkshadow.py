import socket
import whois 
import requests
import pyfiglet 
  
result = pyfiglet.figlet_format("Dark-Shadow") 
print(result)  

def banner():
    print("""https://github.com/BearSmithRiver""")
banner()
print()
def port_scan(ip, ports):
    open_ports = []
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)

        try:
            sock.connect((ip, port))
            open_ports.append(port)
            banner = sock.recv(1024).decode('utf-8').strip()
            print(f"Porta {port} aberta - Serviço: {banner}")
        except socket.error:
            print(f"Porta {port} fechada")
        finally:
            sock.close()

    return open_ports

def whois_lookup(domain):
    try:
        result = whois.whois(domain)
        return result
    except whois.parser.PywhoisError as e:
        print(f"Erro ao consultar WHOIS para {domain}: {e}")
        return None

def brute_force_directory(url, directory_file_path):
    try:
        with open(directory_file_path, 'r') as file:
            directories = file.read().splitlines()

            for directory in directories:
                full_url = url + '/' + directory
                response = requests.get(full_url)

                if response.status_code == 200:
                    print(f"Directory found: {full_url}")

    except FileNotFoundError:
        print(f"Arquivo de lista de diretórios não encontrado: {directory_file_path}")
    except Exception as e:
        print(f"Erro durante o ataque de força bruta: {e}")

if __name__ == "__main__":
    option = int(input("Escolha a opção:\n1. WHOIS\n2. Brute-force de diretórios\n3. Portscan\n"))

    if option == 1:
        target_domain = input("Digite o domínio alvo: ")
        whois_result = whois_lookup(target_domain)

        if whois_result:
            print(f"Informações WHOIS para {target_domain}:\n{whois_result}")
        else:
            print(f"Falha ao recuperar informações WHOIS para {target_domain}")

    elif option == 2:
        target_domain = input("Digite o domínio alvo: ")
        directory_file_path = input("Digite o caminho do arquivo de lista de diretórios: ")
        brute_force_directory(target_domain, directory_file_path)

    elif option == 3:
        target_ip = input("Digite o endereço IP alvo: ")
        target_ports = list(map(int, input("Digite as portas a serem verificadas (separadas por espaço): ").split()))
        open_ports = port_scan(target_ip, target_ports)

        if open_ports:
            print(f"Portas abertas no IP {target_ip}: {open_ports}")
        else:
            print(f"Nenhuma porta aberta no IP {target_ip}")

    else:
        print("Opção inválida. Por favor, escolha uma opção de 1 a 3.")
