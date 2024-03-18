"""Returns the dataset to be used."""

import os

import pandas as pd


def user_datset_selection(limit: int) -> int:
    """Prompt user to select index of the datset they want to use."""
    while True:
        try:
            raw_input = int(input("Select dataset to be processed: "))

            # validate iuser input
            if 0 <= raw_input <= limit:
                return raw_input

            print("Selection not valid. Please try again.")

        except ValueError:
            print("Invalid input. Please enter a valid integer index.")


def data_resource() -> str:
    """Return the path to the data resource."""
    base_path = os.getcwd() + "/data"
    extension = ".csv"
    sample_dataset_path = os.getcwd() + "/data/sample/sample" + extension
    file_path = ""
    file_list = [file for file in os.listdir(base_path) if file.endswith(extension)]

    if len(file_list) == 0:
        print("No user data found. Using sample dataset...")
        file_path = sample_dataset_path

    elif len(file_list) > 1:
        print("Multiple user datasets found. Select the dataset to be used:")

        # list file selection options
        count = 0
        for i, name in enumerate(file_list):
            print(f"File {i}: {name}")
            count = i
        count = count + 1
        print(f"File {count}: sample{extension}")

        # take user input
        dataset_selection = user_datset_selection(count)
        assert 0 <= dataset_selection <= count, "Invalid selection."

        if dataset_selection == count:
            print("Selecting sample dataset")
            file_path = sample_dataset_path

        elif dataset_selection < count:
            file_path = os.path.join(base_path, file_list[dataset_selection])
            print("Selecting ", file_list[dataset_selection])

    else:
        file_path = os.path.join(base_path, file_list[0])

    return file_path


def read_data_file():
    """Input data from xlsx file and store in a pandas dataframe."""
    # raw_data_file_df = pd.read_excel(data_resource())
    raw_data_file_df = pd.read_csv(data_resource())

    # Number data stored as float64 by default.
    # Convert to string to avoid floating point operations
    raw_data_file_df["Amount"] = raw_data_file_df["Amount"].astype(str)

    return raw_data_file_df
