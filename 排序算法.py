def merge(A, B):
    '''
    合并两个已排序数组
    思路:
        分别定义i,j两个整形变量,作为指针, 指向当前A, B数组位置
        循环比较A[i], B[j]位置上的值,小的则提取值放在结果数据, 同时对应的指针+1
        另一个的指针不变.

    Args:
        list A:一个已排序数组
        list B:一个已排序数组

    Returns:
        result:一个已经排序的数组
    '''

    #将要返回的结果数组
    result = []
    #分别为A,B两个数组的遍历指针, 初始指向为0索引位置
    i, j = 0, 0
    while i<len(A) and j<len(B):
        if A[i]<B[j]:
            result.append(A[i])
            i += 1
        else:
            result.append(B[j])
            j += 1
    result += A[i:]
    result += B[j:]
    return result
