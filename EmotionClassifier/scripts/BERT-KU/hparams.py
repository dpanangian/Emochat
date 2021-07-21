from collections import defaultdict


EMOTIONX_MODEL_HPARAMS = defaultdict(
  description='base',
  model_name='base_max_both_em',

  fr_test_path='../../EmotionClassifier/data/friends.test.json',
  fr_train_path='../../EmotionClassifier/data/friends.train.json',
  em_test_path='../../EmotionClassifier/data/emochat.test.one_class.json',
  em_train_path='../../EmotionClassifier/data/emochat.train.one_class.json',
  fb_test_path='../../EmotionClassifier/data/facebook.test.json',
  fb_train_path='../../EmotionClassifier/data/facebook.train.json',  

  save_dir='./saves/',
  log_dir='./logs/',
  log_micro_f1='micro_f1',
  log_wce_loss='train_loss',

  # bert
  bert_type='bert-base-german-cased', # we used post-trained model instead of this.
  posttrained_model_path='',
  max_input_len=512,
  cls_token='[CLS]',
  sep_token='[SEP]',
  pad_token='[PAD]',
  cls_id=101,
  sep_id=4,
  pad_id=0,

  # classifier
  hidden_size=768,
  inter_hidden_size=384,
  n_class=6+1, # neutral, joy, sadness, anger + OOD

  # train
  n_epoch=10,
  batch_size=1,
  learning_rate=2e-5,
  dropout=0.1,
  clip=5,
)