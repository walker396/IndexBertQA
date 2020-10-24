# IndexBertQA: Baseline on SQUAD QA

1. Clone the repo with ```git clone https://github.com/walker396/IndexBertQA.git```
2. ```pip install -r requirements.txt```

## Download PreBuilt Wikipedia Index

I adopt the 20180701 Wikipedia dump used in DrQA with Anserini; you can download the prepared index here:
```
wget ftp://72.143.107.253/indexbertqa/english_wiki_2018_index.zip
````
```*index.zip``` contains the indexed latest Wikipedia dump with Anserini.

After unzipping these files, put them under the root path of this repo, and then you are ready to go.
Take the following folder structure as an example:
```
IndexBertQA
+--- indexes
|    +--- lucene-index.enwiki-20180701-paragraphs
+--- other files under this repo
```


To run our finetuned model, just set ```--model_name_or_path rsvp-ai/<MODEL_NAME>```   
For example: ```--model_name_or_path rsvp-ai/indexbertqa-bert-large-squad```.

# Inferencing and evaluating

## Prepare the datasets:

```
cd data
wget https://rajpurkar.github.io/SQuAD-explorer/dataset/dev-v1.1.json
```

## Inferencing SQuAD under the open-domain setting
For `rsvp-ai/indexbertqa-bert-base-squad`
```
python -m indexbertqa.experiments.inference --dataset_path data/dev-v1.1.json \
                                           --index_path indexes/lucene-index.enwiki-20180701-paragraphs \
                                           --model_name_or_path rsvp-ai/indexbertqa-bert-base-squad \
                                           --output squad_bert_base_pred.json
                                           --topk 10

```




```
## Evaluation

```
mkdir temp
python -m indexbertqa.experiments.evaluate --eval_data data/dev-v1.1.json \
                                          --search_file prediction/squad_bert_large_pred.json \
                                          --output_path temp \
                                          --dataset squad
                                          
```
Expected results:
```
## rsvp-ai/indexbertqa-large-squad, this is finetuned based on bert-large-wwm-uncased
(0.4, {'exact_match': 41.54210028382214, 'f1': 49.45378799697662, 'recall': 51.119838584003105, 'precision': 49.8395951713666, 'cover': 47.228003784295176, 'overlap': 57.6631977294229})

## rsvp-ai/indexbertqa-bert-base-squad, this is finetuned based on bert-base-uncased
(0.5, {'exact_match': 40.179754020813625, 'f1': 47.828056659017584, 'recall': 49.517951036176, 'precision': 48.3495034100538, 'cover': 45.50614947965941, 'overlap': 56.20624408703879})
```