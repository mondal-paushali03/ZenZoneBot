import joblib

# Load the trained intent classifier model
def predict_intent(user_prompt):
    intent_classifier = joblib.load('intent_classifier_model_1.joblib')

# Load the TF-IDF vectorizer used during training
    tfidf_vectorizer = joblib.load('tfidf_vectorizer.joblib')

# User prompt for prediction
    

# Transform the new prompt into TF-IDF features
    user_prompt_tfidf = tfidf_vectorizer.transform([user_prompt])

# Predict the intent label of the new prompt
    predicted_intent = intent_classifier.predict(user_prompt_tfidf)
    
# Display the predicted intent
    
    return(predicted_intent[0].lower())
