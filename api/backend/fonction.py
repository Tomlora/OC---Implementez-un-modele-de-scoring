from sklearn.metrics import confusion_matrix

def cout_metier(y_test, pred_test_y):
    poids_tn = 1 # on maximise le nombre de personnes pouvant rembourser son prêt
    poids_fp = 0
    poids_fn = -10 # on veut à tout prix éviter les personnes ne remboursant pas le prêt que l'algorithme n'arrive pas à détecter
    poids_tp = 0
    conf_mat = confusion_matrix(y_test, pred_test_y)
    tn, fp, fn, tp = conf_mat.ravel()
    total = tn+fp+fn+tp
    
    return (tn*poids_tn + fp*poids_fp + fn*poids_fn + tp * poids_tp)/total