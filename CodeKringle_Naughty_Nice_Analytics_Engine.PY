"""AP Computer Science Christmas Project - Naughty/Nice Analytics System"""

import random
import os

class Child:
    """Child class to store all child data."""
    def __init__(self, name, gender):
        self.name = name
        self.gender = gender
        self.responses = []
        self.score = 0
        self.category = ""
        self.gift = ""

# behaviour questions: (question, points_frequently, points_sometimes, points_never)
behaviour_questions = [
    ("How often did this child help others this year?", 15, -5, -15),
    ("How often did they lie to parents or teachers?", -20, -5, 5),
    ("Did they share toys with siblings or friends?", 12, -3, -8),
    ("Did they complete homework assignments on time?", 8, -2, -10),
    ("Did they say mean things to others?", -15, -5, 8),
    ("Did they volunteer or help in the community?", 18, -2, -8),
    ("Did they break things on purpose?", -18, -3, 10),
    ("Did they apologize when they made mistakes?", 10, -2, -6),
    ("Did they stand up for others being bullied?", 16, -4, -10),
    ("Did they waste food or resources?", -10, -3, 8),
]

# Target percentage ranges for statistics requirements
target_percentages = {
    "nice": (50, 80),
    "angelic": (0, 20),
    "naughty": (10, 40),
    "evil": (0, 10)
}

# Gift inventory: (name, quantity, gender, how much each kid wants the toy/gift )
GIFT_INVENTORY = [
    ("Remote Control Car", 3, "M", 50),
    ("Doll Set", 3, "F", 50),
    ("LEGO Set", 4, "ALL", 30),
    ("Art Kit", 3, "ALL", 20),
    ("Bike", 2, "ALL", 40),
    ("Video Game Console", 2, "ALL", 60),
    ("Soccer Ball", 4, "ALL", 15),
    ("Rubicks Cube", 3, "ALL", 25),
    ("Coal", 5, "ALL", 100),
    ("Socks", 5, "ALL", 80),
    ("Chores List", 5, "ALL", 60),
    ("Krampus Visit", float("inf"), "ALL", 100),
]

# ASCII art for gifts -> acquired through https://ascii.co.uk/art/
GIFT_ART = {
    "Remote Control Car": """
      ____                    
 ____//_]|________       
(o _ |  -|   _  o|       
 `(_)-------(_)--'
    """,
    "Doll Set": """
IDK
    """,
    "LEGO Set": """
    _ 
   [_] 
 /;   :\ 
()'---'()
  | | |
  [=|=]
    """,
    "Art Kit": """
                   ,'|
                  (  ;   ,\ 
            _..-'';,'._,','
         ,-' ,-. //,-,:\ '.
       ,' _  `-'// >',',-.\ 
     ,'  (_)   //,','  `-' :
    /,-.      //','     _  |
   : `-'    _//,'      (_) |
   :       (//')     _     ;
    `._.,-. `-'  _  (_)   /
      ,','/;.   (_)     ,'
     `-' //  \       _.'
        //    `-..-'' 
       `'
    """,
    "Bike": """
                __
     ,--.      <__)
     `- |________7
        |`.      |\ 
     .--|. \     |.\--.
    /   j \ `.7__j__\  \ 
   |   o   | (o)____O)  |
    \     /   J  \     /
     `---'        `---'      

    """,
    "Video Game Console": """
 _n_________________
|_|_______________|_|
|  ,-------------.  |
| |  .---------.  | |
| |  |         |  | |
| |  |         |  | |
| |  |         |  | |
| |  |         |  | |
| |  `---------'  | |
| `---------------' |
|   _ GAME BOY      |
| _| |_         ,-. |
||_ O _|   ,-. "._,"|
|  |_|    "._,"   A | 
|    _  _    B      | 
|   // //           |
|  // //    ||||||  |
|  `  `      ||||| ,
|________...______,"
    """,
    "Soccer Ball": """
           _...----.._
        ,:':::::.     `>.
      ,' |:::::;'     |:::.
     /    `'::'       :::::\ 
    /         _____     `::;\ 
   :         /:::::\      `  :
   | ,.     /::SSt::\        |
   |;:::.   `::::::;'        |
   ::::::     `::;'      ,.  ;
    \:::'              ,::::/
     \                 \:::/
      `.     ,:.        :;'
        `-.::::::..  _.''
           ```----'''

    """,
    "Rubicks Cube": """
     ___ ___ ___
   /___/___/___/|
  /___/___/___/||
 /___/___/__ /|/|
|   |   |   | /||
|___|___|___|/|/|
|   |   |   | /||
|___|___|___|/|/
|   |   |   | /
|___|___|___|/
    """,
    "Coal": """
     _____
  __/#####\__
 /####@@@@####\ 
|####@@@@@@####|
 \#####@@@@####/
  \############/
   \__________/

    """,
    "Socks": """
     _____
    |     |     
    |     |____
    |          |
    |__________|
    """,
    "Chores List": """
╔══════════════════════╗
║      CHORES LIST     ║
╠══════════════════════╣
║ ☐ Make bed           ║
║ ☐ Wash dishes        ║
║ ☐ Take out trash     ║
║ ☐ Tidy room          ║
║ ☐ Feed pets          ║
╠══════════════════════╣
║ ☐ Vacuum floors      ║
║ ☐ Mop floors         ║
║ ☐ Clean bathroom     ║
║ ☐ Do laundry         ║
║ ☐ Change sheets      ║
╚══════════════════════╝
    """,
    "Krampus Visit": """
                                              ,--,  ,.-.
                ,                   \,       '-,-`,'-.' | ._
               /|           \    ,   |\         }  )/  / `-,',
               [ '          |\  /|   | |        /  \|  |/`  ,`
               | |       ,.`  `,` `, | |  _,...(   (      _',
               \  \  __ ,-` `  ,  , `/ |,'      Y     (   \_L\ 
                \  \_\,``,   ` , ,  /  |         )         _,/
                 \  '  `  ,_ _`_,-,<._.<        /         /
                  ', `>.,`  `  `   ,., |_      |         /
                    \/`  `,   `   ,`  | /__,.-`    _,   `\ 
                -,-..\  _  \  `  /  ,  / `._) _,-\`       \ 
                 \_,,.) /\    ` /  / ) (-,, ``    ,        |
                ,` )  | \_\       '-`  |  `(               \ 
               /  /```(   , --, ,' \   |`<`    ,            |
              /  /_,--`\   <\  V /> ,` )<_/)  | \      _____)
        ,-, ,`   `   (_,\ \    |   /) / __/  /   `----`
       (-, \           ) \ ('_.-._)/ /,`    /
       | /  `          `/ \\ V   V, /`     /
    ,--\(        ,     <_/`\\     ||      /
   (   ,``-     \/|         \-A.A-`|     /
  ,>,_ )_,..(    )\          -,,_-`  _--`
 (_ \|`   _,/_  /  \_            ,--`
  \( `   <.,../`     `-.._   _,-`
   `                      ```
    """,
    "IOU": """
    Not enough gifts!
    """
}

# Global data variables
children = []
gift_inventory = {}

# Function to calculate the score given from behaviour questions. Also 
def calculate_behaviour_score(child, simulate=False):
    score = 0
    child.responses = []
    
    # Ask questions and sum points to set score
    for question, freq_points, sometimes_points, never_points in behaviour_questions:
        if simulate:
            if freq_points > 0:
                rand = random.random()
                if rand < 0.15:
                    answer, points = "never", never_points
                elif rand < 0.40:
                    answer, points = "sometimes", sometimes_points
                else:
                    answer, points = "frequently", freq_points
            else:
                rand = random.random()
                if rand < 0.60:
                    answer, points = "never", never_points
                elif rand < 0.85:
                    answer, points = "sometimes", sometimes_points
                else:
                    answer, points = "frequently", freq_points
        else:
            while True:
                answer = input(f"{question} (frequently/sometimes/never): ").lower().strip()
                if answer in ["frequently", "f", "sometimes", "s", "never", "n"]:
                    if answer.startswith("f"):
                        answer, points = "frequently", freq_points
                    elif answer.startswith("s"):
                        answer, points = "sometimes", sometimes_points
                    else:
                        answer, points = "never", never_points
                    break
        
        score += points
        child.responses.append((question, answer, points))
    
    # Apply name-based modifiers
    name_upper = child.name.upper()
    
    # Double letters -> +5
    for i in range(len(name_upper) - 1):
        if name_upper[i] == name_upper[i + 1] and name_upper[i].isalpha():
            score += 5
            break
    
    # All unique letters -> -4
    letters_only = [c for c in name_upper if c.isalpha()]
    if len(set(letters_only)) == len(letters_only) and len(letters_only) > 0:
        score -= 4
    
    # Lucky first letter (A, J, S) -> +6
    if name_upper and name_upper[0] in {"A", "J", "S"}:
        score += 6
    
    # RNG modifier (-3 to +3)
    score += random.randint(-3, 3)
    
    child.score = score
    return score


# Function to split children into groups (naugthy, angelic, etc) based on their behaviour scores
def categorize_child(child):
    
    score = child.score

    if score >= 70:
        child.category = "angelic"
    elif score >= 30:
        child.category = "nice"
    elif score >= -30:
        child.category = "naughty"
    else:
        child.category = "evil"

    return child.category

# Function to Assign gifts besed on child's category, gender, and inventory avaiability.
def assign_gift(child):
    category = child.category
    gender = child.gender
    
    available_gifts = []
    gift_bias = []
    
    # Define which gifts belong to each category
    angelic_gifts = ["Remote Control Car", "Doll Set", "Video Game Console", "Bike"]
    nice_gifts = [ "Art Kit", "Soccer Ball", "Rubicks Cube", "LEGO Set"]
    naughty_gifts = ["Coal", "Socks", "Chores List"]
    
    # Filter by category
    #Angelic gifts assignment
    if category == "angelic":
        for gift_name in angelic_gifts:
            if gift_name in gift_inventory:
                info = gift_inventory[gift_name]
                if info["gender"] == "ALL" or gender == "X" or info["gender"] == gender:
                    available_gifts.append(gift_name)
                    gift_bias.append(info["bias"])

    #nice gifts assignment
    elif category == "nice":
        for gift_name in nice_gifts:
            if gift_name in gift_inventory:
                info = gift_inventory[gift_name]
                if info["gender"] == "ALL" or gender == "X" or info["gender"] == gender:
                    available_gifts.append(gift_name)
                    gift_bias.append(info["bias"])

    #naughty gifts assignment
    elif category == "naughty":
        for gift_name in naughty_gifts:
            if gift_name in gift_inventory:
                info = gift_inventory[gift_name]
                if info["quantity"] > 0:
                    available_gifts.append(gift_name)
                    gift_bias.append(info["bias"])

    else:  # evil
        available_gifts = ["Krampus Visit"]
        gift_bias = [100]
    
    # Assign IOU if gift not avaiable
    if not available_gifts:
        child.gift = "IOU"
        return
    
    # Weighted random selection
    total_weight = sum(gift_bias)
    if total_weight == 0:
        selected_gift = random.choice(available_gifts)
    else:
        rand = random.random() * total_weight
        cumulative = 0
        selected_gift = available_gifts[0]
        for i, weight in enumerate(gift_bias):
            cumulative += weight
            if rand <= cumulative:
                selected_gift = available_gifts[i]
                break
    
    child.gift = selected_gift
    gift_inventory[selected_gift]["quantity"] -= 1


#Function to generate a summary with percentages and relevant information about the children/data
def generate_summary_statistics(children_list):
    total = len(children_list)
    if total == 0:
        print("\n❌ No children to analyze!")
        return
    
    #Count by category
    category_counts = {"evil": 0, "naughty": 0, "nice": 0, "angelic": 0}
    for child in children_list:
        category_counts[child.category] = category_counts.get(child.category, 0) + 1
    
    #calculate percentages
    category_percentages = {}
    for cat in category_counts:
        category_percentages[cat] = (category_counts[cat] / total) * 100
    
    #finding most common gift
    gift_counts = {}
    for child in children_list:
        gift = child.gift
        gift_counts[gift] = gift_counts.get(gift, 0) + 1
    
    most_common_gift = max(gift_counts, key=gift_counts.get, default="None")
    
    #Checking leftover in inventory
    leftover_inventory = []
    for gift_name, info in gift_inventory.items():
        if info["quantity"] > 0:
            leftover_inventory.append((gift_name, info["quantity"]))
    
    # Printing formatted stats
    print("\n" + "="*70)
    print("📊 SUMMARY STATISTICS 📊")
    print("="*70)
    print(f"Total Children: {total}")
    print("\nCategory Distribution:\n")

    for cat in ["angelic", "nice", "naughty", "evil"]:
        count = category_counts.get(cat, 0)
        pct = category_percentages.get(cat, 0)
        print(f"  {cat.upper()}: {count:3} children ({pct:5.1f}%)")
    
    #printing most common gift
    print(f"\nMost Common Gift: {most_common_gift} ({gift_counts.get(most_common_gift, 0)} times)")
    
    #Printing leftover gift storage
    print("\n\nLeftover Inventory:\n")
    if leftover_inventory:
        for gift_name, quantity in leftover_inventory:
            print(f"  {gift_name}: {quantity} remaining")
    else:
        print("  None - all gifts distributed!")
    
    print("="*70)


# Sets the avaiability per gift in the inventory
def set_inventory():
    global gift_inventory
    gift_inventory = {}
    for name, quantity, gender, bias in GIFT_INVENTORY:
        gift_inventory[name] = {
            "quantity": quantity,
            "gender": gender,
            "bias": bias,
            "original_quantity": quantity
        }


#Function to get statistics clorer to the expected values
def adjust_category_percentages(children_list):
    total_children = len(children_list)
    if total_children == 0:
        return
    
    # Calculating percentages
    category_counts = {"evil": 0, "naughty": 0, "nice": 0, "angelic": 0}
    for child in children_list:
        category_counts[child.category] = category_counts.get(child.category, 0) + 1 #plus one due to counting - starts at 0 - tried without and was getting an error so this appears to work out well :)
    
    current_percentages = {}
    for cat in category_counts:
        current_percentages[cat] = (category_counts[cat] / total_children) * 100
    
    # Adjust categories
    for cat in ["nice", "naughty", "evil", "angelic"]:
        min_target, max_target = target_percentages[cat]
        current = current_percentages.get(cat, 0)
        
        if current < min_target:
            needed = int((min_target - current) / 100 * total_children)
            candidates = []
            
            if cat == "nice":
                for child in children_list:
                    if child.category == "naughty" and child.score >= 15:
                        candidates.append((child, abs(child.score - 20)))
            elif cat == "angelic":
                for child in children_list:
                    if child.category == "nice" and child.score >= 65:
                        candidates.append((child, abs(child.score - 70)))
            
            candidates.sort(key=lambda x: x[1])
            for i in range(min(needed, len(candidates))):
                candidates[i][0].category = cat
        
        elif current > max_target:
            excess = int((current - max_target) / 100 * total_children)
            candidates = []
            
            if cat == "nice":
                for child in children_list:
                    if child.category == "nice" and child.score <= 30:
                        candidates.append((child, abs(child.score - 20)))
            elif cat == "angelic":
                for child in children_list:
                    if child.category == "angelic" and child.score <= 75:
                        candidates.append((child, abs(child.score - 70)))
            elif cat == "naughty":
                for child in children_list:
                    if child.category == "naughty" and child.score >= 15:
                        candidates.append((child, abs(child.score - 20)))
            
            candidates.sort(key=lambda x: x[1])
            for i in range(min(excess, len(candidates))):
                if cat == "nice":
                    candidates[i][0].category = "naughty"
                elif cat == "angelic":
                    candidates[i][0].category = "nice"
                elif cat == "naughty":
                    if candidates[i][0].score >= 15:
                        candidates[i][0].category = "nice"
                    else:
                        candidates[i][0].category = "evil"
    
    # Reassign gifts
    # Reset inventory before reassigning gifts
    set_inventory()

    for child in children_list:
        child.gift = ""
        assign_gift(child)

# Function to print detailed report for each child
def print_per_child_report(child):
    print("\n" + "="*70)
    print(f"🎁 PER-CHILD REPORT: {child.name.upper()} 🎁")
    print("="*70)
    print(f"Name: {child.name}")
    print(f"Gender: {child.gender}")
    print(f"behaviour Score: {child.score} points")
    print(f"Final Category: {child.category.upper()}")
    print(f"Assigned Gift: {child.gift}")
    art = GIFT_ART.get(child.gift, "")
    print(art)

    # Printing question responses per child
    print("\nQuestion Responses:\n")
    for question, answer, points in child.responses:
        print(f"  - {question[:50]}...")
        print(f"    Answer: {answer} | Points: {points:+d}\n")
    
    print("="*70)

# Function to print all children grouped by category - naughty, nice, etc
def print_category_lists(children_list):
    categories = ["angelic", "nice", "naughty", "evil"]
    
    print("\n" + "="*70)
    print("📋 CHILDREN BY CATEGORY 📋")
    print("="*70)
    
    # Grouping and printing children by category
    for category in categories:
        category_children = [c for c in children_list if c.category == category]
        if category_children:
            print(f"\n{category.upper()} ({len(category_children)} children):")
            print("-" * 70)
            for child in category_children:
                print(f"  {child.name:<20} Score: {child.score:>4} | Gift: {child.gift}")
    print("="*70)

# Function to print heading with project title - mostly for aesthetics
def heading():
    print("\n" + "="*70)
    print("🎄 SANTA'S NAUGHTY/NICE ANALYTICS SYSTEM 🎅")
    print("="*70)
    print("AP Computer Science Christmas Project")
    print("="*70)

# Main loop for execution of the program
def main():
    global children
    
    set_inventory()
    
    heading()
    
    #Loop till user exits
    while True:
        print("\nMenu:\n")
        print("  1. Add child manually")
        print("  2. Simulate 20 children")
        print("  3. View per-child reports")
        print("  4. View category lists")
        print("  5. Generate summary statistics")
        print("  6. Use data percentage approximation")
        print("  7. Clear all data")
        print("  8. Exit")
        
        choice = input("\nChoice: ").strip()
        
        if choice == "1":
            name = input("\nChild's name: ").strip()
            if name:
                while True:
                    gender = input("Gender (M/F/X): ").strip().upper()
                    if gender in ["M", "F", "X"]:
                        break
                    print("Please enter M, F, or X")
                
                child = Child(name, gender)
                calculate_behaviour_score(child, simulate=False)
                categorize_child(child)
                assign_gift(child)
                children.append(child)

                os.system("clear")
                heading()
                print_per_child_report(child)
        
        elif choice == "2":
            os.system("clear")
            heading()

            print("\n🎲 Simulating 20 children...")
            children.clear()
            set_inventory()
            
            names = ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", 
                     "Henry", "Ivy", "Jack", "Kate", "Liam", "Mia", "Noah", 
                     "Olivia", "Paul", "Quinn", "Ruby", "Sam", "Tina"]
            genders = ["M", "F", "X"]
            
            for name in names:
                gender = random.choice(genders)
                child = Child(name, gender)
                calculate_behaviour_score(child, simulate=True)
                categorize_child(child)
                children.append(child)
            
            for child in children:
                assign_gift(child)
            
            print(f"\n✅ Simulated {len(children)} children!")
            generate_summary_statistics(children)
        
        elif choice == "3":
            os.system("clear")
            heading()

            if not children:
                print("\n❌ No children added yet!")
            else:
                for child in children:
                    print_per_child_report(child)
        
        elif choice == "4":
            os.system("clear")
            heading()

            if not children:
                print("\n❌ No children data yet!")
            else:
                print_category_lists(children)
        
        elif choice == "5":
            os.system("clear")
            heading()

            generate_summary_statistics(children)
        
        elif choice == "6":
            if not children:
                print("\n❌ No children to adjust!")
            else:
                os.system("clear")
                heading()

                print("\n🔄 Applying percentage requests...")
                adjust_category_percentages(children)
                print("✅ Categories adjusted!")
                generate_summary_statistics(children)
        
        elif choice == "7":
            if input("\nClear all data? (yes): ").strip().lower() == "yes":
                children.clear()
                set_inventory()

                os.system("clear")
                heading()
                print("✅ All data cleared!")
        
        elif choice == "8":
            print("\n🎅 Thank you for using Santa's Analytics System! 🎄\n")
            break
        
        else:
            print("❌ Invalid choice.")


if __name__ == "__main__":
    os.system("clear")
    main()
    print("🎅 Marry Christmas and Goodbye! 🎄")

