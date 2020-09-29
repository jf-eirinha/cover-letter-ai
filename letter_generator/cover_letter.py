import gpt_2_simple as gpt2


_checkpoint_dir = './letter_generator/models/gpt2/checkpoint_run1/checkpoint'


def generate_letter(prefix=None):

    sess = gpt2.start_tf_sess()

    gpt2.load_gpt2(sess,
                   run_name="run1",
                   checkpoint_dir=_checkpoint_dir,
                   model_name=None,
                   model_dir="models")

    return gpt2.generate(sess,
                         run_name='run1',
                         checkpoint_dir=_checkpoint_dir,
                         model_name=None,
                         model_dir='models',
                         sample_dir='samples',
                         return_as_list=True,
                         truncate=None,
                         destination_path=None,
                         sample_delim='=' * 20 + '\n',
                         prefix=prefix,
                         seed=None,
                         nsamples=1,
                         batch_size=1,
                         length=1023,
                         temperature=0.7,
                         top_k=0,
                         top_p=0.0,
                         include_prefix=True)
