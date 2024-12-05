from flask import Flask, jsonify, render_template
from sip_client import SipClient
from peer_manager import PeerManager

# Criação do aplicativo Flask
app = Flask(__name__)

# Instâncias das classes
sip_client = SipClient(container_ip='172.31.102.161', username='root', password='s3rv1c0s##!,')
peer_manager = PeerManager()

# Rota inicial que renderiza a interface HTML
@app.route('/')
def index():
    return render_template("index.html")

# Rota para fornecer os dados atualizados dos peers SIP
@app.route('/update')
def update():
    output, response_time_ms = sip_client.connect_and_execute_sip_command()
    if "Erro" in output:
        return jsonify(peers=[], response_time_ms=0, offline_peers=[])

    peers, offline_peers = peer_manager.parse_sip_peers(output)

    return jsonify(peers=peers, response_time_ms=response_time_ms, offline_peers=offline_peers)

# Inicia o servidor Flask
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
