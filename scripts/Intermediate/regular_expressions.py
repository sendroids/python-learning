# This script demonstrates regular expressions (regex) in Python
# Regex is used for pattern matching and text manipulation

import re

# Basic pattern matching with search()
text = "The quick brown fox jumps over the lazy dog"

# Find 'fox' in the text
match = re.search(r"fox", text)
if match:
    print(f"Found '{match.group()}' at position {match.start()}-{match.end()}")
print()


# Common regex patterns
patterns = {
    r"\d+": "One or more digits",
    r"\w+": "One or more word characters",
    r"\s+": "One or more whitespace",
    r"[aeiou]": "Any vowel",
    r"[A-Z]": "Any uppercase letter",
    r"^The": "Starts with 'The'",
    r"dog$": "Ends with 'dog'",
}

print("Pattern matching examples:")
for pattern, description in patterns.items():
    matches = re.findall(pattern, text)
    print(f"  {pattern}: {description}")
    print(f"    Matches: {matches[:5]}...")  # Show first 5
print()


# Using findall() to get all matches
email_text = "Contact us at support@example.com or sales@company.org"
emails = re.findall(r"[\w.+-]+@[\w-]+\.[a-zA-Z]+", email_text)
print(f"Found emails: {emails}")
print()


# Using match() - only matches at the beginning
text1 = "Python is great"
text2 = "I love Python"

print(f"match() on '{text1}': {re.match(r'Python', text1)}")
print(f"match() on '{text2}': {re.match(r'Python', text2)}")  # None - not at start
print()


# Groups - capturing parts of a pattern
date_text = "Event date: 2024-03-15"
pattern = r"(\d{4})-(\d{2})-(\d{2})"
match = re.search(pattern, date_text)

if match:
    print(f"Full match: {match.group(0)}")
    print(f"Year: {match.group(1)}")
    print(f"Month: {match.group(2)}")
    print(f"Day: {match.group(3)}")
    print(f"All groups: {match.groups()}")
print()


# Named groups
pattern = r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})"
match = re.search(pattern, date_text)

if match:
    print(f"Year (named): {match.group('year')}")
    print(f"Dict: {match.groupdict()}")
print()


# Substitution with sub()
text = "Hello World! Hello Python!"
new_text = re.sub(r"Hello", "Hi", text)
print(f"Original: {text}")
print(f"After sub: {new_text}")

# Substitute with a function
def upper_match(match):
    return match.group(0).upper()

text = "The cat sat on the mat"
result = re.sub(r"\b\w{3}\b", upper_match, text)
print(f"3-letter words uppercased: {result}")
print()


# Splitting with split()
text = "apple,banana;cherry:date"
parts = re.split(r"[,;:]", text)
print(f"Split result: {parts}")
print()


# Compiled patterns (more efficient for repeated use)
phone_pattern = re.compile(r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}")

contacts = [
    "Call me at (123) 456-7890",
    "Phone: 987.654.3210",
    "Number is 555 123 4567",
]

print("Finding phone numbers:")
for contact in contacts:
    match = phone_pattern.search(contact)
    if match:
        print(f"  Found: {match.group()}")
print()


# Flags for pattern matching
text = "Python\npython\nPYTHON"

# Case insensitive
matches = re.findall(r"python", text, re.IGNORECASE)
print(f"Case insensitive matches: {matches}")

# Multiline mode
matches = re.findall(r"^python", text, re.MULTILINE | re.IGNORECASE)
print(f"Multiline matches: {matches}")
print()


# Lookahead and lookbehind
text = "Price: $100, Cost: $50, Value: $200"

# Positive lookahead: find numbers followed by '0'
matches = re.findall(r"\d+(?=0)", text)
print(f"Numbers followed by 0: {matches}")

# Positive lookbehind: find numbers after '$'
matches = re.findall(r"(?<=\$)\d+", text)
print(f"Numbers after $: {matches}")


# Validating input patterns
def validate_email(email):
    pattern = r"^[\w.-]+@[\w.-]+\.\w+$"
    return bool(re.match(pattern, email))


test_emails = ["user@example.com", "invalid.email", "test@domain.org"]
print("\nEmail validation:")
for email in test_emails:
    status = "Valid" if validate_email(email) else "Invalid"
    print(f"  {email}: {status}")

