from nltk.translate.bleu_score import sentence_bleu
from nltk.translate.bleu_score import SmoothingFunction
import subprocess
import csv
import timeit


def translate():
    command = ' '.join(
        ['python', '-m', 'sockeye.translate',
         '-m', 'trained_model_short_20', '-i', 'enu_src_word.en',
         '-o', 'enu_translation_short_word.en'])
    subprocess.call(command, shell=True)


def calculate_BLEU(ref, cdd):
    return round(sentence_bleu([ref], cdd,
                            smoothing_function=SmoothingFunction().method1), 4)


def enumerate_sentences(src_file):
    with open('enu_src.zh', 'w') as new_file:
        for line in src_file:
            word_sequence = line.split()
            new_file.write(line)
            for i in range(len(word_sequence)):
                new_line = ' '.join(word_sequence[:i]+word_sequence[i+1:])
                new_file.write(new_line+'\n')


def enumerate_sentences_word(src_file):
    with open('enu_src_word.en', 'w') as new_file:
        for line in src_file:
            word_sequence = line.split('@@')
            new_file.write(line)
            for i in range(len(word_sequence)):
                new_line = '@@'.join(word_sequence[:i]+word_sequence[i+1:])
                new_file.write(new_line)
            new_file.write('\n')


def main():
    start = timeit.default_timer()
    total_blue = 0
    total_old_blue = 0
    total_new_blue = 0
    valid_sentence = 0
    valid_enumeration = 0
    all_sentence = 0
    hallucination = 0

    with open('corpus.test.char.en', 'r') as src:
        enumerate_sentences_word(src)
    translate()
    src = open('corpus.test.char.en', 'r')
    candidates = open('enu_translation_long_word.en', 'r')
    ref = open('corpus.test.char.zh', 'r')
    eval = open('evaluate_result_long_word_en.csv', 'w')
    fieldnames = ['src', 'ref', 'trans', 'BLEU', 'new_trans', 'new_BLEU', 'token']
    writer = csv.DictWriter(eval, fieldnames=fieldnames)
    writer.writeheader()
    for line in src:
        zh_cdd = candidates.readline().split()
        zh_ref = ref.readline().split()
        BLEU_score = calculate_BLEU(zh_ref, zh_cdd)
        src_seq = line.split('@@')
        total_blue += BLEU_score
        all_sentence += 1
        # print(line, zh_ref, zh_cdd, BLEU_score, len(src_seq))
        if BLEU_score >= 0.5:
            valid_sentence += 1
            total_old_blue += BLEU_score
            for i in range(len(src_seq)):
                valid_enumeration += 1
                token = src_seq[i]
                new_zh_cdd = candidates.readline().split()
                new_BLEU = calculate_BLEU(zh_ref, new_zh_cdd)
                total_new_blue += new_BLEU
                if new_BLEU < 0.1:
                    hallucination += 1
                    writer.writerow({'src': line.replace(' ', '').replace('@@', ' '),
                                     'ref': ''.join(zh_ref),
                                     'trans': ''.join(zh_cdd),
                                     'BLEU': BLEU_score,
                                     'new_trans': ''.join(new_zh_cdd),
                                     'new_BLEU': new_BLEU,
                                     'token': token})
        else:
            for i in range(len(src_seq)):
                candidates.readline()

    stop = timeit.default_timer()
    print('total_sentence:', all_sentence,
          'avg_bleu:', total_blue/all_sentence,
          'valid_sentence:', valid_sentence,
          'avg_old_bleu:', total_old_blue/valid_sentence,
          'valid_enumeration:', valid_enumeration,
          'avg_new_bleu:', total_new_blue/valid_enumeration,
          'hallucination:', hallucination)
    print('Time in min: ', (stop - start)/60)


if __name__ == "__main__":
    main()
