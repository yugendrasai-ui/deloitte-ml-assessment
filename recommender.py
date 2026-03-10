import pandas as pd
from difflib import get_close_matches

def load_data(file_path='data.csv'):
    """
    Loads the book dataset from a CSV file using pandas.
    """
    try:
        df = pd.read_csv(file_path)
        # Ensure column names are clean
        df.columns = [col.strip() for col in df.columns]
        return df
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return None

def get_similar_titles(book_title, df):
    """
    Uses fuzzy matching to suggest similar book titles if an exact match isn't found.
    Normalizes case for better matching reliability.
    """
    # Create a mapping of lowercase titles to original titles
    titles_map = {title.lower(): title for title in df['Book'].tolist()}
    
    # Get matches against the lowercase titles
    matches = get_close_matches(book_title.lower(), titles_map.keys(), n=3, cutoff=0.3)
    
    # Return the original case titles
    return [titles_map[m] for m in matches]

def get_recommendations(book_title, df, num_recommendations=3):
    """
    Finds books with the same genre as the input book.
    Handles case-insensitive search.
    """
    # Find the input book using case-insensitive comparison
    book_row = df[df['Book'].str.lower() == book_title.lower()]
    
    if book_row.empty:
        return None
    
    # Get the genre and actual title of the selected book
    genre = book_row.iloc[0]['Genre']
    actual_title = book_row.iloc[0]['Book']
    
    # Filter books in the same genre, excluding the original book
    recommendations = df[
        (df['Genre'] == genre) & 
        (df['Book'].str.lower() != book_title.lower())
    ]
    
    # Sort recommendations by rating in descending order
    recommendations = recommendations.sort_values(by='Rating', ascending=False)
    
    return recommendations.head(num_recommendations)

def get_top_rated(df, n=5):
    """
    Returns the top N highest-rated books in the dataset.
    """
    return df.sort_values(by='Rating', ascending=False).head(n)
