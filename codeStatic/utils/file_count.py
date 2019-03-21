from tempfile import SpooledTemporaryFile


def count_row(file_obj):
    """
    统计单文件代码行数
    排除:
        # 单行注释
        双引号多行注释
        空行
    :param file_obj: 文件路径 或者 SpooledTemporaryFile对象
    :return: num 代码行数
    """

    content = None
    if isinstance(file_obj, str):
        with open(file_obj, 'rb') as f:
            return _count_row(f.readlines())
    elif isinstance(file_obj, SpooledTemporaryFile):
        return _count_row(file_obj)
    else:
        raise Exception("不支持该类型参数文件")


def _count_row(obj):
    """

    :param obj:
    :return:
    """
    total = 0
    flag = True
    for line in obj:
        line_strip = line.strip()
        if line.startswith(b'"""'):
            if line.endswith(b'"""'):
                continue
            flag = not flag  # 开关原则
            continue
        if flag:
            if line.startswith(b"#"):
                continue
            if len(line_strip) == 0:
                continue
            total += 1
    return total