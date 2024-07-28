def moveTower(height, fromPole, toPole, withPole):
    if height >= 1:
        moveTower(height - 1, fromPole, withPole, toPole)  # Move tower of size height-1 to auxiliary pole
        moveDisk(fromPole, toPole)                         # Move the largest disk to the target pole
        moveTower(height - 1, withPole, toPole, fromPole)  # Move the tower from auxiliary to target pole

def moveDisk(fp, tp):
    print("Moving disk from", fp, "to", tp)

# Example usage
moveTower(3, "A", "B", "C")
