
import json

def get_dummy_eval():
    file_path = 'single_words\\temp.json'
    with open(file_path, 'r') as file:
        data = json.load(file)

    syllables_with_scores = []
    
    # Navigate through the "NBest" list and the "Words" list
    for nbest_item in data.get('NBest', []):
        for word in nbest_item.get('Words', []):
            for syllable in word.get('Syllables', []):
                syllable_text = syllable.get('Syllable')
                accuracy_score = syllable.get('PronunciationAssessment', {}).get('AccuracyScore')
                
                # Append the syllable and its accuracy score to the list
                syllables_with_scores.append({
                    'syllable': syllable_text,
                    'accuracy_score': accuracy_score
                })
    
    return syllables_with_scores

