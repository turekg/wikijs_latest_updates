#!/usr/bin/python
import psycopg2
import argparse
from configobj import ConfigObj


def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        config = read_config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(host=config['dbhost'], database=config['dbname'], user=config['dbuser'], password=config['dbpwd'])
        
        # create a cursor
        cur = conn.cursor()
        
        # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)
       
        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

def read_config():
    # Configuration file (required, assume it's in the same dir as script, option to specify a new config available)
    config_file = 'wikijs_updates.conf'
    
    # Set up argument parser (none required)
    parser = argparse.ArgumentParser(description='Process input arguments.')
    parser.add_argument('-c', metavar='<config_file>', dest='config_file', help='Absolute path to config file. If not present, will look for ./wikijs_updates.conf')

    # Parse arguments
    args = parser.parse_args()
    
    if (args.config_file != None):
        config_file = args.config_file
    
    # Read config file
    try:
        config = ConfigObj(config_file)
        return config
    except IOError:
        print("Error: config file not found or unreadable.\n")
        sys.exit(1)
    
if __name__ == '__main__':
    connect()