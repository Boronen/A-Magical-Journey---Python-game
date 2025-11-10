def safe_input_int(prompt, min_val=None, max_val=None):
    while True:
        try:
            val = int(input(prompt).strip())
            if (min_val is not None and val < min_val) or (max_val is not None and val > max_val):
                print(f"❌ Érvénytelen érték ({min_val}-{max_val})")
                continue
            return val
        except ValueError:
            print("❌ Kérlek számot adj meg!")
