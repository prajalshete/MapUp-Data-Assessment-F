import pandas as pd
from sklearn.metrics.pairwise import haversine_distances
from math import radians

def calculate_distance_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame): DataFrame with 'id', 'lat', and 'lon' columns.

    Returns:
        pandas.DataFrame: Distance matrix
    """
    # Calculate distance matrix using haversine formula
    lat_lon_rad = df[['lat', 'lon']].applymap(radians)
    distances = haversine_distances(lat_lon_rad, lat_lon_rad) * 6371000  # Earth radius in meters

    # Convert distance matrix to DataFrame
    distance_matrix = pd.DataFrame(distances, index=df['id'], columns=df['id'])

    return distance_matrix

# Example usage
# Assuming 'your_dataset_with_lat_lon.csv' is the name of your CSV file
df_with_lat_lon = pd.read_csv('your_dataset_with_lat_lon.csv')
result_distance_matrix = calculate_distance_matrix(df_with_lat_lon)
print(result_distance_matrix)
def unroll_distance_matrix(distance_matrix: pd.DataFrame) -> pd.DataFrame:
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        distance_matrix (pandas.DataFrame): Distance matrix

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
    # Unroll distance matrix
    unrolled_df = distance_matrix.unstack().reset_index()
    unrolled_df.columns = ['id_start', 'id_end', 'distance']

    return unrolled_df

# Example usage
result_unrolled_distance_matrix = unroll_distance_matrix(result_distance_matrix)
print(result_unrolled_distance_matrix)
def find_ids_within_ten_percentage_threshold(df: pd.DataFrame, reference_id: int) -> pd.DataFrame:
    """
    Find all IDs whose average distance lies within 10% of the average distance of the reference ID.

    Args:
        df (pandas.DataFrame): Unrolled DataFrame containing 'id_start', 'id_end', and 'distance'.
        reference_id (int): Reference ID

    Returns:
        pandas.DataFrame: DataFrame with IDs whose average distance is within the specified percentage threshold
                          of the reference ID's average distance.
    """
    # Calculate average distance for each ID
    avg_distances = df.groupby('id_start')['distance'].mean()

    # Calculate average distance for the reference ID
    reference_avg_distance = avg_distances.loc[reference_id]

    # Find IDs within 10% threshold
    ids_within_threshold = avg_distances[(avg_distances >= 0.9 * reference_avg_distance) & 
                                         (avg_distances <= 1.1 * reference_avg_distance)].index

    # Filter the original DataFrame based on found IDs
    result_df = df[df['id_start'].isin(ids_within_threshold)]

    return result_df

# Example usage
# Assuming 'your_unrolled_distance_matrix.csv' is the name of your CSV file
unrolled_df = pd.read_csv('your_unrolled_distance_matrix.csv')
result_ids_within_threshold = find_ids_within_ten_percentage_threshold(unrolled_df, reference_id=1)
print(result_ids_within_threshold)
