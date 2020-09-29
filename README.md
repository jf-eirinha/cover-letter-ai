# Cover Letter AI

This model produces cover letters from a prefix text. It uses GPT-2 trained with thousands of cover letters.

## Running the model

I recommend creating a virtual environment with conda and install the required packages:

```
conda create --name coverletteraienv python=3.6
conda activate coverletteraienv
pip install tensorflow==1.14 gpt-2-simple absl-py
```

> Make sure you use a Python 3 version equal or below 3.6

If you're on MacOS, also run the following:

```
conda install nomkl
```

Finally, to generate the cover letter run:

```
python -W ignore cover-letter-ai.py --prefix "Dear Sirs, I am applying for the hairdresser position because"
```

This is not optimized so it takes a couple of minutes to make the inference.
