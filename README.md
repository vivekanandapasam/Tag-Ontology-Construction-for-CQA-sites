# Tag-Ontology-Construction-for-CQA-sites
Constructing Tag onotlogy for QA sites

# Description of what each folder and files contains
1. datacsv - Contains csv files of posts and tags which are creates from xml files in super meta folder. It also creates nodes.csv and edges.csv which are created from Ontology.py file.

2. xml_to_csv - Converts the xml files in super meta folder to csv files

3. model - labelled LDA model

4. cleandata.py - reads the csv files in datacsv and created dictionaries of posts and tags

5. Ontology.py - creates edges for all the tags and saves common and similarity pickles(comm.p and sim.p) to the disk

6. communites.csv - communites obtained through online infomap tool https://www.mapequation.org/infomap/

7. succ_pred.py - takes cluster number as input and gives successor predecessor of that cluster as output in a csv file

8. parent_child.py - takes cluster number as input and produces gephi_egdes.csv files which has parent-child(subsumption edges) of that cluster

9. filter_parent_child.py - takes gephi_edges.csv as input and filters those edges like converting all tags to the head tags, removing duplicate edges, removing succ-pred edges,etc.

10. create_corpus.py - created corpus for glove(lda also in the similar manner).  Read this reference paper to understand how the corpus is created

11. siblings_glove - trains the glove model and gives siblings using only Glove

12. labelled_lda_training - trains the llda model.

13. siblings_lda - gives siblings using both LDA and Glove

14. filer_siblings.py - filters siblings just the same way parent-child relationships are filtered.

15. all_relationships.py - takes parent-child and siblings of a cluster as input and combines them to view how the relationships are.

16. concept_net.py - gives relationships from concept net

17. webosa.py - gives relationships from webisa

18. dbpedia_abstracts_catlinks.py - extracts abstracts and category links of tags from dbpedia.

19. Tag Ontologu for QA sites.pdf - presentation pdf 

