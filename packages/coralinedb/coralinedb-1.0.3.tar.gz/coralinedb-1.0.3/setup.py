from distutils.core import setup
from setuptools import find_packages

setup(
    name='coralinedb',
    packages=find_packages(),
    version='1.0.3',
    description='Coraline Database Manager Package',
    long_description="""
    Coraline Database Manager Package
    *Now, only SQL DB is supported*  
      
    -**How to use**-
    
    1. Initial database object by specify host, username and password  
         
        
        from coralinedb import SQLDB \n
        sql_db = SQLDB(host, username, password)
        
    
    2. Load a table or multiple tables 
    
        new_table = sql_db.load_table("database_name", "table_name")
    
        or  
      
        table1, table2 = sql_db.load_table("database_name", ["table_name1", "table_name2"])  
    
    3. Save a dataframe to a table
         
        sql_db.save_table(df, "database_name", "table_name")
         
    4. Get number of rows of a table
     
        n_rows = sql_db.get_count("database_name", "table_name")  
         
    5. Run other SQL statement on host (with or without database name) 
    
        table = sql_db.query("show databases;") \n
        table = sql_db.query("SELECT * FROM ...", "database_name")
    
    """,
    author='Jiranun J.',
    author_email='jiranun@coraline.co.th',
    url='https://www.coraline.co.th',
    keywords=['sql', 'database', 'db', 'coraline'],
    python_requires='>=3.6',
    classifiers=['Programming Language :: Python',
                 'Programming Language :: SQL',
                 'Development Status :: 4 - Beta',
                 'Intended Audience :: Developers',
                 'Intended Audience :: Science/Research',
                 'License :: OSI Approved :: MIT License',
                 'Natural Language :: English',
                 'Topic :: Database',
                 ],
    install_requires=['pandas',
                      'sqlalchemy',
                      'pymysql',
                      ],
    entry_points={
        'console_scripts': [
            'coralinedb=coralinedb.coralinedb:print_help',
        ],
    },
    # include_dirs=[numpy.get_include()]
)

