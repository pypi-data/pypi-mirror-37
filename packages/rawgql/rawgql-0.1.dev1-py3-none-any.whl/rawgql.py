import os
import json
import requests


GQL_FOLDER = os.environ.get('GQL_FOLDER')
if GQL_FOLDER is None:
    GQL_FOLDER = os.path.join(os.getcwd(), 'gql')

FRAGMENTS_FILE = os.environ.get('GQL_FRAGMENTS_FILE')
if FRAGMENTS_FILE is None:
    FRAGMENTS_FILE = 'fragments.gql'

AUTH_FILE = os.environ.get('GQL_AUTH_FILE')
if AUTH_FILE is None:
    AUTH_FILE = 'auth.json'


class GraphQL:
    """Backend class for interacting with a Prisma GraphQL API."""

    def __init__(self, endpoint):
        with open(os.path.join(GQL_FOLDER, AUTH_FILE), 'r') as auth:
            self.headers = json.load(auth)
        self.headers['Content-Type'] = 'application/json'
        self.endpoint = endpoint

    def query(self, q, variables=None):
        """
        Run a GraphQL Query/Mutation and get the server response
        in json format. If only positional arguments are used,
        the method will attempt to open the first argument as a file
        within the folder set by GQL_FOLDER.

        Args:
            q (str): The .gql file or raw string to run; tests if file
                     located in GQL_FOLDER
            variables (dict): Replacement variables for query placeholders;
                              defaults to None

        Returns:
            A json object containing response data from the server.
        """
        fragments_path = os.path.join(GQL_FOLDER, FRAGMENTS_FILE)
        if os.path.exists(fragments_path):
            with open(fragments_path, 'r') as ff:
                fragments = ff.read()
        else:
            fragments = '' 

        query_path = os.path.join(GQL_FOLDER, q)
        if os.path.exists(query_path):
            with open(query_path, 'r') as qf:
                query = qf.read()
        else:
            query = q

        r = requests.post(self.endpoint,
                          json={'query': fragments + query,
                                'variables': variables},
                          headers=self.headers)

        data = r.json()
        return data


if __name__ == '__main__':
    pass
