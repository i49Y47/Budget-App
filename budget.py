class Category:

  def __init__(self, category_name):
    self.category_name = category_name
    self.ledger = list()

  def deposit(self, amount: float, description=""):
    self.ledger.append({"amount": amount, "description": description})

  def withdraw(self, amount: float, description=""):
    if self.check_funds(amount):
      self.ledger.append({"amount": -amount, "description": description})
      return True
    return False

  def get_balance(self):
    return sum([transaction["amount"] for transaction in self.ledger])

  def transfer(self, amount: float, cls):
    if self.check_funds(amount):
      self.ledger.append({
        "amount": -amount,
        "description": f"Transfer to {cls.category_name}"
      })
      cls.deposit(amount, description=f"Transfer from {self.category_name}")
      return True
    return False

  def check_funds(self, amount: float):
    if self.get_balance() >= amount:
      return True
    return False

  def __str__(self):
    l = len(self.category_name)
    res = self.category_name.rjust(15 + l // 2, '*').ljust(30, '*') + '\n'
    total = 0
    for transation in self.ledger:
      am = transation.get('amount')
      total += am
      res += transation.get('description')[:23].ljust(23)
      res += f"{am:.2f}".rjust(7) + '\n'
    res += f"Total: {total:.2f}"

    return res


def create_spend_chart(categories):
  spent_amounts = [
    round(
      abs(sum([item['amount'] for item in cat.ledger
               if item['amount'] < 0])), 2) for cat in categories
  ]

  # Calculate percentage rounded down to the nearest 10
  total = round(sum(spent_amounts), 2)
  spent_percentage = list(
    map(lambda amount: int((((amount / total) * 10) // 1) * 10),
        spent_amounts))

  # Create the bar chart substrings
  header = "Percentage spent by category\n"

  chart = ""
  for value in range(100, -10, -10):
    chart += str(value).rjust(3) + '|'
    for percent in spent_percentage:
      chart += f" {'o' if percent >= value else ' '} "
    chart += " \n"

  footer = "    " + "-" * ((3 * len(categories)) + 1) + "\n"
  descriptions = list(map(lambda category: category.category_name, categories))
  max_length = max(map(lambda description: len(description), descriptions))
  descriptions = list(
    map(lambda description: description.ljust(max_length), descriptions))
  for x in zip(*descriptions):
    footer += "    " + "".join(map(lambda s: s.center(3), x)) + " \n"

  return (header + chart + footer).rstrip("\n")
