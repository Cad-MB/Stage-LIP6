import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

def jaccard_similarity(str1, str2):
    set1 = set(str1.split())
    set2 = set(str2.split())
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    return len(intersection) / len(union)

def group_object_ids_by_errors(csv_file, similarity_threshold=0.75):
    # Charger le fichier CSV dans un DataFrame
    df = pd.read_csv(csv_file)

    # Utiliser TfidfVectorizer pour convertir les messages d'erreurs en vecteurs de caractéristiques
    vectorizer = TfidfVectorizer()
    error_vectors = vectorizer.fit_transform(df['errorsMessages'])

    # Calculer la similarité des vecteurs de caractéristiques des messages d'erreurs
    similarity_matrix = linear_kernel(error_vectors, error_vectors)

    # Regrouper les objectId en fonction des messages d'erreurs similaires
    grouped_data = {}
    for idx, row in df.iterrows():
        message = row['errorsMessages']
        object_id = row['objectId']
        if message not in grouped_data:
            # Trouver les messages d'erreurs similaires et les regrouper
            similar_indices = similarity_matrix[idx].argsort()[::-1]
            similar_messages = df.iloc[similar_indices[1:]]  # Exclure l'indice actuel (il est similaire à lui-même)
            similar_messages = similar_messages[similar_messages['errorsMessages'] != message]
            for _, similar_row in similar_messages.iterrows():
                similar_message = similar_row['errorsMessages']
                if jaccard_similarity(message, similar_message) >= similarity_threshold:
                    if message in grouped_data:
                        grouped_data[message].append(similar_row['objectId'])
                    else:
                        grouped_data[message] = [object_id, similar_row['objectId']]

    return grouped_data

if __name__ == "__main__":
    # Utilisez un chemin brut (raw string) en ajoutant 'r' avant le chemin
    csv_file_path = r'C:\Users\Surface\Documents\LIP6\Stage-LIP6\Validation\wp\validationErrors_03082023_165134.csv'

    result = group_object_ids_by_errors(csv_file_path, similarity_threshold=0.75)

    # Convertir les données regroupées en DataFrame
    grouped_data_df = pd.DataFrame(result.items(), columns=['errorsMessages', 'objectId'])
    
    # Utilisez des barres obliques inverses doubles (\\) ou un chemin brut pour éviter les erreurs d'échappement
    grouped_data_df.to_csv(r'C:\Users\Surface\Documents\LIP6\Stage-LIP6\Validation\wp\class.csv', index=False)
