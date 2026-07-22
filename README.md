# 🌸 Anime Score Oracle

> An AI-powered Anime Rating Prediction System built using Machine Learning and deployed on Hugging Face Spaces.

Anime Score Oracle predicts an anime's rating (score out of 10) by analyzing various metadata such as episodes, popularity statistics, source material, age rating, and genres. The model leverages Machine Learning techniques to identify patterns that influence audience ratings and provides real-time predictions through an interactive web interface.

---

## 🚀 Live Demo

> Hugging Face Space:
>
> ADD YOUR HUGGING FACE LINK HERE

---

## 📌 Problem Statement

Anime ratings are influenced by multiple factors, including genre combinations, popularity metrics, audience engagement, and production characteristics. Understanding these relationships can provide valuable insights into audience preferences.

This project aims to predict an anime's score using Machine Learning by analyzing metadata such as:

- Episodes
- Anime Type
- Source Material
- Age Rating
- Popularity Rank
- Favorites
- Members
- User Scores
- Genres

---

## ✨ Features

- Real-time anime score prediction
- Interactive and aesthetic user interface
- Genre-based multi-label prediction support
- Machine Learning powered recommendations
- Popularity and engagement analysis
- Hugging Face deployment using Gradio

---

## 🧠 Machine Learning Pipeline

```
Anime Metadata
        ↓
   Data Cleaning
        ↓
 Feature Engineering
        ↓
 Label Encoding
        ↓
 Genre Encoding
        ↓
 Train-Test Split
        ↓
 Random Forest Regressor
        ↓
 Model Evaluation
        ↓
     Prediction
        ↓
    Hugging Face UI
```

---

## 🛠️ Technologies Used

### Programming Language

- Python

### Machine Learning

- Random Forest Regressor
- Scikit-Learn
- Label Encoding
- MultiLabel Binarizer

### Libraries

- Pandas
- NumPy
- Matplotlib
- Joblib
- Gradio

### Deployment

- Hugging Face Spaces

---

## 📊 Dataset Features

The model utilizes the following attributes for prediction:

- Episodes
- Anime Type
- Source
- Rating Classification
- Rank
- Popularity
- Favorites
- Members
- Scored By
- Multiple Anime Genres

Target Variable:

- Anime Score (/10)

---

## ⚙️ Data Preprocessing

The following preprocessing techniques were implemented:

- Missing value handling
- Forward filling of incomplete records
- Label Encoding for categorical variables
- Multi-label encoding for genres
- Feature selection
- Dataset cleaning and transformation

Several unnecessary attributes were removed to improve model performance and reduce noise within the dataset.

---

## 🤖 Machine Learning Model

The project utilizes:

> Random Forest Regressor

Random Forest was selected because it performs well on non-linear relationships and can effectively handle complex interactions between anime metadata and audience ratings.

### Model Workflow

```
Dataset
   ↓
Data Cleaning
   ↓
Feature Engineering
   ↓
Encoding
   ↓
Random Forest Training
   ↓
Prediction
   ↓
Performance Evaluation
```

---

## 📈 Model Evaluation

The model was evaluated using:

- RMSE (Root Mean Squared Error)
- R² Score
- Residual Analysis
- Feature Importance Analysis
- Actual vs Predicted Score Visualization

Performance analysis was carried out to understand feature contributions and prediction behavior.

---


## 📸 Project Preview

<p align="center">
  <img src="screenshots/anime-score-oracle.png" width="1000">
</p>

The Anime Score Oracle interface allows users to provide anime metadata, including episodes, source material, popularity statistics, age ratings, and genres to generate real-time rating predictions using Machine Learning.

---

## 📂 Repository Structure

```
Anime-Score-Oracle
│
├── Anime_Rating_Prediction.ipynb
├── requirements.txt
├── model.joblib
├── README.md
│
├── encoders
│      |
│      ├── le_type.joblib
│      ├── le_source.joblib
│      └── le_rating.joblib
│
├── screenshots
│      |
│      ├── home.png
│      └── prediction.png
│
└── sample_dataset.csv
```

---

## 🌱 Future Improvements

- Deep Learning based prediction models
- Personalized anime recommendations
- Hybrid recommendation systems
- Cloud-based model deployment
- Enhanced visualization dashboards
- Improved genre similarity analysis

---

## 🎓 Learning Outcomes

Through this project, I gained hands-on experience in:

- Machine Learning Pipelines
- Feature Engineering
- Random Forest Regression
- Data Preprocessing
- Model Evaluation Techniques
- Hugging Face Deployment
- Interactive ML Application Development

---

## ⭐ Built With

- Python
- Machine Learning
- Scikit-Learn
- Hugging Face Spaces
- Gradio
- Pandas
- NumPy

---

> Built as part of my journey in Artificial Intelligence, Machine Learning, and Real-World AI Applications.
