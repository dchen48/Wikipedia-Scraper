from datetime import date 
class Movie_Node:
    
    def __init__(self,name,box_office,actors):
        '''
        constructor for class Movie_Node
        @param name: name of the movie
        @param box_office: box office of the movie
        @param actors: list of actors of the movie
        @return a Movie_Node object
        '''
        self.name=name
        self.box_office=box_office
        self.actors=actors
        
class Actor_Node:
    def __init__(self,name,age,filmography):
        '''
        constructor for class Actor_Node
        @param name: name of the actor
        @param age: age of the actor
        @param filmography: list of films that the actor participate
        @return an Actor_Node object
        '''
        self.name=name
        self.age=age
        self.filmography=filmography    
        

class Graph:
    def __init__(self,movies,actors):
        '''
        constructor for class Graph
        @param movies: a list of movies
        @param actors: a list of actors
        @return an actor object
        '''
        self.movie_nodes=[]
        self.actor_nodes=[]
        for actor in actors:
            self.actor_nodes.append(Actor_Node(actor[0],actor[1],actor[2]))
        for movie in movies:
            self.movie_nodes.append(Movie_Node(movie[0],movie[1],movie[2]))
    
    def find_movie_grossing_value(self,movie_name):
        '''
        find grossing value of  a movie
        @movie_name: name of the movie
        @return grossing value of  a movie
        '''
        for Movie_Node in self.movie_nodes:
            if Movie_Node.name==movie_name:
                return Movie_Node.box_office
        print("log no such movie found")
        return -1
    
    def find_edge_weight(self,movie_name,actor_name):
        '''
        find weighted edge between a movie and an actor
        @movie_name: name of the movie
         @actor_name: name of the actor
        @return weighted edge between a movie and an actor
        '''
        movie=None
        actor=None
        for Movie_Node in self.movie_nodes:
            if Movie_Node.name==movie_name:
                movie=Movie_Node
        for Actor_Node in self.actor_nodes:
            if Actor_Node.name==actor_name:
                actor=Actor_Node
        if (movie!=None and actor!=None):
            for actor_movies in actor.filmography.values():
                for actor_movie in actor_movies:       
                    if ((actor_movie[0] in movie_name) or (movie_name in actor_movie[0])):
                        return movie.box_office/actor.age
        return 0
    
    def find_most_gvalue_actor(self):
        '''
        find the actor with the highest grossing value
        @movie_name: name of the movie
        @return the actor with the highest grossing value
        '''
        most_gvalue_actor=None
        for Actor_Node in self.actor_nodes:
            if (most_gvalue_actor==None):
                most_gvalue_actor=Actor_Node
            else:
                v1=0
                v2=0
                for films in most_gvalue_actor.filmography.values():
                    for film in films:
                        v1=v1+self.find_edge_weight(film[0],most_gvalue_actor.name)
                for films in Actor_Node.filmography.values():
                    for film in films:
                        v2=v2+self.find_edge_weight(film[0],Actor_Node.name)  
                if (v2>v1):
                    most_gvalue_actor=Actor_Node
        return most_gvalue_actor.name
        
        
        
    def find_filmography(self,actor_name):
        '''
        find filmography of an actor
        @actor_name: name of the actor
        @return dictionary of films that the actor participate
        '''
        for Actor_Node in self.actor_nodes:
            if Actor_Node.name==actor_name:
                return Actor_Node.filmography
        print("log no such actor found")
        return {}
    
    def find_actors_of_movie(self,movie_name):
        '''
        find cast of a movie
        @movie_name: name of the movie
        @return cast of a movie
        '''
        for Movie_Node in self.movie_nodes:
            if Movie_Node.name==movie_name:
                return Movie_Node.actors
        print("log no such movie found")
        return {}
    
    def find_oldest_actor(self):
        '''
        find oldest actor in the graph
        @return oldest actor in the graph
        '''
        oldest_actors=[]
        for Actor_Node in self.actor_nodes:
            #print("name: ",Actor_Node.name)
            if (oldest_actors==[]):
                oldest_actors=[Actor_Node]
            else:
                if Actor_Node.age>oldest_actors[0].age:
                    oldest_actors=[Actor_Node]
                elif Actor_Node.age==oldest_actors[0].age:
                    oldest_actors.append(Actor_Node)
                else:
                    continue
        ret=[]
        for oldest_actor in oldest_actors:
            ret.append(oldest_actor.name)
        return ret
    
    def find_movies_of_year(self,year):
        '''
        find movies released in a given year
        @year: year
        @return list of movies in released in a given year
        '''
        movies=[]
        for Actor_Node in self.actor_nodes:
            #print("Actor_Node.filmography: ",Actor_Node.filmography)
            for movie_year,Movie_Node in (Actor_Node.filmography.items()):
                if (movie_year==year):
                    movies=movies+Movie_Node
        return movies
    
    def find_actors_of_year(self,year):
        '''
        find actors born in a given year
        @year: year
        @return list of actors born in a given year
        '''
        actors=[]
        for Actor_Node in self.actor_nodes:
            birth_year=date.today().year-Actor_Node.age
            if (birth_year==year):
                    actors.append(Actor_Node)
        ret=[]
        for actor in actors:
            ret.append(actor.name)
        return ret