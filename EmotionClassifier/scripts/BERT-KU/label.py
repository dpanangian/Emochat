import os
os.environ['CUDA_VISIBLE_DEVICES'] = '0'
import json

import torch

from hparams import EMOTIONX_MODEL_HPARAMS
from models import EmotionX_Model
from utils import load_data_test, get_batch
from sklearn.metrics import precision_recall_fscore_support as score
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix,classification_report
import sys, getopt
from pathlib import Path
import matplotlib.pyplot as plt 
import seaborn as sns
import pandas as pd
import numpy as np

def label(argv):

  test_json_path = ''
  pretrained_model_path = ''
  try:
    opts, args = getopt.getopt(argv,"hi:m:",["ifile=","model="])
  except getopt.GetoptError:
    print('test.py -i <inputfile> -o <outputfile>')
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
        print('test.py -i <inputfile> -o <outputfile>')
        sys.exit()
    elif opt in ("-i", "--ifile"):
        test_json_path = arg
    elif opt in ("-m", "--model"):
        pretrained_model_path = arg
 
  p=Path(pretrained_model_path)

  if not torch.cuda.is_available():
    raise NotImplementedError()
  hparams = type('', (object,), EMOTIONX_MODEL_HPARAMS)()
  print('preprocessing...')
  test_dialogs, test_labels, dialogues = load_data_test(hparams, test_json_path)
  hparams.n_appear = [sum(test_labels, []).count(i) for i in range(hparams.n_class)]

  
  model = EmotionX_Model(hparams)
  checkpoint = torch.load(pretrained_model_path)
  model.load_state_dict(checkpoint)
  model.cuda()
  model.eval()
  pred_list=[]
  label_list=[]
  for i_test in range(len(test_dialogs) // hparams.batch_size):
    batch = get_batch(test_dialogs, hparams.batch_size, i_test)      
    logits = model(batch)[:, :-1] # trim the OOD column
    _, pred = torch.max(logits, dim=1)
    batch_labels = get_batch(test_labels, hparams.batch_size, i_test)
    batch_labels = sum(batch_labels, [])
    pred_lables = pred.tolist()
    pred_list.extend(pred_lables) 
    label_list.extend(batch_labels)

  precision, recall, fscore, support = score(label_list, pred_list)
  acc=accuracy_score(label_list, pred_list)
  print('precision: {}'.format(precision))
  print('recall: {}'.format(recall))
  print('fscore: {}'.format(fscore))
  print('support: {}'.format(support))
  print('accuracy: {}'.format(acc))

  cf_matrix = confusion_matrix(label_list, pred_list)
  df_cm = pd.DataFrame(cf_matrix, columns=np.unique(label_list), index = np.unique(label_list))
  df_cm.index.name = 'Actual'
  df_cm.columns.name = 'Predicted'
  sns.heatmap(df_cm, cmap="Blues", annot=True,annot_kws={"size": 16}, fmt = 'g', square=2, linewidth=1.)
  plt.show()

  print('labeling...')

  index_to_emotion = {0: 'joy', 1: 'fear', 2: 'surprise', 3: 'sadness', 4: 'anger', 5: 'disgust'}
  for dialog in dialogues:
    for utter_dict in dialog:
      utter_dict['pred_emotion'] = index_to_emotion[pred_list[0]]
      pred_list.pop(0)

  result_dir = os.path.join(str(p.parent),'result.json')
  json.dump(dialogues, open(result_dir, 'w'), indent=4, sort_keys=True)

if __name__ == '__main__':
  label(sys.argv[1:])