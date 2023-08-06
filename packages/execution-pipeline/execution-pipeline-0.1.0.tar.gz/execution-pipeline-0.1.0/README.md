# python-pipeline

This library allows users to easily wrap functions with a series of decorators. This is useful in scenarios where input needs to be cleaned and output needs to be processed in a systematic way.


## Usage
A pipeline consists of four optional segments
### Pre
The `pre` execution segment allows you to modify any input parameters passed to the decorated function. Any functions 
passed to the `pre` segment will always be executed first.

    from pipeline import execution_pipeline

    def do_thing_before(params):
        params['arg1'] = 'okay'
        return params


    @execution_pipeline(pre=[do_thing_before])
    def do_thing(arg1=5):
        return arg1*10
     
    
    
    do_thing()
    # okayokayokayokayokayokayokayokayokayokay


### Post
The `post` execution segment allows you to modify or handle the result after the decorated function has already run.

    def do_thing_after(response):
        response['added'] = 'yup'
        return response
        
        
    @execution_pipeline(post=[do_thing_after])
    def do_thing(**kwargs):
        return {**kwargs}  # just make a new dictionary using the passed keyword arguments
        
        
    do_thing(apples=2, oranges=3, bananas=0)
     # {'apples': 2, 'oranges': 3, 'bananas': 0, 'added': 'yup'}
     
Just like the other segments, you can use as many post processing functions as you need; they will be executed in the order
that they are passed.


    def do_another_thing_after(response):
        assert response['added'] == 'yup' # the one that is first in the pipeline happens first.
        response['also_added'] = 'also yup'
        return response
    
    
    @execution_pipeline(post=[do_thing_after, do_another_thing_after])
    def do_thing(**kwargs):
        return {**kwargs}
        
     
    do_thing()
    # {'apples': 2, 'oranges': 3, 'bananas': 0, 'added': 'yup', 'also_added': 'also yup'}
        
### Error
The `error` execution segment allows you to pass error handling to log, modify, absorb, etc. any exceptions that are 
raised by the wrapped function.


    class MyException(BaseException):
        pass
    
    def handle_this_error(e, response=None):
        print(f"oh no, Bob! {e}")
        return "Don't worry, we handled a TypeError."
    
    
    def handle_that_error(e, response=None):
        print(f"oh no, Bob! {e}")
        return "Don't worry, we handled MyException."
        
    error_handlers = [
        {"exception_class": TypeError, "handler": handle_this_error},
        {"exception_class": MyException, "handler": handle_that_error},
    ]
    
    
    @execution_pipeline(pre=[do_thing_before], post=[do_thing_after], error=error_handlers)
    def fun_boys(arg1, arg4, arg2, arg3, thing=None):
        raise MyException('Something went wrong!')
        
    
    result = fun_boys(1, 2, 3, 4, 5)
    # oh no, Bob! Something went wrong!
    
    print(result) 
    # Don't worry, we handled MyException.
    
### Cache
The `cache` execution segment will record all arguments (before and after the `pre` segment) and store the result 
(after the `post` and `error` segments) in cache using a string constructed from the arguments as a key. 

    from pipeline.cache.mock import MockCache
    # MockCache is basically just a dict() with some expiration convenience methods.
    mock_cache = MockCache()
    
    @execution_pipeline(cache=mock_cache)
    def fun_boys(arg1, arg4, arg2, arg3, thing=None):
        return 500
        
    fun_boys(1, 2, 3, 4, 5)
    # 500
    
    mock_cache.set("fun_boys:{'thing':_5,_'arg1':_1,_'arg4':_2,_'arg2':_3,_'arg3':_4}", 200, 5)
    # True to indicate successful setting of key
    
    fun_boys(1, 2, 3, 4, 5)
    # 200
        
#### Supported Cache Backends
Note: if the appropriate backend is not installed, they will be replaced with a `MockCache` instance at runtime. This 
is intended to improve portability of pipeline code. 

##### Redis
```
pip install redis
```
And then same as above except with

    from pipeline.cache.redis import RedisCache
    redis = RedisCache(host='localhost', port=6379) # defaults
    
    
##### MemCached
```
pip install memcached
```
And then the same as above except with

    from pipeline.cache.mem_cache import MemCache 
    mem_cache = MemCache(host='localhost', port=11211) # defaults

