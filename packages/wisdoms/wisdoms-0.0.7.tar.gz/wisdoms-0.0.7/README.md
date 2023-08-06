# 天智信达的库

## 用法
1. 此库作为git项目管理，凡是修改完后应及时通知到开发团队
2. 需要使用库中的方法，需要将项目下载的本地，然后进入到项目中执行 python setup.py install,这时候就可以在项目中引用库中的方法
3. 引用的方法举例： 

#### install

- pip install wisdoms

#### find the latest package of wisdoms
- pip list --outdated

#### upgrade
- pip install wisdoms --upgrade

---------------------------

#### generation

Make sure you installed setuptools and wheel.

Important: You must modify the version of the package in setup.py and delete folders (build, dist, egg-info)
- python setup.py sdist bdist_wheel

#### upload

Install twine before doing this
- twine upload dist/*

## packet usage:

#### auth.py:

``` python

    from wisdoms.auth import permit

    host ={'AMQP_URI': "amqp://guest:guest@localhost"}

    auth = permit(host)

    class A:
        @auth
        def func():
            pass
```

#### config.py

``` python

    from wisdoms.config import c

    # gains item of YML config
    print(c.get('name'))

    # transforms class into dict
    d = c.to_dict()
    print(d['name'])

```

#### common.py

``` python

    from wisdoms.commons import revert, codes

    def func():
        # do something

        # return revert(codes.code) or return revert(number)
        return revert(1)

        return revert(codes.SUCCESS)

```

## 如何设计包
- 顶级包：wisdom，代表天智，智慧
- 现阶段的约定：采用一级包的方式
- 不同的功能放在不同的文件（模块）即可做好方法的分类