# HALLUCINATION Research

This repo contains files that I use to evaluate NMT models.
Steps:\\

1. Put a parallel data (train, val, and test) under the root dir of this project.\\
2. Run tokenize_tool.py with corresponding file names to tokenize all sentences by char.\\
3. Prepare data using a command like this: `python3 -m sockeye.prepare_data -s 
corpus.train.en -t corpus.train.zh --num-samples-per-shard 10000 --shared-vocab 
-o train_short_data`. In my previous experiments, the `num-sample-per-shard` 
parameter is 1,000 for the 1,000,000 dataset and 10,000 for the 10,000,000 one.\\
4. Train the model using a command like this: `python3 -m sockeye.train -d 
train_short_data -vs corpus.val.char.en -vt corpus.val.char.zh 
--decode-and-evaluate 500 --max-num-checkpoint-not-improved 20 
--batch-size 256 --max-seq-len 100 --shared-vocab -o trained_model_short`\\
5. Evaluate the model on test data by running evaluate.py after manually updating
the corresponding file names in it.

