from flask import Flask, request, send_file, jsonify, Response
import pretty_midi
import os

app = Flask(__name__)

# Função para criar MIDI
def create_midi(progression):
    try:
        midi = pretty_midi.PrettyMIDI()
        piano_program = pretty_midi.instrument_name_to_program("Acoustic Grand Piano")
        piano = pretty_midi.Instrument(program=piano_program)

        # Dicionário de acordes
        chords = {
    "E9": [40, 44, 47, 50, 54],        # E, G#, B, D, F#
    "C#m7": [41, 44, 48, 51],          # C#, E, G#, B
    "A6(9)": [33, 40, 44, 46, 50],     # A, C#, E, F#, B
    "B7(13)": [35, 43, 47, 50, 56],    # B, D#, F#, A, G#
}

        # Adicionando acordes
        start_time = 0
        for chord_name in progression:
            chord_notes = chords.get(chord_name, [])
            for note in chord_notes:
                note_obj = pretty_midi.Note(
                    velocity=100, pitch=note, start=start_time, end=start_time + 1
                )
                piano.notes.append(note_obj)
            start_time += 1

        midi.instruments.append(piano)

        # Salvando o arquivo MIDI
        file_path = "/tmp/output.mid"  # Diretório temporário
        midi.write(file_path)
        print(f"Arquivo MIDI criado: {file_path}")
        return file_path
    except Exception as e:
        print(f"Erro na criação do MIDI: {e}")
        raise

# Endpoint para criar MIDI
@app.route("/generate", methods=["POST"])
def generate():
    try:
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

if __name__ == "__main__":
    app.run(debug=True)
