# amieci
The python client for amie.ai.

Install with 

`pip install amieci`

### Documentation
A tutorial notebook to get you started is [here](https://github.com/disraptoer/resources/blob/master/tutorial.ipynb "amieci tutorial notebook").

More notebooks that show you how to integrate amie in your measurement and data-science workflows [here](https://github.com/disraptoer/resources "amieci resources").



### Installation

Sign up (free) on www.amie.ai and obtain an API key after you're logged in under [www.amie.ai/#/user]("www.amie.ai/#/user")

Then sign in from python, and load the garden. 

``` 
garden = amieci.Garden(key=your_key)
garden.load()
...
```
The fundamental object in amie is the garden. It contains all trees and leaves and remembers how your data interconnects.

Every day, valuable data and results get lost and forgotten. amie provides you with an easy way to structure and store your results. It does not only store your data, 
but also their relationships, to make sure your workflow is fully reproducible and make it easy for you to keep an overview. 
amie works with any data-driven task, from data-science to beer brewing.

