"""from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

# Configurações de conexão com o BD da Hostinger
db_config = {
    "host": "193.203.175.82",
    "user": "u115176877_GALLERY_AFRO",
    "password": "J20010917$!##&%20011013f",
    "database": "u115176877_GALLERY_AFRO"
}

@app.route('/get_image_ids', methods=['GET'])
def get_image_ids():
    try:
        # Conecta ao banco de dados
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Consulta para pegar todos os ImageId em ordem decrescente
        cursor.execute("SELECT ImageId FROM Image ORDER BY RegisterDate DESC")
        result = cursor.fetchall()

        # Extrai os IDs em uma lista de strings
        image_ids = [str(row[0]) for row in result]  # Convertendo para string para garantir compatibilidade

        # Fecha a conexão com o BD
        cursor.close()
        conn.close()

        # Retorna o JSON formatado
        response_json = {
            "image_ids": image_ids
        }
        print(response_json)  # Para debug
        return jsonify(response_json), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)"""
