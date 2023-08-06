import unittest

from pipeline import execution_pipeline
from pipeline.cache.mock import MockCache
from pipeline.cache.redis import RedisCache
from pipeline.cache.memcache import MemCache


def do_thing_before(params):
    params['arg1'] = 'this argument is always changed'
    return params


def do_thing_after(response):
    if isinstance(response, dict):
        response['added'] = 'yup'
    return response


def do_another_thing_after(response):
    assert response['added'] == 'yup'  # the one that is first in the pipeline happens first.
    response['also_added'] = 'also yup'
    return response


def handle_this_error(e, response=None):
    print(f"oh no, Bob! {e}")
    return "Don't worry, we handled a TypeError."


def handle_that_error(e, response=None):
    print(f"oh no, Bob! {e}")
    return "Don't worry, we handled MyException."


class MyException(BaseException):
    pass


class TestPipeline(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.mock_cache = MockCache()
        cls.redis_cache = RedisCache()
        cls.mem_cache = MemCache()
        error_handlers = [
            {"exception_class": TypeError, "handler": handle_this_error},
            {"exception_class": MyException, "handler": handle_that_error},
        ]

        class A:

            @execution_pipeline(pre=[do_thing_before])
            def __init__(self, arg1='okay'):
                self.stored = arg1

            @execution_pipeline(pre=[do_thing_before], post=[do_thing_after])
            def fun_boys(self, arg1, arg4, arg2, arg3, thing=None):
                print(arg1, arg2, arg3, thing)
                return dict()

            @execution_pipeline(pre=[do_thing_before], post=[do_thing_after, do_another_thing_after], error=error_handlers)
            def fun_boys1(self, arg1, arg4, arg2, arg3, thing=None):
                return {'thing': thing}

            @execution_pipeline(pre=[do_thing_before], post=[do_thing_after], error=error_handlers)
            def fun_boys2(self, arg1, arg4, arg2, arg3, thing=None):
                raise MyException('Something went wrong!')


        class MC:
            @execution_pipeline(cache=cls.mock_cache)
            def fun_boys3(self, arg1, arg4, arg2, arg3, thing=None):
                return 500

        class RC:
            @execution_pipeline(cache=cls.redis_cache)
            def fun_boys3(self, arg1, arg4, arg2, arg3, thing=None):
                return 500

        class MMC:
            @execution_pipeline(cache=cls.mem_cache)
            def fun_boys3(self, arg1, arg4, arg2, arg3, thing=None):
                return 500

        cls.A = A
        cls.MC = MC
        cls.RC = RC
        cls.MMC = MMC

    def test_pre_execution_pipeline(self):
        a = self.A('sup')
        self.assertFalse(a.stored == 'sup')
        self.assertTrue(a.stored == 'this argument is always changed')

    def test_post_execution_pipeline(self):
        a = self.A()
        self.assertTrue(a.fun_boys(1, 2, 3, 4, 5)['added'] == 'yup')
        print(a.fun_boys1(1, 2, 3, 4, 5))
        self.assertTrue(a.fun_boys1(1, 2, 3, 4, 5)['also_added'] == 'also yup')

    def test_error_pipeline(self):
        a = self.A()
        self.assertEqual(a.fun_boys2(), "Don't worry, we handled a TypeError.")  # handles TypeError
        self.assertEqual(a.fun_boys2(1, 2, 3, 4, 5), "Don't worry, we handled MyException.")  # handles MyException

    def test_cache_pipeline(self):

        mc = self.MC()
        self.assertEqual(mc.fun_boys3(1, 2, 3, 4, 5), 500)
        self.mock_cache.set("fun_boys3:{'thing':_5,_'arg1':_1,_'arg4':_2,_'arg2':_3,_'arg3':_4}", 200, 5)
        self.assertEqual(mc.fun_boys3(1, 2, 3, 4, 5), 200)

        rc = self.RC()
        self.assertEqual(rc.fun_boys3(1, 2, 3, 4, 5), 500)
        self.redis_cache.set("fun_boys3:{'thing':_5,_'arg1':_1,_'arg4':_2,_'arg2':_3,_'arg3':_4}", 300, 5)
        self.assertEqual(rc.fun_boys3(1, 2, 3, 4, 5), 300)

        mmc = self.MMC()
        self.assertEqual(mmc.fun_boys3(1, 2, 3, 4, 5), 500)
        self.mem_cache.set("fun_boys3:{'thing':_5,_'arg1':_1,_'arg4':_2,_'arg2':_3,_'arg3':_4}", 400, 5)
        self.assertEqual(mmc.fun_boys3(1, 2, 3, 4, 5), 400)




