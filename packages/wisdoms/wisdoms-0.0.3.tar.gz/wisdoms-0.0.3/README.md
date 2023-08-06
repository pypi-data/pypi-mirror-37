# 天智信达的库

## 用法
1. 此库作为git项目管理，凡是修改完后应及时通知到开发团队
2. 需要使用库中的方法，需要将项目下载的本地，然后进入到项目中执行 python setup.py install,这时候就可以在项目中引用库中的方法
3. 引用的方法举例： 

## usage:

### auth.py:

    ``` python

        from wisdoms.auth import permit

        host = 'xxxx'

        auth = permit(host)

        class A:
            @auth
            def func():
                pass
    ```
### config.py

    ``` python

        from wisdoms.config import c
        c.get('name')
    ```

## 如何设计包
- 顶级包：wisdom，代表天智，智慧
- 现阶段的约定：采用一级包的方式
- 不同的功能放在不同的文件（模块）即可做好方法的分类
