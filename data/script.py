import click
import os
from pathlib import Path
import shutil


def moveFile(folderpath):
    classification = folderpath / 'final' / 'classification'
    # news = folderpath / 'news'
    cluster = folderpath / "clusterData" / "0"
    cluster.mkdir(parents=True)
    shutil.move(str(classification), str(cluster))
    # shutil.move(str(news), str(cluster))
    shutil.rmtree(str(folderpath / 'final'))
    # shutil.rmtree(str(folderpath / 'experiment'))

    # newClusterPath = folderpath / 'clusterData'
    # newClustersPath = [x for x in newClusterPath.iterdir() if x.is_dir()]
    # for cp in newClustersPath:
    #     # shutil.move(str(cp / 'final' / 'corpus.csv'), str(cp))
    #     # shutil.move(str(cp / 'final' / 'corpus_statements.csv'), str(cp))
    #     if not (cp / 'final' / 'index_tweet_2_index_candidate_statement.json').exists():
    #         shutil.rmtree(str(cp))
    #         continue
    #     shutil.move(str(cp / 'final' / 'index_tweet_2_index_candidate_statement.json'), str(cp))
    #     shutil.move(str(cp / 'final' / 'index_candidate_statement_2_index_tweet.json'), str(cp))
    #     shutil.move(str(cp / 'final' / 'snippets.json'), str(cp))
    #     shutil.move(str(cp / 'final' / 'corpus_classification.csv'), str(cp))
    #     shutil.move(str(cp / 'final' / 'corpus_statements_classification.csv'), str(cp))
    #     shutil.move(str(cp / 'final' / 'corpus_snippets_classification.csv'), str(cp))
    #     shutil.rmtree(str(cp / 'final'))


@click.command()
@click.option('--foldername')
def main(foldername):
    folderpath = Path(foldername)
    # newfolderpath = [x for x in folderpath.iterdir() if x.is_dir()]
    # for np in newfolderpath:
    moveFile(folderpath)


main()
