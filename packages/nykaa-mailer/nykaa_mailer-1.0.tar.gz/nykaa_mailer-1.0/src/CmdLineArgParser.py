import argparse
from src import NNRecMailer

parser = argparse.ArgumentParser(description='Generate NN Recommendations')
parser.add_argument('--output-path', dest='output', type=str,
                    help='output file for the generated content')
parser.add_argument('--nn-path', dest='nn_path', type=str,
                    help='nykaa network post path')
parser.add_argument('--description', dest='description', type=str,
                    help='description content')

args = parser.parse_args()

NNRecMailer.NNRecMailer().run(args.nn_path, args.description ,args.output)