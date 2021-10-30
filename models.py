# utils
import json
from utils import get,post,BASE_URL

# typing
from typing import Dict, List


class Dog(object):
    """
    Dog object that is composed of the id, name and breed of the dog

    To initialize:
    :param id: dog id
    :param name: dog name
    :param breed: dog breed id

    USAGE:
        >>> dog = Dog(id=1, name='Bobby', breed=1)
    """
    def __init__(self, id: int, name: str, breed: int):
        self.id = id
        self.name = name
        self.breed = breed


class Breed(object):
    """
    Breed object that is composed of the id and the name of the breed.

    To initialize:
    :param id: breed id
    :param name: breed name

    Also, breed has a list of dogs for development purposes
    :field dogs: breed dog list

    USAGE:
        >>> breed = Breed(id=1, name='Kiltro')
        >>> dog = Dog(id=1, name='Cachupin', breed=breed.id)
        >>> breed.add_dog(dog)
        >>> breed.dogs_count()
        1
    """
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
        self.dogs: List[Dog] = []

    def add_dog(self, dog: Dog):
        self.dogs.append(dog)

    def dogs_count(self) -> int:
        return len(self.dogs)


class DogHouse(object):
    """
    Doghouse object that manipulates information on breeds and dogs.
    We expect you implement all the methods that are not implemented
    so that the flow works correctly


    DogHouse has a list of breeds and a list of dogs.
    :field breeds: breed list
    :field dogs: dog list

    USAGE:
        >>> dog_house = DogHouse()
        >>> dog_house.get_data(token='some_token')
        >>> total_dogs = dog_house.get_total_dogs()
        >>> common_breed = dog_house.get_common_breed()
        >>> common_dog_name = dog_house.get_common_dog_name()
        >>> total_breeds = dog_house.get_total_breeds()
        >>> data = {  # add some data
        ...     'total_dogs': total_dogs,
        ...     'total_breeds': total_breeds,
        ...     'common_breed': common_breed.name,
        ...     'common_dog_name': common_dog_name,
        ... }
        >>> token = 'some token'
        >>> dog_house.send_data(data=data, token=token)
    """

    __API_URL="/api/v1"
    __url_breeds=BASE_URL+__API_URL+"/breeds/"
    __url_dogs=BASE_URL+__API_URL+"/dogs/"
    __url_answer=BASE_URL+__API_URL+"/answer/"

    def __init__(self):
        self.breeds: List[Breed] = []
        self.dogs: List[Dog] = []

    def get_data(self, token: str):
        """
        You must get breeds and dogs data from our API: http://dogs.magnet.cl

        We recommend using the Dog and Breed classes to store
        the information, also consider the dogs and breeds fields
        of the DogHouse class to perform data manipulation.
        """
        self.__getBreeds(token)
        self.__getDogs(token)
        self.__fillBreedsWithDogs()

    def __getBreeds(self,token):
        breedDictionaryList=self.__getBreedDictionaryList(token=token)
        self.breeds=self.__getBreedObjectList(breedDictionaryList)
        
    
    def __getDogs(self,token):
        dogDictionaryList=self.__getDogDictionaryList(token=token)
        self.dogs=self.dogs=self.__getDogObjectList(dogDictionaryList)  

    def __fillBreedsWithDogs(self):
        for breed in self.breeds:
            for dog in self.dogs:
                if breed.id == dog.breed:
                    breed.add_dog(dog=dog)

    def __getBreedObjectList(self,breedDictionaryList) -> List[Breed]:
        return list(map(self.__parseDictionaryItemToBreed,breedDictionaryList))

    def __getDogObjectList(self,dogDictionaryList) -> List[Dog]:
        return list(map(self.__parseDictionaryItemToDog,dogDictionaryList))

    def __parseDictionaryItemToBreed(self,itemDict:dict) -> Breed:
        return Breed(id=itemDict["id"],name=itemDict["name"])

    def __parseDictionaryItemToDog(self,itemDict:dict) -> Dog:
        return Dog(id=itemDict["id"],name=itemDict["name"],breed=itemDict["breed"])

    def __getBreedDictionaryList(self,token:str) -> List[Dict]:
        return get(url=self.__url_breeds,token=token)["results"]
    
    def __getDogDictionaryList(self,token:str) -> List[Dict]:
        return get(url=self.__url_dogs,token=token)["results"]


    def get_total_breeds(self) -> int:
        """
        Returns the amount of different breeds in the doghouse
        """
        return len(self.breeds)

    def get_total_dogs(self) -> int:
        """
        Returns the amount of dogs in the doghouse
        """
        return len(self.dogs)

    def get_common_breed(self) -> Breed:
        """
        Returns the most common breed in the doghouse

        If there are 2 or more breed with the same high number (including 0):
            I am returning the first one (depends on the policy)
        """

        mostPopularBreed=self.breeds[0]
        for breed in self.breeds:
            if breed.dogs_count()>mostPopularBreed.dogs_count():
                mostPopularBreed=breed
                
        return mostPopularBreed

    def get_common_dog_name(self) -> str:
        """
        Returns the most common dog name in the doghouse
        """

        mostPopularDogName=self.dogs[0].name
        highestAmount=1
        dictAmountsDogsWithName={}

        for dog in self.dogs:
            if dog.name in dictAmountsDogsWithName:
                dictAmountsDogsWithName[dog.name]+=1
            else:
                dictAmountsDogsWithName[dog.name]=1

            if dictAmountsDogsWithName[dog.name]>highestAmount:
                highestAmount=dictAmountsDogsWithName[dog.name]
                mostPopularDogName=dog.name

        return mostPopularDogName


    def send_data(self, data: dict, token: str):
        """
        You must send the answers obtained from the implemented
        methods, the parameters are defined in the documentation.

        Important!! We don't tell you if the answer is correct
        """
        response=post(url=self.__url_answer,data=data,token=token)
        print(response)
