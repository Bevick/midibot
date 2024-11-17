@app.route("/generate", methods=["POST"])
def generate():
    try:
        # Verificar o cabeçalho Content-Type
        if not request.is_json:
            return jsonify({"error": "Unsupported Media Type. Use Content-Type: application/json"}), 415

        # Recebe a progressão do corpo da requisição
        data = request.json
        progression = data.get("progression", ["E9", "C#m7", "A6(9)", "B7(13)"])
        
        # Gera o arquivo MIDI
        midi_file = create_midi(progression)
        
        # Confirma se o arquivo foi gerado e existe
        if os.path.exists(midi_file):
            print(f"Enviando o arquivo MIDI: {midi_file}")
            with open(midi_file, "rb") as f:
                return Response(
                    f.read(),
                    mimetype="audio/midi",
                    headers={"Content-Disposition": "attachment;filename=output.mid"}
                )
        else:
            print("Arquivo MIDI não foi encontrado após criação.")
            return jsonify({"error": "MIDI file not found"}), 500
    except Exception as e:
        # Retorna o erro em caso de falha
        print(f"Erro na API: {e}")
        return jsonify({"error": str(e)}), 500
