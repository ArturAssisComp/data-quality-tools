import argparse


parser = argparse.ArgumentParser(
    description='A toolkit for data quality. It helps you to generate data quality'
                ' reports about structured data.',
    epilog='For more information, visit https://github.com/ArturAssisComp/data-quality-tools#readme',
    )

parser.add_argument("--version", action="version", version="data-quality-tools 0.0.1")

def main():
    parser.parse_args()







if __name__ == "__main__":
    main()