def luhn_check(card_number):
    # Remove spaces
    card_number = card_number.replace(" ", "")
    
    total = 0
    reverse_digits = card_number[::-1]

    for i, digit in enumerate(reverse_digits):
        n = int(digit)
        
        if i % 2 == 1:   # double every second digit
            n *= 2
            if n > 9:
                n -= 9
        
        total += n

    return total % 10 == 0


# Test
number = input("Enter card number: ")

if luhn_check(number):
    print("Valid Card Number ✅")
else:
    print("Invalid Card Number ❌")