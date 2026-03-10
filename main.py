import recommender
import sys

def display_header(title):
    """Prints a formatted header for the CLI."""
    print(f"\n{'='*50}")
    print(f"{title:^50}")
    print(f"{'='*50}\n")

def display_books(df, message):
    """Helper to print a list of books in a clean format."""
    if df is None or df.empty:
        print("No books found.")
        return
    
    print(f"--- {message} ---")
    for index, row in df.iterrows():
        print(f"* {row['Book']} | Genre: {row['Genre']} | Rating: {row['Rating']}")
    print("-" * 50)

def main():
    dataset_file = 'data.csv'
    df = recommender.load_data(dataset_file)
    
    if df is None:
        print("Failed to load dataset. Please check if data.csv exists.")
        return

    while True:
        display_header("Book Recommendation System")
        print("MAIN MENU:")
        print("1. Get book recommendations")
        print("2. Show top rated books")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == '1':
            print("\nEnter a book name you like:")
            user_input = input(">>> ").strip()
            
            if not user_input:
                print("(!) Input cannot be empty. Please try again.")
                continue
            
            # 1. Try exact search (recommender handles case-insensitivity)
            results = recommender.get_recommendations(user_input, df)
            
            if results is not None:
                display_books(results, f"Recommendations based on '{user_input}'")
            else:
                # 2. Try fuzzy matching if title not found
                suggestions = recommender.get_similar_titles(user_input, df)
                print(f"\nBook '{user_input}' not found.")
                if suggestions:
                    print("Did you mean:")
                    for s in suggestions:
                        print(f"  * {s}")
                else:
                    print("No similar titles found in our database.")
                    
        elif choice == '2':
            top_books = recommender.get_top_rated(df)
            display_books(top_books, "Top 5 Highest Rated Books")
            
        elif choice == '3' or choice.lower() == 'exit':
            print("\nThank you for using the Book Recommendation System! Goodbye.\n")
            sys.exit()
            
        else:
            print("(!) Invalid choice. Please select 1, 2, or 3.")

if __name__ == "__main__":
    main()
