from flask import Flask, current_app, g, request, session, render_template, make_response, abort, redirect, url_for

app = Flask(__name__)
# 配置 Debug 模式
app.config['DEBUG'] = True
# 为模板引擎添加扩展，支持break/continue语法
app.jinja_env.add_extension('jinja2.ext.loopcontrols')


@app.route('/index')
def index():
    return 'Hello World!'


@app.route('/test01')
def test01():
    print(current_app.name)
    print(request.data)
    print(g)
    print(session)
    """ 引用相同 内存地址不同 """
    print(app == current_app)
    print(app is current_app)
    return 'test01'


@app.route('/test02/<page>')
def test02(page):
    return page


@app.route('/test03/<int:page>')
def test03(page):
    args = request.args
    # print(args.get('page'))
    # 打印请求头
    print(request.headers['User-Agent'])
    return str(page)


@app.before_request
def before_request():
    print('before_request')


@app.context_processor
def context_processor():
    print('context_processor')
    return {'name': 'context_processor'}


@app.after_request
def after_request(response):
    print('after_request')
    return response


@app.route('/test04/html')
def test04():
    html = render_template('index.html', flag='test04')
    return make_response(html, 500, {'Content-Type': 'text/html'})


@app.route('/test05')
def test05():
    abort(401)
    return redirect(url_for('test01'), code=302)


@app.errorhandler(401)
def error_401(error):
    return 'error_401'


@app.route('/test06')
def test06():
    user_info = {'username': 'test06', 'nickname': 'test123', 'address.city': 'beijing', 'address.area': 'shanghai'}
    list_user = [{'username': '张三', 'address': {'city': '广州'}}, {'username': '李四', 'address': {'city': '深圳'}}]
    return render_template('index2.html',
                           age=18,
                           money=10000,
                           name='test06',
                           user_info=user_info,
                           tuple_city=('beijing', 'shanghai', 'guangzhou'),
                           list_city=['beijing', 'shanghai', 'guangzhou'],
                           list_user=list_user
                           )


@app.route('/tag')
def tag():
    """  模板标签的使用 """
    var = None
    a = 2
    list_user = [
        {'username': '张三', 'age': 32, 'address': '北京'},
        {'username': '李四', 'age': 22},
        {'username': '王五', 'age': 32, 'address': '北京'},
        {'username': '王文', 'age': 22}
    ]
    # list_user = []
    return render_template('tag.html',
                           var=var,
                           a=a,
                           list_user=list_user,
                           phone_number="12345678901")


@app.template_filter('phone_format')
def phone_format(phone_number):
    # 过滤手机号
    return phone_number[:3] + '****' + phone_number[7:]


@app.route('/filter')
def use_filter():
    """ 过滤器的使用 """
    welcome = 'hello, lucy'
    var = 'hello'
    name = None
    html_value = '<h2>标题加粗</h2>'
    phone_number = '13312345678'
    return render_template('use_filter.html',
                           welcome=welcome,
                           var=var,
                           name=name,
                           html_value=html_value,
                           phone_number=phone_number)


@app.route('/gb')
def gb():
    """  全局变量的使用 """
    return render_template('global_func.html')


@app.route('/macro')
def macro():
    """ 模板中宏的使用 """
    return render_template('macro.html')


@app.route('/extend')
def extend():
    """ 模板继承 """
    return render_template('extends_demo.html')


if __name__ == '__main__':
    app.run()
