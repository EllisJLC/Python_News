from datetime import datetime

# Run {python app/utils/filters.py} to run tests

def format_date(date):
  return date.strftime('%d/%m/%y') # Format date string into dd/mm/yyyy

# test format_date() function
# print(format_date(datetime.now())) # Should return current date formatted into dd/mm/yyyy

def format_url(url):
  # Split url, removes / navigation, ? queries, and unnecessary http/https/www/etc
  return url.replace('http://','').replace('https://','').replace('www.','').split('/')[0].split('?')[0]

# Test format_url()
# print(format_url('http://google.com/test/')) # Should return 'google.com'
# print(format_url('https://www.google.com?q=test')) # Should return 'google.com'

def format_plural(amount, word):
  if amount != 1:
    return word + 's'
  return word

# Test format_plural()
# print(format_plural(2, 'cat')) # Should return 'cats'
# print(format_plural(1, 'dog')) # Should return 'dog'