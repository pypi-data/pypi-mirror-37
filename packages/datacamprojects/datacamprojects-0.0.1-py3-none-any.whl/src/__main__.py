import argparse
from pipeline import classify, regress


def main():
    parser = argparse.ArgumentParser(description='Scikit-learn datasets only!')
    parser.add_argument('--dataset', '-d', default='diabetes')
    parser.add_argument('--model', '-m', default='linear_model.BayesianRidge')
    args = parser.parse_args()
    kwargs = dict(dataset=args.dataset, model=args.model)
    return (classify(**kwargs) if args.dataset in ('digits', 'iris', 'wine')
            else regress(**kwargs) if args.dataset in ('boston', 'diabetes')
            else print(f'{args.data} is not a supported dataset!'))


if __name__ == "__main__":
    main()
