import csv
import json
from pathlib import Path

class Helper(object):
    """Helper class.
    
    """
    @classmethod
    def getRumors(cls, folderPath):
        """Get the tweets details for each cluster.
        
        Arguments:
            folderPath {Path} -- the path of data folder
        
        Returns:
            list -- the list contains rumor information
        """
        details = []
        with (folderPath / "corpus_classification.csv").open() as fp:
            reader = csv.reader(fp, delimiter='\t')
            next(reader)
            for r in reader:
                details.append(r)
        return details

    @classmethod
    def getStatements(cls, folderPath):
        """Get the statements details for each cluster.
        
        Arguments:
            folderPath {Path} -- the path of data folder
        
        Returns:
            list -- the list contains statement inforamtion
        """
        statements = []
        with (folderPath / "corpus_statements_classification.csv").open() as fp:
            reader = csv.reader(fp, delimiter='\t')
            next(reader)
            for r in reader:
                statements.append(r)
        return statements

    @classmethod
    def getSnippets(cls, folderPath, index_statement):
        """Get snippets for each statement.
        
        Arguments:
            folderPath {Path} -- the path of data folder
            index_statement {int} -- index of statement in csv file
        
        Returns:
            list -- the list contains statement information
        """
        snippets = []
        with (folderPath / "corpus_snippets_classification.csv").open() as fp:
            reader = csv.reader(fp, delimiter='\t')
            next(reader)
            for r in reader:
                if r[6][0] == index_statement:
                    snippets.append(r)
        return snippets

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