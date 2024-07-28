def pour(jug1, jug2):
    max1, max2, fill = 5, 7, 4
    print(f"Jug1: {jug1}, Jug2: {jug2}")
    
    if jug1 == fill or jug2 == fill:
        return True

    if (jug1, jug2) in visited:
        return False

    visited.add((jug1, jug2))

    # Fill Jug1
    if pour(max1, jug2):
        return True
    # Fill Jug2
    if pour(jug1, max2):
        return True
    # Empty Jug1
    if pour(0, jug2):
        return True
    # Empty Jug2
    if pour(jug1, 0):
        return True
    # Pour Jug1 to Jug2
    if jug1 + jug2 <= max2:
        if pour(0, jug1 + jug2):
            return True
    else:
        if pour(jug1 - (max2 - jug2), max2):
            return True
    # Pour Jug2 to Jug1
    if jug1 + jug2 <= max1:
        if pour(jug1 + jug2, 0):
            return True
    else:
        if pour(max1, jug2 - (max1 - jug1)):
            return True

    return False

def main():
    global visited
    visited = set()
    print("Steps:")
    if not pour(0, 0):
        print("No solution found")

if __name__ == "__main__":
    main()
