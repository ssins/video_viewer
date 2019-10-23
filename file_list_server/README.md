# camera_server
一个简单的后端架构demo，对模型稍作调整即可作为一个通用的后端架构
## 架构 /App/
 - 主要代码在App目录下，以各个模块划分目录，每个模块都是一个flask蓝图
 - cryptor.py：加解密工具，用于计算用户Token
 - decorators.py：装饰器，主要用于验证用户权限
 - models.py：数据表模型，提供了模型序列化的能力
## 数据表模型 /App/models.py
 - camera：摄像头信息
 - user：简单的用户信息，默认存在root用户
 - permission：用户操作摄像头的权限
## 一些工具 /Utils/
 - create_flask_model.py：flask模块代码生成工具
## 项目配置 /config.py
 - 提供项目的配置内容
 - ROOT_NAME：默认ROOT用户，初始账号密码均为ROOT_NAME
## 入口 /server.py
 - /init 用于初始化数据库
