def bounce_simulation(initial_height, bounces):
    """
    模擬球的彈跳運動。
    計算球從給定的初始高度彈跳特定次數後的總行程和最終彈跳高度。
    :param initial_height: 球的初始高度。
    :param bounces: 彈跳的次數。
    :return: (總行程, 最終彈跳高度)。
    """
    total_distance = initial_height  # 初始總行程等於初始高度
    for _ in range(bounces - 1):  # 對於每一次彈跳
        initial_height /= 2  # 每次反彈後的高度是前一次的一半
        total_distance += 2 * initial_height  # 加上上升和下降的距離
    final_bounce_height = initial_height / 2  # 最終彈跳高度
    return total_distance, final_bounce_height


def test_bounce_simulation():
    """
    測試球彈跳模擬函數。
    確保計算出的總行程和最終彈跳高度與預期值相符。
    :return: (總行程, 最終彈跳高度)。
    """
    initial_height = 100  # 初始高度
    bounces = 10  # 彈跳次數
    expected_total_distance = 299.609375  # 預期的總行程
    expected_final_bounce_height = 0.09765625  # 預期的最終彈跳高度
    total_distance, final_bounce_height = bounce_simulation(initial_height, bounces)  # 執行模擬
    # 斷言檢查：比較計算出的總行程和預期總行程是否足夠接近
    # 1e-6（即0.000001）是設定的一個小誤差閾值，用來判斷計算結果是否“足夠接近”預期結果。
    assert abs(total_distance - expected_total_distance) < 1e-6, (
        f"Test failed for total distance. Expected: {expected_total_distance}, Got: {total_distance}")
    # 如果計算的總行程和預期的總行程相差超過1e-6，則會觸發錯誤
    # 斷言檢查：比較計算出的最終彈跳高度和預期最終彈跳高度是否足夠接近
    assert abs(final_bounce_height - expected_final_bounce_height) < 1e-6, (
        f"Test failed for final bounce height. Expected: {expected_final_bounce_height}, Got: {final_bounce_height}")
    # 如果計算的最終彈跳高度和預期的最終彈跳高度相差超過1e-6，則會觸發錯誤
    # 如果上面的所有斷言都沒有觸發錯誤，則打印"測試通過"的信息
    print("Test passed for bounce simulation.")  # 測試通過
    # 返回計算出的總行程和最終彈跳高度
    return total_distance, final_bounce_height


test_bounce_simulation()
