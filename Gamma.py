import re

def load_wordlist(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        wordlist = set(line.strip() for line in f)
    return wordlist

def is_compromised(password, wordlist):
    return password in wordlist

def check_length(password):
    return len(password) >= 12

def check_character_variety(password):
    has_upper = re.search(r'[A-Z]', password) is not None
    has_lower = re.search(r'[a-z]', password) is not None
    has_digit = re.search(r'\d', password) is not None
    has_special = re.search(r'[!@#$%^&*(),.?":{}|<>]', password) is not None
    return has_upper, has_lower, has_digit, has_special

def check_common_patterns(password):
    common_patterns = ["1234", "password", "qwerty", "letmein"]
    for pattern in common_patterns:
        if pattern in password.lower():
            return False
    return True

def calculate_strength_score(password, wordlist):
    score = 0

    length = len(password)
    if length >= 12:
        score += 3
    elif length >= 8:
        score += 2
    elif length >= 6:
        score += 1

    if length > 15:
        score += 1

    print(f"Length: {length} -> Score: {score}")

    has_upper, has_lower, has_digit, has_special = check_character_variety(password)
    variety_score = sum([has_upper, has_lower, has_digit, has_special])
    score += variety_score

    if variety_score == 4 and length >= 12:
        score += 1

    print(f"Character Variety - Upper: {has_upper}, Lower: {has_lower}, Digit: {has_digit}, Special: {has_special} -> Score: {variety_score}")

    if not check_common_patterns(password):
        score -= 2
        print(f"Common pattern detected -> Score Deduction: -2")

    if is_compromised(password, wordlist):
        score = 0
        print(f"Password found in leak -> Score: 0")

    score = max(1, min(score, 10))
    print(f"Final Score: {score}")
    return score

def check_password_strength(password, wordlist):
    score = calculate_strength_score(password, wordlist)
    if score == 10:
        return f"Password is extremely strong. (Strength: {score}/10)"
    elif score >= 7:
        return f"Password is strong. (Strength: {score}/10)"
    elif score >= 4:
        return f"Password is moderate. (Strength: {score}/10)"
    else:
        return f"Password is weak. (Strength: {score}/10)"

def validate_password(password, wordlist):
    leak_status = "Password found in the leak. Choose a different password." if is_compromised(password, wordlist) else "Password is not found in the leak."
    strength_status = check_password_strength(password, wordlist)
    return f"{leak_status}\n{strength_status}"

def main():
    wordlist = load_wordlist('rockyou.txt')

    while True:
        print("\nMenu:")
        print("1 - Check if password has been found in data leak")
        print("2 - Check password strength")
        print("3 - Check both password strength and if password has been found in data leak")
        print("0 - End script")
        
        choice = input("Enter your choice: ")
        
        if choice == '0':
            print("Ending script. Goodbye!")
            break
        elif choice in ['1', '2', '3']:
            password_to_check = input("Enter a password to check: ")
            
            if choice == '1':
                if is_compromised(password_to_check, wordlist):
                    print("Password found in the leak. Choose a different password.")
                else:
                    print("Password is not found in the leak.")
            
            elif choice == '2':
                strength_result = check_password_strength(password_to_check, wordlist)
                print(strength_result)
            
            elif choice == '3':
                result = validate_password(password_to_check, wordlist)
                print(result)
        
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
