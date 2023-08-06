FlaskCap
########

FlaskCap是一个基于flask封装的Web框架，集成了orator和DBUtils来提供数据库ORM及连接池的支持，并包含了一些工具类和易于使用的特性。

安装
====

使用pip安装和更新flaskcap:

.. code-block:: bash

    pip install flaskcap


示例
====

flaskcap
--------

* flaskcap 的使用与flask一致。

.. code-block:: python

    from flaskcap import FlaskCap
    from flaskcap import jsonify

    app = FlaskCap(__name__)

    @app.route('/foo')
    def foo():
        return 'Hello World'

    @app.route('/bar')
    def bar():
        return jsonify({'hello': 'world'})

    if __name__ == '__main__':
        app.run()


* 通过 g 获取请求参数

::

    flaskcap 将HTTP请求参数(文件参数除外)封装在 `g.request_payload` 中，包含表单及JSON参数。

.. code-block:: python

    from flaskcap import g, jsonify

    @app.route('/', methods=['GET', 'POST'])
    def index():
        return jsonify(g.request_payload)



* 日志分割

::

    flaskcap 提供一个跨平台的可按自然时间进行日志分割的实现，`NaturalTimedRotating`。
    该实现是进程安全的，并且支持日志文件丢失后自动重建。

.. code-block:: python

    from flaskcap import NaturalTimedRotating

    logger_handler = NaturalTimedRotating('app.log', backupCount=7)


* 访问日志

::

    flaskcap 提供了请求日志处理的注册方法，并提供了 `elapsed_time` 值记录请求处理时间

.. code-block:: python

    from flaskcap import current_app

    app.access_logger.addHandler(NaturalTimedRotating('access.log'))

    @app.log_access
    def access_func(request, response):
        current_app.access_logger.info('Request takes %s seconds' % current_app.elapsed_time)


orm
----

* orm的使用与orator一致，请参见orator的使用。

.. code-block:: python

    from flaskcap import FlaskCap
    from flaskcap.orator import Orator

    app = FlaskCap(__name__)

    app.config['DATABASE'] = {
        'mysql': {
            'driver': 'mysql',
            'host': 'localhost',
            'database': 'db',
            'user': 'user',
            'password': 'password',
            # 是否开启慢查询日志，默认关闭
            'log_slow_query': True,
            # 慢查询时间阀值(毫秒)，默认2000
            'slow_query_time': 3000,
            # 连接池策略，即DBUtils的连接池方案，包含'PersistentDB'和'PooledDB'两种，
            # 对应配置值为'persistent'和'pooled'，默认为'pooled'
            'pool_policy': 'persistent',
            # 其它连接池参数，参见DBUtils
            # 'maxcached': 4,
            # 'maxusage': 10,
            # ...
        }
    }

    db = Orator(app)
    # or
    db = Orator()
    db.init_app(app)

    # 查询
    users = db.table('users').all()

    # 定义Model
    class User(db.Model):
        pass

    users = User.all()


* 配置数据库慢查询日志。

.. code-block:: python

    import logging

    from flaskcap.logging import NaturalTimedRotating
    from flaskcap.orator import slow_query_logger

    # 定义慢查询日志
    log_handler = NaturalTimedRotating('slow_query.log', backupCount=7)
    slow_query_logger.addHandler(log_handler)

