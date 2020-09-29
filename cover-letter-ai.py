from letter_generator.cover_letter import generate_letter
from absl import flags
from absl import app

FLAGS = flags.FLAGS
flags.DEFINE_string('prefix', 'Dear Sirs, I am applying for', 'Cover letter start text')

def main(argv):

  response = generate_letter(prefix=FLAGS.prefix)
  output_letter = response[0].rsplit('<|endoftext|>')[0]

  print(output_letter)

if __name__ == '__main__':
      app.run(main)
