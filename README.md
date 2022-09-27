## Projet OC (P7) : Implémentez un modèle de scoring

Le but du projet est d'aider une société financière, qui propose des crédits à la consommation.

Elle souhaite mettre en oeuvre un outil de scoring crédit, pour calculer la probabilité qu'un client rembourse son crédit, puis classifie la demande en crédit accordé ou non.

### Contraintes du projet :

Dans un soucis de transparence, il faut developper un dashboard interactif permettant aux conseillers clientèles de comprendre les décisions, et de disposer des informations clients plus facilement.
Les contraintes sont de mettre en place obligatoirement une __API__ et un __dashboard__ 

### Compétences évaluées :

- Déployer un modèle via une API sur le web
- Réaliser un dashboard pour présenter son travail de modélisation
- Rédiger une note méthodologique afin de communiquer sa démarche de modélisation
- Utiliser un logiciel de version de code pour assurer l'intégralité du modèle

### Ressources (non-exhaustif) :
- Pandas
- __Sklearn__ (LogisticRegression, DecisionTreeClassifier, RandomForest, GradientBoosting, LDA, MLP)
- LightGBM
- __Metrics__ (Matrice de confusion, recall, precision, accuracy, roc/auc curve, F1, make_scorer pour score personnalisée)
- Plotly / Matplotlib
- Shap
- Imblearn
- __FastApi__ + __Uvicorn__ pour API / __Streamlit__ pour Dashboard

