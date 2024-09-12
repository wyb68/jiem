# 创建应用实例
import sys

from wxcloudrun import app

# 启动Flask Web服务
if __name__ == '__main__':
    app.run(host=sys.argv[1], port=sys.argv[2])  # 上线
    # app.run(host='0.0.0.0', port=5000, debug=True)  # 本地测试-启动程序
