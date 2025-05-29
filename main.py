import os
import requests
import zipfile
import json
from datetime import datetime

from urllib3.response import io

# Define the speaker ID
SPEAKER_ID = 3 # ずんだもん
SPEED_SCALE = 1.4
SPEAKER_ID = 2 # 四国めたん
SPEED_SCALE = 1.3
# SPEAKER_ID = 13 # 青山龍星
# SPEED_SCALE = 1.2
POST_PHONEME_LENGTH = 1.1

def read_text_from_file(filepath):
    print(f"Read text from {filepath}")
    with open(filepath, 'r', encoding='utf-8') as file:
        return file.read()

def get_audio_query(text):
    response = requests.post("http://127.0.0.1:50021/audio_query",
        params={
            'text': text,
            'speaker': SPEAKER_ID,
        })

    if response.status_code == 200:
        return response.json()
    else:
        message = f"Failed to get audio query for text: {text}, Status Code: {response.status_code}, {response.json()}"
        raise Exception(message)

def edit_audio_query(query):
    query['speedScale'] = SPEED_SCALE  # Update speedScale
    query['postPhonemeLength'] = POST_PHONEME_LENGTH  # Update postPhonemeLength
    return query

def handle_text(text):
    print('Get audio query')
    queries = []

    for line in text.strip().split('\n'):
        line = line.strip()

        if line and not line.startswith('#'):
            query = get_audio_query(line)

            if query:
                edited_query = edit_audio_query(query)
                queries.append(edited_query)

    return queries

def save_queries_to_file(queries, filename):
    print(f"Save audio query as json")
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(queries, f, ensure_ascii=False, indent=2)

def get_audio_from_queries(queries):
    print(f"Generate audio")

    synthesis_response = requests.post(
        f"http://127.0.0.1:50021/multi_synthesis?speaker={SPEAKER_ID}",
        json=queries,
        headers={"Content-Type": "application/json"}
    )

    if synthesis_response.status_code == 200:
        return synthesis_response.content
    else:
        message = f"Failed to synthesize audio, Status Code: {synthesis_response.status_code},, {synthesis_response.json()} "
        raise Exception(message)

def save_and_extract_zip(content, output_folder):
    print(f"Generate audio")
    z = zipfile.ZipFile(io.BytesIO(content))
    z.extractall(output_folder)

def main():
    # Read text from input file
    text = read_text_from_file('./input/input.txt')

    queries = handle_text(text)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Define output filenames
    queries_filename = f'./output/{timestamp}.txt'
    audio_folder = f'./output/{timestamp}_audio'

    save_queries_to_file(queries, queries_filename)

    content = get_audio_from_queries(queries)

    save_and_extract_zip(content, audio_folder)

if __name__ == "__main__":
    main()
