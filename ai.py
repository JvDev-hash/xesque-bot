import json
import requests
import random
import spacy

def replace_with_random_words(text, replacement_prob=0.3):
    nlp = spacy.load("pt_core_news_sm")
    doc = nlp(text)
    replacements = { 'NOUN': ['Xesque', 'Desque', 'Raulis', 'Brelele', 'Trelele', 'Xesquedele', 'Desquexele', 'Deregue'] }
    
    new_words = []
    for token in doc:
        if random.random() < replacement_prob and token.pos_ in replacements:
            new_words.append(random.choice(replacements[token.pos_]))
        else:
            new_words.append(token.text)
    
    # Reconstruct the text with proper spacing
    return " ".join(new_words).replace(" ,", ",").replace(" .", ".").replace(" '", "'")

def process_ndjson_stream(url, prompt):
    
    data = {
	    "model": "gemma3:1b",
        "prompt":  "Limite suas respostas a 2000 caracteres. Responda o prompt a seguir. " + prompt,
	    "stream": True
    }

    response = requests.post(url, stream=False, json=data)
    response.raise_for_status()

    finalString = ""
    
    for line in response.iter_lines():
        if line:  # Ignora linhas vazias
            try:
                data = json.loads(line)
                finalString = finalString + data['response']
                #print(data['response'])
                # Processa cada objeto aqui
            except json.JSONDecodeError as e:
                print(f"Erro ao decodificar JSON: {e} - Linha: {line}")
    return replace_with_random_words(finalString)
    #return finalString
# Uso
#process_ndjson_stream("http://localhost:11434/api/generate", "Oi, tudo bem?")