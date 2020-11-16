s = "Just text for testing. Cool!"
print(len(s))
print("{}".format(s[10]))
print(s[len(s)-5])
print(s[5:9])
print(s[:4])
print(s[::2])
print(s[1::2])
print(ord(s[3]))
print(s[::-1]) # Reverse string
print(s.upper())
print(s.lower())
print(s.count('text', 3, 10))
print(s.find('for'))
print(s.rfind('for'))
print(s.index('o'))
print(s.replace(' ','-',2)) 
print(s.isalpha())
print(s.isdigit())
print(s.ljust(30, "_")) # Add aditional symbol to string
print(s.rjust(30, "_")) # Add aditional symbol to string
t_str = s.split(' ') # Split string by words
print("_".join(t_str))
print(s.strip()) # removing both the leading and the trailing characters