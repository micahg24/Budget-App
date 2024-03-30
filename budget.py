class Category:
  def __init__(self, category):
    #ledger list and name of category
    self.name = category
    self.ledger = []

  def __str__(self):
    display = []
    #Sets up title
    display.append(self.name.center(30, "*"))
    for item in self.ledger:
      description = item["description"][:23].ljust(23)
      amount = item["amount"]
      display.append(description + f"{amount:.2f}".rjust(7))
    display.append(f"Total: {self.get_balance():.2f}")
    return "\n".join(display)

  #Deposit function
  def deposit(self,amount, description = " "):
    deposit = {"amount": amount, "description": description}
    self.ledger.append(deposit)

    return deposit

  #Withdrawal function
  def withdraw(self, amount, description = " "):
    if self.check_funds(amount):
      withdraw = {"amount": amount * - 1, "description": description}
      self.ledger.append(withdraw)
      return True

    else:
      return False

  #Gets the total amount of the balance
  def get_balance(self):
    balance = 0
    for item in self.ledger:
      balance = balance + item["amount"]

    return balance

  #Transfers amount to different categories
  def transfer(self, amount, destination_category):
    if self.check_funds(amount):
      self.withdraw(amount, f"Transfer to  + {destination_category.name}")
      destination_category.deposit(amount, f"Transfer from  {self.name}")
      return True

    else:
      return False

  #Checks the amount of funds available
  def check_funds(self, amount):
    funds = 0
    
    for item in self.ledger:
      funds = funds + item["amount"]

      if amount > funds:
        return False

      else:
        return True
      
    

def create_spend_chart(categories):
    total_spent = 0
    categories_spent = []

    #Percentage is calculated by using withdrawal and desposit functions
    for category in categories:
      spent = 0

      #Calcualtes amount spent in each category and the total amount spent
      for item in category.ledger:
        if item["amount"] < 0 and "Transer" not in item["description"]:
          spent = spent + item["amount"]
          total_spent = total_spent + spent

      categories_spent.append({"name": category.name, "spent": spent})

      #Calculates the percentage of the amount spent in each category
    for category in categories_spent:
      percent = (category["spent"] * 100) / total_spent
      category["percent"] = int(percent - (percent % 100))

    #Title of percetnage spent in the category
    display_rows = []
    display_rows.append("Percentage spent by category")

    #Formats percentage from 100-0
    #Bars in chart are marked with o
    for percent in range(100, -1, -10):
      row = str(percent).rjust(3) +"|"
      for category in categories_spent:
        if category["percent"] >= percent:
          row += "o".center(3)

        else:
          row += " " * 3

      row += " "
      display_rows.append(row)

    #Horizontal line 
    display_rows.append((" ".rjust(4)) + "---" * len(categories_spent) + "-")

    #Category name should be below the horizontal line
    length_tags = max([len(category["name"]) for category in categories_spent])

    for i in range(length_tags):
      row = " " * 4
      for category in categories_spent:
        if i < len(category["name"]):
          row += category ["name"][i].center(3)

        else:
          row += " " * 3

      row += " "

      display_rows.append(row)

    #join rows and connect it to the string
    display = "\n".join(display_rows)
    return display
