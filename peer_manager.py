import re
import time

class PeerManager:
    def __init__(self):
        self.offline_peers_log = {}

    def parse_sip_peers(self, output):
        peers = []
        lines = output.splitlines()

        for line in lines[1:]:
            match = re.search(r'^(\S+)\s+(\S+).*?\s+(OK|UNREACHABLE|UNKNOWN|.*)\s+.*?(\d+)', line)
            if match:
                ramal = match.group(1)
                status = match.group(3).lower() if match.group(3) else "unknown"
                response_time = match.group(4)
                peers.append({'ramal': ramal, 'status': status, 'response_time': response_time})

                if status == "unreachable":
                    if ramal not in self.offline_peers_log:
                        self.offline_peers_log[ramal] = {
                            'ramal': ramal,
                            'status': status,
                            'tempo_queda': time.time()  # Marca o tempo de quando caiu
                        }
                elif status != "unreachable":
                    if ramal in self.offline_peers_log:
                        del self.offline_peers_log[ramal]

        for ramal, log in self.offline_peers_log.items():
            if log['status'] == 'unreachable':
                log['tempo_queda'] = round(time.time() - log['tempo_queda'], 2)

        return peers, list(self.offline_peers_log.values())
