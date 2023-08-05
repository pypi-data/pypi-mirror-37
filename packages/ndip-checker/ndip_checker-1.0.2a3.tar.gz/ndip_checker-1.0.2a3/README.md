## 说明

本脚本可以检查 病程记录/培养/涂片 三种检查项的数据是否有问题。

项目基于python2.7，因MySQLDB尚未支持python3。

## 安装与使用

1. 创建虚拟环境： `virtualenv venv -p python2.7`
2. 激活虚拟环境： `source venv/bin/activate`   # Linux 环境
3. 安装依赖： `pip install -r requirements.txt`
4. 修改数据库地址、用户名、密码： 打开`main.py`
5. 使用： `python main.py`
