
# MIDI Bot
A Flask-based web service to generate MIDI files with custom chord progressions.

## How to Use
1. Clone the repository and install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Run the application locally:
   ```
   python app.py
   ```
3. Deploy the application to Render for cloud hosting.

## API Endpoint
### `/generate` (POST)
- **Request**:
  ```json
  {
    "progression": ["E9", "C#m7", "A6(9)", "B7(13)"]
  }
  ```
- **Response**: A downloadable MIDI file.
