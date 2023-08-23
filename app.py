from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('https://joaojmol.github.io/', methods=['GET','POST'])
def index():
    return render_template('index.html')

@app.route('https://joaojmol.github.io/buscar', methods=['POST'])
def buscar_dados():
    nome = request.form.get('nome')

    query_params = {
        "nome": nome,
        "origem": 241,
        "token": "9c7b96e74285fef10684acf34646da02"
    }

    # Primeira requisição para buscar dados da pessoa
    url = "https://crmrbacademy.apprubeus.com.br/api/Contato/dadosPessoas"
    url2 = "https://crmrbacademy.apprubeus.com.br/api/Contato/listarOportunidades"
    
    response = requests.post(url, params=query_params)
    
    if response.status_code == 200:
        pessoa_data = response.json()
        pessoa_id = pessoa_data["dados"][0]["id"]
        response2 = requests.post(url2, params={
            "id": pessoa_id ,
            "origem": 241,
            "token": "9c7b96e74285fef10684acf34646da02"
        })
        if response2.status_code == 200:
            registro_data = response2.json()
            for registro in registro_data["dados"]:
                if registro["processo"] == "20":
                    cod_oferta = registro["codOferta"]
                    cod_curso = registro["codCurso"]
                    enviar_evento(pessoa_id, cod_oferta, cod_curso)
                    break

        return jsonify(pessoa_data)
    else:
        return "Erro ao buscar dados da pessoa."
    

def enviar_evento(pessoa_id,cod_oferta,cod_curso):
    # Segunda requisição para enviar evento
    url = "https://crmrbacademy.apprubeus.com.br/api/Evento/cadastro"
    evento_data = {
        "tipo": 1652,
        "pessoa":{
            "id": pessoa_id
        },
        "codOferta": cod_oferta,
        "codCurso": cod_curso,
        "origem": 241,
        "token": "9c7b96e74285fef10684acf34646da02"
    }
    
    response = requests.post(url, json=evento_data)
    
    if response.status_code == 200:
        print("Evento enviado com sucesso!")
    else:
        print("Erro ao enviar evento.")

if __name__ == '__main__':
    app.run(debug=True)