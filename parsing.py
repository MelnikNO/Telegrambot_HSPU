import requests
from bs4 import BeautifulSoup
import csv

domain = 'https://atlas.herzen.spb.ru'
source_url = 'https://atlas.herzen.spb.ru/prof.php'

def person_details(url):
  response = requests.get(url)
  soup = BeautifulSoup(response.text, 'html.parser')

  details = {
        'degree': 'не указано',
        'phone': 'не указано',
        'email': 'не указано',
        'department': 'не указано'
  }

  for h3 in soup.find_all('h3', class_='mm'):
    header = h3.get_text(strip=True)
    next_sibling = h3.find_next_sibling()

    if not next_sibling:
      continue

    value = next_sibling.get_text(' ', strip=True)

    if 'Ученая степень и звание' in header:
      degree_span = h3.find_next('span', class_='text')
      if degree_span:
        details['degree'] = degree_span.get_text(' ', strip=True)
        details['degree'] = details['degree'].split('\n')[0].split('<')[0].strip()
      else:
        details['degree'] = 'ученой степени не имеет, ученого звания не имеет'

      if any(x in details['degree'].lower() for x in ['e-mail', 'телефон', 'расписание', 'дисциплины']):
        details['degree'] = 'ученой степени не имеет, ученого звания не имеет'
    elif 'E-mail' in header:
      details['email'] = value
    elif 'Контактный телефон' in header:
      details['phone'] = value
    elif 'Кафедра:' in header:
      department_span = h3.find_next('span', class_='text')
      if department_span:
        details['department'] = department_span.get_text(' ', strip=True)

  return details


def get_persons(url):
  response = requests.get(url)

  my_soup = BeautifulSoup(response.text, 'html.parser')

  cells = my_soup.find_all('td', class_='t1')

  results = []

  for cell in cells:
    link = cell.find('a')
    if cell.a:
      name = cell.a.text.strip()
      clean_name = name.replace('"', '').strip()
      if any(word in clean_name.lower() for word in ['управление', 'отдел', 'центр', 'деканат']):
        continue
      person_url = domain + '/' + cell.a['href'].lstrip('/')
      details = person_details(person_url)
      person_data = {
          'name': clean_name,
          'url': person_url,
          **details
      }

      results.append(person_data)
      print(f"Обработан: {clean_name}")

  return results


def save_to_csv(data, filename):
  with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['name', 'degree', 'phone', 'email', 'department', 'url']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)


def main():
  professors = []
  all_pages = 22
  for page in range(1, all_pages + 1):
    url = f"{source_url}?FND=0&FIO=&PAGE=" + str(page)
    print(f"\nПарсинг страницы {page}/{all_pages}")
    professors.extend(get_persons(url))
    print(f"На странице: {len(get_persons(url))}")

  save_to_csv(professors, 'professors_info.csv')
  # save_to_csv(professors, 'info.csv') # для теста
  print(f"\nВсего {len(professors)} преподавателей.")
  print("Результат сохранен в professors_info.csv")
  # print("Результат сохранен в info.csv") # для теста

if __name__ == '__main__':
  main()

