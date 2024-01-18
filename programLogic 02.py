def bounce_simulation(initial_height, bounces):
    total_distance = initial_height
    for _ in range(bounces - 1):
        initial_height /= 2
        total_distance += 2 * initial_height
    final_bounce_height = initial_height / 2
    return total_distance, final_bounce_height


def test_bounce_simulation():
    initial_height = 100
    bounces = 10
    expected_total_distance = 299.609375
    expected_final_bounce_height = 0.09765625
    total_distance, final_bounce_height = bounce_simulation(initial_height, bounces)
    assert abs(total_distance - expected_total_distance) < 1e-6, (
        f"Test failed for total distance. Expected: {expected_total_distance}, Got: {total_distance}")
    assert abs(final_bounce_height - expected_final_bounce_height) < 1e-6, (
        f"Test failed for final bounce height. Expected: {expected_final_bounce_height}, Got: {final_bounce_height}")
    print("Test passed for bounce simulation.")
    return total_distance, final_bounce_height


test_bounce_simulation()
