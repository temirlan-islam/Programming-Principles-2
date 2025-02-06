def grams_to_ounces(grams):
    ounces = grams / 28.3495231
    return ounces

grams = float(input("Enter grams: "))
print(f"{grams} grams is equal to {grams_to_ounces(grams):.2f} ounces.")
