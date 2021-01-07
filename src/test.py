'''
Created on Feb 25, 2018

@author: dingyangchen
'''
import web_scrapping
import Graph
import json_storage_retrieval
import unittest


class Test(unittest.TestCase):

    def test_find_oldest_actor(self):
        actors=[('actor1',50,{1980:[('movie1','link1'),('movie2','link2')],1990:[('movie3','link3')]}),('actor2',60,{1980:[('movie1','link1')],2000:[('movie4','link4')]}), ('actor3',70,{2000:[('movie4','link4')]})]
        movies=[('movie1',1000,{'actor1':'link1','actor2':'link2'}),('movie2',2000,{'actor1':'link1'}),('movie3',3000,{'actor1':'link1'}),('movie4',4000,{'actor2':'link2','actor3':'link3'})]
        graph=Graph.Graph(movies,actors)
        self.assertTrue('actor3' in graph.find_oldest_actor(),"find_oldest_actor() return wrong value")
        
    def test_find_movie_grossing_value(self):
        actors=[('actor1',50,{1980:[('movie1','link1'),('movie2','link2')],1990:[('movie3','link3')]}),('actor2',60,{1980:[('movie1','link1')],2000:[('movie4','link4')]}), ('actor3',70,{2000:[('movie4','link4')]})]
        movies=[('movie1',1000,{'actor1':'link1','actor2':'link2'}),('movie2',2000,{'actor1':'link1'}),('movie3',3000,{'actor1':'link1'}),('movie4',4000,{'actor2':'link2','actor3':'link3'})]
        graph=Graph.Graph(movies,actors)
        self.assertTrue(graph.find_movie_grossing_value("movie1")==1000,"find_movie_grossing_value() return wrong value")
    
    def test_find_edge_weight(self):
        actors=[('actor1',50,{1980:[('movie1','link1'),('movie2','link2')],1990:[('movie3','link3')]}),('actor2',60,{1980:[('movie1','link1')],2000:[('movie4','link4')]}), ('actor3',70,{2000:[('movie4','link4')]})]
        movies=[('movie1',1000,{'actor1':'link1','actor2':'link2'}),('movie2',2000,{'actor1':'link1'}),('movie3',3000,{'actor1':'link1'}),('movie4',4000,{'actor2':'link2','actor3':'link3'})]
        graph=Graph.Graph(movies,actors)
        self.assertTrue(graph.find_edge_weight("movie1","actor1")==1000/50,"find_edge_weight() return wrong value")
        
    def test_find_most_gvalue_actor(self):
        actors=[('actor1',50,{1980:[('movie1','link1'),('movie2','link2')],1990:[('movie3','link3')]}),('actor2',60,{1980:[('movie1','link1')],2000:[('movie4','link4')]}), ('actor3',70,{2000:[('movie4','link4')]})]
        movies=[('movie1',10000,{'actor1':'link1','actor2':'link2'}),('movie2',2000,{'actor1':'link1'}),('movie3',3000,{'actor1':'link1'}),('movie4',4000,{'actor2':'link2','actor3':'link3'})]
        graph=Graph.Graph(movies,actors)
        self.assertTrue(graph.find_most_gvalue_actor()=="actor1","ffind_most_gvalue_actor() return wrong value")
    
    def test_find_filmography(self):
        actors=[('actor1',50,{1980:[('movie1','link1'),('movie2','link2')],1990:[('movie3','link3')]}),('actor2',60,{1980:[('movie1','link1')],2000:[('movie4','link4')]}), ('actor3',70,{2000:[('movie4','link4')]})]
        movies=[('movie1',10000,{'actor1':'link1','actor2':'link2'}),('movie2',2000,{'actor1':'link1'}),('movie3',3000,{'actor1':'link1'}),('movie4',4000,{'actor2':'link2','actor3':'link3'})]
        graph=Graph.Graph(movies,actors)
        filmography=graph.find_filmography('actor1')
        self.assertTrue(filmography[1980][0]==('movie1','link1'),"find_filmography() return wrong value")    
        self.assertTrue(filmography[1980][1]==('movie2','link2'),"find_filmography() return wrong value")    
        self.assertTrue(filmography[1990][0]==('movie3','link3'),"find_filmography() return wrong value") 
        
    def test_find_actors_of_movie(self):
        actors=[('actor1',50,{1980:[('movie1','link1'),('movie2','link2')],1990:[('movie3','link3')]}),('actor2',60,{1980:[('movie1','link1')],2000:[('movie4','link4')]}), ('actor3',70,{2000:[('movie4','link4')]})]
        movies=[('movie1',10000,{'actor1':'link1','actor2':'link2'}),('movie2',2000,{'actor1':'link1'}),('movie3',3000,{'actor1':'link1'}),('movie4',4000,{'actor2':'link2','actor3':'link3'})]
        graph=Graph.Graph(movies,actors)
        actor_of_movie=graph.find_actors_of_movie("movie1")
        self.assertTrue(actor_of_movie["actor1"]=="link1","find_actors_of_movie() return wrong value")
        self.assertTrue(actor_of_movie["actor2"]=="link2","find_actors_of_movie() return wrong value")
    
    def test_find_movies_of_year(self):
        actors=[('actor1',50,{1980:[('movie1','link1'),('movie2','link2')],1990:[('movie3','link3')]}),('actor2',60,{1980:[('movie1','link1')],2000:[('movie4','link4')]}), ('actor3',70,{2000:[('movie4','link4')]})]
        movies=[('movie1',10000,{'actor1':'link1','actor2':'link2'}),('movie2',2000,{'actor1':'link1'}),('movie3',3000,{'actor1':'link1'}),('movie4',4000,{'actor2':'link2','actor3':'link3'})]
        graph=Graph.Graph(movies,actors)
        self.assertTrue(graph.find_movies_of_year(1990)[0][0]=="movie3","find_movies_of_year() return wrong value")
        self.assertTrue(graph.find_movies_of_year(1990)[0][1]=="link3","find_movies_of_year() return wrong value")
        
    def test_find_actors_of_year(self):
        actors=[('actor1',50,{1980:[('movie1','link1'),('movie2','link2')],1990:[('movie3','link3')]}),('actor2',60,{1980:[('movie1','link1')],2000:[('movie4','link4')]}), ('actor3',70,{2000:[('movie4','link4')]})]
        movies=[('movie1',10000,{'actor1':'link1','actor2':'link2'}),('movie2',2000,{'actor1':'link1'}),('movie3',3000,{'actor1':'link1'}),('movie4',4000,{'actor2':'link2','actor3':'link3'})]
        graph=Graph.Graph(movies,actors)
        self.assertTrue(graph.find_actors_of_year(1968)[0]=="actor1","ffind_actors_of_year() return wrong value")
    
    def test_store_load_data(self):
        actors=[('actor1',50,{1980:[('movie1','link1'),('movie2','link2')],1990:[('movie3','link3')]}),('actor2',60,{1980:[('movie1','link1')],2000:[('movie4','link4')]}), ('actor3',70,{2000:[('movie4','link4')]})]
        movies=[('movie1',10000,{'actor1':'link1','actor2':'link2'}),('movie2',2000,{'actor1':'link1'}),('movie3',3000,{'actor1':'link1'}),('movie4',4000,{'actor2':'link2','actor3':'link3'})]
        json_storage_retrieval.store_data("/Users/dingyangchen/Desktop/CS242/actors.json",actors)
        json_storage_retrieval.store_data("/Users/dingyangchen/Desktop/CS242/movies.json",movies)
        load_actors=json_storage_retrieval.load_data("/Users/dingyangchen/Desktop/CS242/actors.json")
        load_movies=json_storage_retrieval.load_data("/Users/dingyangchen/Desktop/CS242/movies.json")
        self.assertTrue(len(load_actors)==len(actors),"data loaded is not the same as the original one")
        self.assertTrue(len(load_movies)==len(movies),"data loaded is not the same as the original one")
        graph=Graph.Graph(load_movies,load_actors)
        self.assertTrue('actor3' in graph.find_oldest_actor(),"data loaded is not the same as the original one")
        self.assertTrue(graph.find_actors_of_year(1968)[0]=="actor1","ffind_actors_of_year() return wrong value")
        actor_of_movie=graph.find_actors_of_movie("movie1")
        self.assertTrue(actor_of_movie["actor2"]=="link2","find_actors_of_movie() return wrong value")
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    