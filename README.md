## Project: Logs Analysis

This project is for practicing SQL skills by building a reporting tool 
that summarizes data from a large database.

### Description

The following files are included in the project: 
***proj1_log_analysis.py***: the python file for performing three database queries
`def query(sql, db_conn, the_tail)` is defined to reuse the database connection, which will reduce the load on the database.
***query3.sql***: as a long single query, putting into a separate .sql file to be read by python file is being used.  

An alternative way for the 3rd query is using views.
1. create view *not-found_vw* by
`CREATE VIEW not_found_vw AS
SELECT DATE(time) the_date, status, COUNT(DATE(time)) ctn
  FROM log
 WHERE status LIKE '%404%'
 GROUP BY DATE(time), status
 ORDER BY ctn DESC;`
2. create view *full_vw* by
` CREATE VIEW full_vw AS
 SELECT DATE(time) the_date, COUNT(DATE(time)) ctn
    FROM log
   GROUP BY DATE(time);`
3. Replace *query3.sql* content with the following query:
`SELECT TO_CHAR(a.the_date, 'fmMonth DD,YYYY'), TO_CHAR(((a.ctn::decimal / b.ctn::decimal) * 100.0)::float, 'FM999999990.00') || '%'
      FROM not_found_vw a, full_vw b
      WHERE a.the_date = b.the_date AND
           ((a.ctn::decimal / b.ctn::decimal) * 1) > 0.01
     LIMIT 10`

***proj1_log_analysis_output.txt***
***README.md***

### Getting Started
##### Dependencies

This project depends on correctly installing **vagrant** Linux-based virtual machine (VM) 

##### Installing

1. From Udacity    [Download data file here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)
2. Unzip the downloaded *newsdata.zip* to get the data file *newsdata.sql*, and put this file into */vagrant* directory
3. To load the data, *cd* into */vagrant* directory and type
`psql -d news -f newsdata.sql`
4. To exit, use
`\q`

##### Executing program

   To execute the program, please follow these steps:
   1. Navigate to */vagrant* directory where the program files are stored
   2. Bring up VM by typing `vagrant up`
   3. Type `vagrant ssh` to open Ubuntu vm
   4. Navigate to */vagrant* directory by `cd /vagrant` and run
   `vagrant@vagrant:/vagrant$ python proj1_log_analysis.py`

   To check Python code against the PEP 8 style conventions, please run:
   `vagrant@vagrant:/vagrant$ pycodestyle --first proj1_log_analysis.py`

### Authors

 Cong Li

### Version History

0.1 - Initial Release on 09-02-2019

### License

This project is licensed under the cl9451

### Acknowledgments

Inspiration, code snippets, etc.
    [google](https://www.google.com)
    [A simple README.md template](https://www.google.com/search?ei=HSZuXfTSA4PytAWiwYiwCA&q=A+simple+readme+template&oq=A+simple+readme+template&gs_l=psy-ab.3...44482.52255..52627...3.2..0.221.2303.0j13j1......0....1..gws-wiz.......0i71j35i304i39j0i7i30j0i13j0i8i7i30j0i8i30j35i39j33i10.9tafhYdHYAQ&ved=0ahUKEwi01cPon7TkAhUDOa0KHaIgAoYQ4dUDCAo&uact=5)
    [Udacity Writing READMEs](https://classroom.udacity.com/courses/ud777)
    [DILLINGER](https://dillinger.io/)
    