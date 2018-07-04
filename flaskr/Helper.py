import csv
import json
from pathlib import Path


class Helper(object):
    """Helper class.

    """
    @classmethod
    def getClusterClaims(cls, folderPath):
        """Get the cluster claims details for each cluster.

        Arguments:
            folderPath {Path} -- the path of data folder

        Returns:
            list -- the list contains rumor information
        """
        details = []
        with (folderPath / "corpus_cluster_claims_classification.csv").open() as fp:
            reader = csv.reader(fp, delimiter='\t')
            next(reader)
            for r in reader:
                details.append(r)
        return details

    @classmethod
    def getRepresentativeClaim(cls, folderPath):
        """Get the representative claim details for each cluster.

        Arguments:
            folderPath {Path} -- the path of data folder

        Returns:
            list -- the list contains statement inforamtion
        """
        with (folderPath / "corpus_representative_claims_classification.csv").open() as fp:
            reader = csv.reader(fp, delimiter='\t')
            next(reader)
            for r in reader:
                statement = r
        return statement

    @classmethod
    def getNews(cls, cluster, folderPath):
        """Get snippets for each statement.

        Arguments:
            folderPath {Path} -- the path of data folder
            index_statement {int} -- index of statement in csv file

        Returns:
            list -- the list contains statement information
        """
        with (cluster / "news" / (folderPath + "_news.json")).open() as fp:
            news = json.load(fp)
        return news

    @classmethod
    def getIndex(cls, folderPath):
        """Get index_statement_2_index_rumor for each cluster.

        Arguments:
            folderPath {Path} -- the path of data folder

        Returns:
            dict -- {index_tweet: index_statement}
        """
        with (folderPath / "index_tweet_2_index_candidate_statement.json").open() as fp:
            index = json.load(fp)
        return index
