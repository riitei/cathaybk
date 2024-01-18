def adjust_grade(original_grade):
    if original_grade < 40:
        return original_grade
    next_multiple_of_5 = 5 * ((original_grade // 5) + 1)
    if next_multiple_of_5 - original_grade < 3:
        return next_multiple_of_5
    return original_grade

def test_grade_adjustment(student, original_grade, expected_grade):
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