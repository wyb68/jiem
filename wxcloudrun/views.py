from datetime import datetime
from flask import render_template, request
from run import app
from wxcloudrun.dao import delete_counterbyid, query_counterbyid, insert_counter, update_counterbyid
from wxcloudrun.model import Counters
from wxcloudrun.response import make_succ_empty_response, make_succ_response, make_err_response
import os
import re


@app.route('/')
def index():
    """
    :return: 返回index页面
    """
    return render_template('index.html')


@app.route('/api/model1', methods=['POST'])
def model1():
    params = request.get_json()
    name = params.get("name")
    time = params.get("time")
    work = re.sub(r'[ \n]', '', params.get("work"))  # 正则去除空格和回车

    # 设定文件夹和文件的路径
    folder_path = './userData/'
    file_path = os.path.join(folder_path, name + '.txt')
    print(file_path)
    # 检查userData文件夹是否存在，如果不存在则创建它
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

        # 检查文件是否存在，如果不存在则创建它（这里其实不需要显式创建文件，因为使用'a'模式打开文件时如果文件不存在会自动创建）
    if not os.path.exists(file_path):
        # 这里其实不需要执行具体的创建文件操作，因为下面使用'a'模式打开文件时会自动创建
        print(f"文件'{file_path}'不存在，将在写入时自动创建。")

        # 使用追加模式('a')打开文件，写入内容
    with open(file_path, 'a', encoding='utf-8') as file:
        file.write(time + '@@' + work + '\n')

    return {
        'success': True,
        'message': '提交成功！'
    }


@app.route('/api/model2', methods=['POST'])
def model2():
    params = request.get_json()
    name = params.get("name")
    data = []
    path = './userData/'
    for filename in os.listdir(path):
        if name == os.path.splitext(filename)[0] or name == '':
            if os.path.isfile(os.path.join(path, filename)):
                with open(path + filename, encoding='utf-8') as file:
                    data0 = []
                    for line in file:
                        if line.strip():
                            line_data = line.strip().replace('\n', '').split('@@')
                            data0.append({
                                "time": line_data[0],
                                "content": line_data[1]
                            })
            data.append({
                'user_name': os.path.splitext(filename)[0],
                'user_data': data0
            })
    if len(data):
        response_data = {
            'success': True,
            'message': '提交成功！',
            'data': data
        }
    else:
        response_data = {
            'success': False,
            'message': '未查到用户数据！',
            'data': []
        }
    return response_data


@app.route('/api/model3', methods=['POST'])
def model3():
    params = request.get_json()
    name = params.get("name")
    path = './userData/'
    # 定义文件路径
    file_path = os.path.join(path, name + '.txt')

    # 检查文件是否存在
    if os.path.exists(file_path):
        # 删除文件
        os.remove(file_path)
        response_data = {
            'success': True,
            'message': '删除成功！'
        }
    else:
        response_data = {
            'success': False,
            'message': '用户不存在！'
        }

    return response_data


# 以下模板默认
@app.route('/api/count', methods=['POST'])
def count():
    """
    :return:计数结果/清除结果
    """

    # 获取请求体参数
    params = request.get_json()

    # 检查action参数
    if 'action' not in params:
        return make_err_response('缺少action参数')

    # 按照不同的action的值，进行不同的操作
    action = params['action']

    # 执行自增操作
    if action == 'inc':
        counter = query_counterbyid(1)
        if counter is None:
            counter = Counters()
            counter.id = 1
            counter.count = 1
            counter.created_at = datetime.now()
            counter.updated_at = datetime.now()
            insert_counter(counter)
        else:
            counter.id = 1
            counter.count += 1
            counter.updated_at = datetime.now()
            update_counterbyid(counter)
        return make_succ_response(counter.count)

    # 执行清0操作
    elif action == 'clear':
        delete_counterbyid(1)
        return make_succ_empty_response()

    # action参数错误
    else:
        return make_err_response('action参数错误')


@app.route('/api/count', methods=['GET'])
def get_count():
    """
    :return: 计数的值
    """
    counter = Counters.query.filter(Counters.id == 1).first()
    return make_succ_response(0) if counter is None else make_succ_response(counter.count)
