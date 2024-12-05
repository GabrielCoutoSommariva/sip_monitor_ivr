import paramiko  # Certifique-se de que o paramiko está importado
import time

class SipClient:
    def __init__(self, container_ip, username, password):
        self.container_ip = container_ip
        self.username = username
        self.password = password

    def connect_and_execute_sip_command(self):
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            start_time = time.time()

            ssh_client.connect(self.container_ip, username=self.username, password=self.password)
            stdin, stdout, stderr = ssh_client.exec_command('asterisk -rx "sip show peers"')

            output = stdout.read().decode()
            ssh_client.close()

            elapsed_time_ms = (time.time() - start_time) * 1000  # Converter para milissegundos
            return output, round(elapsed_time_ms, 2)

        except Exception as e:
            return f"Erro ao conectar ao container: {e}", None
