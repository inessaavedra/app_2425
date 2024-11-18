import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

def load_and_prepare_data(file_path):
    data = pd.read_csv(file_path)
    data['Start Time'] = pd.to_datetime(data['Start Time'])
    data['Year'] = data['Start Time'].dt.year
    
    data['Content Type'] = data['Title'].apply(
    lambda x: 'Serie' if any(keyword in str(x) for keyword in ['Season', 'Temporada', 'Capítulo']) else 'Película'
    )

    
    # Codificar el tipo de contenido para el modelo
    le = LabelEncoder()
    data['Content_Type_encoded'] = le.fit_transform(data['Content Type'])
    return data, le

def train_content_type_model(data, profile_name):
    profile_data = data.loc[data['Profile Name'] == profile_name]
    if profile_data.empty:
        return None  # No hay datos para este perfil
    X = profile_data[['Year']]
    y = profile_data['Content_Type_encoded']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(class_weight='balanced', random_state=42)
    model.fit(X_train, y_train)
    return model

def predict_content_type(model, X, label_encoder):
    content_type_encoded = model.predict(X)[0]
    content_type = label_encoder.inverse_transform([content_type_encoded])[0]
    return content_type
