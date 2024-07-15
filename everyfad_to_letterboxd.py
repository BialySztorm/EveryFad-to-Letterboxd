import json
import csv
import math
import os


def create_file(data):
    print("Creating files...")
    for (key, value) in data.items():
        if (len(value) == 0):
            continue
        with open(f"{key}.csv", "w", newline="") as file:
            keys = value[0].keys()
            writer = csv.writer(file)
            writer.writerow(keys)
            for movie in value:
                writer.writerow(list(movie.values()))


def round_mathematically(x):
    if x - math.floor(x) < 0.5:
        return math.floor(x)
    else:
        return math.ceil(x)


def get_data():
    print("Getting data...")
    is_valid = [True, True]
    watched = reviews = []
    try:
        watched = json.load(open("movies_watched.json"))
    except FileNotFoundError:
        print("movies_watched.json not found. Please make sure the file is in the same directory as this script.")
        is_valid[0] = False
    try:
        reviews = json.load(open("movies_reviews.json"))
    except FileNotFoundError:
        print("movies_reviews.json not found. Please make sure the file is in the same directory as this script.")
        is_valid[1] = False
    watched_movies = []
    if is_valid[0]:
        for movie in watched:
            watchedDate = movie["watchedDate"].split("T")[0] if movie["watchedDate"] else ""
            if (len(watchedDate) <= 4 and watchedDate):
                watchedDate += "-01-01"
            elif (len(watchedDate) <= 7 and watchedDate):
                watchedDate += "-01"
            review = [review for review in reviews if review["movie"]["femaId"] == movie["movie"]["femaId"]]
            if (review and is_valid[1]):
                watched_movies.append({
                    "tmdbId": movie["movie"]["tmdbId"],
                    "imdbId": movie["movie"]["imdbId"],
                    "Title": movie["movie"]["name"],
                    "Year": movie["movie"]["year"],
                    "Rating": round_mathematically(review[0]["review"]["rating"]/10),
                    "WatchedDate": watchedDate,
                    "Review": review[0]["review"]["review"]
                })
            else:
                watched_movies.append({
                    "tmdbId": movie["movie"]["tmdbId"],
                    "imdbId": movie["movie"]["imdbId"],
                    "Title": movie["movie"]["name"],
                    "Year": movie["movie"]["year"],
                    "Rating": "",
                    "WatchedDate": watchedDate,
                    "Review": ""
                })
        print(f"Found movies_watched.json with {len(watched_movies)} movies.")

    other = {}
    target_contain = 'MoviesFad-'
    for file in os.listdir("."):
        if target_contain in file:
            suffix = file.split(target_contain)[1].split(".")[0]
            try:
                tmp = []
                data = json.load(open(file))
                for movie in data:
                    tmp.append({
                        "tmdbId": movie["item"]["tmdbId"],
                        "imdbId": movie["item"]["imdbId"],
                        "Title": movie["item"]["name"],
                        "Year": movie["item"]["year"]
                    })
                other[suffix] = tmp
                print(f"Found {file} with {len(tmp)} movies.")
            except FileNotFoundError:
                print(f"{file} not found. Please make sure the file is in the same directory as this script.")

    return {
        "watched": watched_movies,
        **other
    }


def prepare_files():
    target_contain = 'MoviesFad'
    for file in os.listdir("."):
        if target_contain in file:
            suffix = file.split(target_contain)[1]
            if ("MoviesFad"+suffix == file):
                continue
            print(f"Renaming {file} to MoviesFad{suffix}")
            os.rename(file, f"MoviesFad{suffix}")


if __name__ == "__main__":
    prepare_files()
    data = get_data()
    create_file(data)
