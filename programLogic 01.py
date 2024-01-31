def adjust_grade(original_grade):
    """
    調整學生的成績。
    如果原始成績小於40，則不進行調整。
    如果原始成績到下一個5的倍數的差距小於3，則將成績調整為那個倍數。
    :param original_grade: 原始成績。
    :return: 調整後的成績。
    """
    if original_grade < 40:
        return original_grade
    next_multiple_of_5 = 5 * ((original_grade // 5) + 1)
    if next_multiple_of_5 - original_grade < 3:
        return next_multiple_of_5
    return original_grade

def test_grade_adjustment(student, original_grade, expected_grade):
    """
    測試成績調整函數。
    使用assert語句確保調整後的成績符合預期。
    :param student: 學生的名字。
    :param original_grade: 原始成績。
    :param expected_grade: 預期的調整後成績。
    :return: 測試結果信息。
    """
    calculated_grade = adjust_grade(original_grade)
    assert calculated_grade == expected_grade, f"Test failed for {student}. Expected: {expected_grade}, Got: {calculated_grade}"
    return f"Test passed for {student}"

test_data = {
    "德瑞克": (33, 33),
    "尚恩": (73, 75),
    "傑夫": (63, 65),
    "馬基": (39, 39)
}

# Run tests and print results
for student, data in test_data.items():
    result = test_grade_adjustment(student, data[0], data[1])
    print(result)