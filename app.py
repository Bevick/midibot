from flask import Flask, request, send_file
import pretty_midi
import os

app = Flask(__name__)

# Função para criar MIDI
def create_midi(progression):
    midi = pretty_midi.PrettyMIDI()
    piano_program = pretty_midi.instrument_name_to_program("Acoustic Grand Piano")
    piano = pretty_midi.Instrument(program=piano_program)

    # Dicionário de acordes
    chords = {
        "E9": [40, 44, 47, 51, 54],
        "C#m7": [40, 43, 47, 51],
        "A6(9)": [33, 40, 44, 47, 50],
        "B7(13)": [35, 42, 45, 49, 52]
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
    file_path = "output.mid"
    midi.write(file_path)
    return file_path

# Endpoint para criar MIDI
@app.route("/generate", methods=["POST"])
def generate():
    try:
        data = request.json
        progression = data.get("progression", ["E9", "C#m7", "A6(9)", "B7(13)"])
        midi_file = create_midi(progression)
        if os.path.exists(midi_file):
            return send_file(midi_file, as_attachment=True)
        else:
            return {"error": "File not generated"}, 500
    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == "__main__":
    app.run(debug=True)
