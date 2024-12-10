from yannakakis.db import Database
from yannakakis.yannakakis import Yannakakis
from yannakakis.jobdataset.JobQuery1A import JobQuery1A
from yannakakis.jobdataset.JobQuery5C import JobQuery5C
from yannakakis.jobdataset.JobQuery5B import JobQuery5B
from yannakakis.jobdataset.JobQuery6E import JobQuery6E
import logging
import itertools


def generate_join_tree_permutations(join_tree):
    """
    Generate valid permutations of the join tree.
    
    A valid permutation must maintain the connection between tables 
    through their join keys.
    
    Args:
    join_tree (list): List of dictionaries representing joins between tables
    
    Returns:
    list: List of valid join tree permutations
    """
    def is_valid_permutation(perm):
        """
        Check if a permutation maintains table connections.
        
        Args:
        perm (list): A permutation of join tree entries
        
        Returns:
        bool: True if the permutation is valid, False otherwise
        """
        # Track tables that have been connected
        connected_tables = set()
        
        # Start with the first join's left and right tables
        first_join = perm[0]
        connected_tables.add(first_join['left'])
        connected_tables.add(first_join['right'])
        
        # Check subsequent joins
        for join in perm[1:]:
            # Check if either left or right table is already connected
            if (join['left'] in connected_tables or 
                join['right'] in connected_tables):
                # Add both tables to connected set
                connected_tables.add(join['left'])
                connected_tables.add(join['right'])
            else:
                # This join doesn't connect to previous joins
                return False
        
        return True
    
    # Generate all permutations
    valid_permutations = []
    for perm in itertools.permutations(join_tree):
        # Convert permutation to list for mutability
        perm_list = list(perm)
        
        # Check if this permutation maintains connections
        if is_valid_permutation(perm_list):
            valid_permutations.append(perm_list)
    
    return valid_permutations


try:

    # Clean the log file first 
    # with open("test.log", "w") as file:
    #     pass 

    # Set the log details
    logging.basicConfig(
        filename="test.log",
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logger = logging.getLogger(__name__)

    # Connect to the database and load the job dataset params
    db = Database()
    job = JobQuery5C()

    # Load tables from the database
    tables = {
        table_name: db.fetch_table_from_db(table_name, columns, db.connection)
        for table_name, columns in job.columns.items()
    }

    # Run Yannakakis
    logger.setLevel(logging.INFO)
    test = [{'left': 'movie_companies', 'right': 'movie_info', 'left_key': 'movie_id', 'right_key': 'movie_id'}, {'left': 'company_type', 'right': 'movie_companies', 'left_key': 'id', 'right_key': 'company_type_id'}, {'left': 'title', 'right': 'movie_info', 'left_key': 'id', 'right_key': 'movie_id'}, {'left': 'movie_companies', 'right': 'title', 'left_key': 'movie_id', 'right_key': 'id'}, {'left': 'movie_info', 'right': 'info_type', 'left_key': 'info_type_id', 'right_key': 'id'}]
    yannakakis = Yannakakis(tables, test, job.selection_criteria, job.projection_criteria, logger, logging, False)

except Exception as e:
    logger.setLevel(logging.ERROR)
    logger.error(f"Error occurred :  {e}")
finally:
    db.closeConnection()
