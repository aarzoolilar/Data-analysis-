import pandas as pd
import matplotlib.pyplot as plt
import time
from datetime import datetime
import os

# ========== Save Results ==========
def save_result(name, score, total):
    percentage = (score / total) * 100
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    new_data = pd.DataFrame([[name, score, total, f"{percentage:.2f}%", date]],
                            columns=["Name", "Score", "Total", "Percentage", "Date"])

    if os.path.exists("results.csv"):
        old_data = pd.read_csv("results.csv")
        final = pd.concat([old_data, new_data], ignore_index=True)
    else:
        final = new_data

    final.to_csv("results.csv", index=False)
    print("\n✅ Result saved successfully!\n")


# ========== View Previous Results ==========
def view_results():
    if os.path.exists("results.csv"):
        df = pd.read_csv("results.csv")
        print("\n=== 🧾 Previous Quiz Results ===\n")
        print(df.to_string(index=False))
    else:
        print("\n⚠️ No previous results found.\n")


# ========== Run the Quiz ==========
def run_quiz(name):
    try:
        df = pd.read_excel("quiz.xlsx")
    except FileNotFoundError:
        print("⚠️ quiz_questions.xlsx file not found!")
        return

    questions = df.sample(frac=0.02).reset_index(drop=True)
    score = 0
    wrong_questions = []

    print(f"\n🎯 Welcome {name}! Let's start the quiz.\n")
    time.sleep(1)

    for index, row in questions.iterrows():
        print(f"Q{index+1}: {row['Question']}")
        print(f"A. {row['Option A']}")
        print(f"B. {row['Option B']}")
        print(f"C. {row['Option C']}")
        print(f"D. {row['Option D']}")

        start = time.time()
        ans = input("Your Answer: ").strip().upper()
        end = time.time()
        print(f"⏱ You took {end - start:.2f} seconds.\n")


        if end - start > 15:
            print("⏰ Time’s up! No points awarded.\n")
            continue

        if ans == row["Answer"].upper():
            print("✅ Correct!\n")
            score += 1
        else:
            print(f"❌ Wrong! Correct answer: {row['Answer']}\n")
            wrong_questions.append(row['Question'])

    total = len(questions)
    percentage = (score / total) * 100

    # Summary
    print("\n----- QUIZ SUMMARY -----")
    print(f"Total Questions: {total}")
    print(f"Correct Answers: {score}")
    print(f"Wrong Answers: {total - score}")
    print(f"Accuracy: {percentage:.2f}%")
    print("------------------------")

    # Save results
    save_result(name, score, total)

    # Pie chart
    labels = ['Correct', 'Incorrect']
    sizes = [score, total - score]
    colors = ["#79BBDC", "#B47CC1"]

    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    plt.legend()
    plt.title(f"{name}'s Quiz Performance")
    plt.show()


# ========== Main Menu ==========
def main_menu():
    while True:
        print("\n==== QUIZ GENERATOR & ANALYZER ====")
        print("1. Take Quiz")
        print("2. View Previous Results")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter your name: ").strip()
            run_quiz(name)
        elif choice == '2':
            view_results()
        elif choice == '3':
            print("\n👋 Goodbye! Thanks for using Quiz Generator.\n")
            break
        else:
            print("❗Invalid choice, please try again.\n")


# Run program
if __name__ == "__main__":
    main_menu()
