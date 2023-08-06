# 对基本类型dict, list, set, tuple进行遍历

### 对遍历的数据进行操作

### 测试代码
```
from zforeach import foreach_object
from zforeach import foreach_data


def foreach_fun(item: foreach_object):
    print('foreach:', item)
    if item.key == 'level2':
        item.key = 'change_level2'


data = [
    'level1',
    {
        'level2':
            [
                'level3'
            ],
    }
]

value = foreach_data(data, foreach_fun, deep=True)
print('结果', value)
```

> foreach: <level:1> level1
> foreach: <level:3> level3
> foreach: <level:2> level2: ['level3']
> foreach: <level:1> {'change_level2': ['level3']}
> result: ['level1', {'change_level2': ['level3']}]


更新日志:
>     1.0.0
>     首发

- - -
本项目仅供所有人学习交流使用,禁止用于商业用途
