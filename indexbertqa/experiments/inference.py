import json
from tqdm import tqdm
from indexbertqa.reader.bert_reader import BERT
from indexbertqa.retriever.pyserini_retriever import retriever, build_searcher
from indexbertqa.utils.utils_new import extract_squad_questions
from indexbertqa.experiments.args import *

if __name__ == "__main__":
    questions = extract_squad_questions(args.dataset_path)
    bert_reader = BERT(args.model_name_or_path, args.tokenizer_name)
    searcher = build_searcher(args.index_path, language=args.language)

    all_answer = []
    for question in tqdm(questions):
        contexts = retriever(question, searcher, args.topk)
        final_answers = bert_reader.predict(question, contexts)
        final_answers_lst = []
        for ans in final_answers:
            final_answers_lst.append(
                {"id": question.id,
                 "answer": ans.text,
                 "phrase_score": ans.score,
                 "paragraph_score": ans.ctx_score,
                 }
            )
        all_answer.append(final_answers_lst)
    json.dump(all_answer, open(args.output, 'w'), indent=4)

