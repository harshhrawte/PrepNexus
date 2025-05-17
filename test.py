import joblib

# Load the model from the .pkl file
model_data = joblib.load("resume_role_predictor_improved.pkl")

# Check the type of the loaded object
print("Type of loaded model:", type(model_data))

# If it's a dictionary, print the keys to understand its structure
if isinstance(model_data, dict):
    print("Keys in the dictionary:", model_data.keys())
    
    # Inspect and print details of each component
    print("TF-IDF Vectorizer:", model_data.get('tfidf', 'Not available'))
    print("SVD Components:", model_data.get('svd', 'Not available'))
    print("Scaler:", model_data.get('scaler', 'Not available'))
    print("Imputer:", model_data.get('imputer', 'Not available'))
    print("Label Encoder:", model_data.get('label_encoder', 'Not available'))
    print("Model:", model_data.get('model', 'Not available'))
    print("Important Skills:", model_data.get('important_skills', 'Not available'))
    print("Model Name:", model_data.get('model_name', 'Not available'))
    print("Accuracy:", model_data.get('accuracy', 'Not available'))

    # Optionally, check the dimensionality of the components
    if 'svd' in model_data:
        print("SVD components:", model_data['svd'].n_components)
        
    if 'scaler' in model_data:
        print("Scaler expected features:", model_data['scaler'].n_features_in_)
        
    if 'model' in model_data:
        print("Model type:", type(model_data['model']))
