"""
Count and plot the frequencies of keywords
in software projects

This was a quick hack, do email me with your suggestions for the exact analysis
abhinav.tushar.vs@gmail.com
"""

import os
import re
import numpy as np
from matplotlib import pyplot as plt
import keys
import argparse


def analyze(directory, extensions, keywords):

    files = []
    frequencies = np.zeros(len(keywords))
    for root, dirs, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith(extensions):
                files.append(os.path.join(root, filename))

    total_files = len(files)

    for file_idx, source_file in enumerate(files):
        print("Searching in file " + str(file_idx + 1) + " of " + str(total_files))
        with open(source_file, "r") as f:
            content = f.read()
            for idx, word in enumerate(keywords):
                regex = re.compile(ur"\b" + word + "[^a-zA-Z]", re.MULTILINE)
                frequencies[idx] += len(regex.findall(content))

    # Plotting
    zipf = np.zeros(len(keywords))
    for i in range(len(keywords)):
        zipf[i] = 1.0 / (i + 1)

    zipf *= np.max(frequencies)

    sort_idx = np.argsort(frequencies)
    sorted_freq = frequencies[sort_idx]
    sorted_words = np.array(keywords)[sort_idx]
    sorted_freq = sorted_freq[::-1]
    sorted_words = sorted_words[::-1]

    plt.style.use("ggplot")
    fig, ax = plt.subplots()
    # Plotting first 50, if more are available
    ax.plot(zipf[:50])
    ax.plot(sorted_freq[:50], "o")
    plt.xticks(np.arange(min(50, len(keywords))), sorted_words[:50], rotation = 90)
    plt.title(directory + " vs Zipfian")
    plt.ylabel("Frequencies")
    plt.show()


parser = argparse.ArgumentParser(description="zipf creates frequency distributions of keywords in software projects.")
parser.add_argument("directory",
                    help="project directory")
parser.add_argument("lang",
                    help="dominant language of the project (js|python|c_cpp|java)",)

args = parser.parse_args()

if args.lang == "java":
    analyze(args.directory, (".java"), keys.java)
elif args.lang == "js":
    analyze(args.directory, (".js"), keys.js)
elif args.lang == "c_cpp":
    analyze(args.directory, (".c", ".h", ".cpp"), keys.c_cpp)
elif args.lang == "python":
    analyze(args.directory, (".py"), keys.python)
else:
    print("Unknown language, please add the keys in keys.py and modify this script")
