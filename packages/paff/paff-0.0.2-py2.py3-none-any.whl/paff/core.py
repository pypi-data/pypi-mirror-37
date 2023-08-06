# -*- coding: utf-8 -*-
"""
paff.core - the basic ingredients to great data consistency
"""

import os
import operator
import hashlib

import progressbar

from .data import hashData


# ToDo: Work on writing the md5 data to custom location... in home folder... save MD5 for later use... this allows
# for the command to be stopped and started again, without performance issues
def getMD5forDirectory(path):
    print("Get file list from device...", end=" ", flush=True)
    #files = [file for file in glob.glob(path + "/**/*", recursive=True)]
    files = []
    for root, dirname, filenames in os.walk(path):
        for filename in [f for f in filenames if not f[0] == "."]:
            files.append(os.path.join(root, filename))
    print("Get file list from device... Found %d files." % len(files), flush=True)
    hashes = {}
    bar = progressbar.ProgressBar(redirect_stdout=True)  # print("Calculate md5 checksum for files...")
    countCache = 0
    for file in bar(files):
        file_hash = None
        use_cache = False
        if hashData.pathExists(file):
            file_hash = hashData.getHash(file)
            countCache += 1
            use_cache = True
        else:
            hash_md5 = hashlib.md5()
            with open(file, "rb") as f:
                for chunk in iter(lambda: f.read(8192), b""):
                    hash_md5.update(chunk)
            file_hash = hash_md5.hexdigest()
            hashData.addHash(file, file_hash)
        hashes[file_hash] = file
        if use_cache:
            print(file_hash + " - " + file + " (Cached)", flush=True)
        else:
            print(file_hash + " - " + file, flush=True)
    print("Succesfully loaded directory: " + path + " (%d loaded from Cache)" % countCache)
    return hashes


def getNamesforDirectory(path):
    print("Get file list from device...", end=" ", flush=True)
    # files = [file for file in glob.glob(path + "/**/*", recursive=True)]
    files = []
    for root, dirname, filenames in os.walk(path):
        for filename in [f for f in filenames if not f[0] == "."]:
            files.append(os.path.join(root, filename))
    print("Get file list from device... Found %d files." % len(files), flush=True)
    names = {}
    bar = progressbar.ProgressBar(redirect_stdout=True)  # print("Calculate md5 checksum for files...")
    for file in bar(files):
        name = os.path.basename(file)
        names[name] = file
        print(name + " - " + file, flush=True)
    print("Succesfully loaded directory: " + path)
    return names


def getDatesforDirectory(path):
    print("Get file list from device...", end=" ", flush=True)
    # files = [file for file in glob.glob(path + "/**/*", recursive=True)]
    files = []
    for root, dirname, filenames in os.walk(path):
        for filename in [f for f in filenames if not f[0] == "."]:
            files.append(os.path.join(root, filename))
    print("Get file list from device... Found %d files." % len(files), flush=True)
    names = {}
    bar = progressbar.ProgressBar(redirect_stdout=True)  # print("Calculate md5 checksum for files...")
    for file in bar(files):
        date = os.path.getmtime(file)
        name = os.path.basename(file)
        names[(name, date)] = file
        print(name + " - " + file, flush=True)
    print("Succesfully loaded directory: " + path)
    return names


def checkPathExistence(paths):
    """ returns all paths that do not exist anymore """
    missingPaths = []
    for path in paths:
        if not os.path.exists(path):
            missingPaths.append(path)

    return missingPaths


def compareHashesFromDirectory(hashes1, hashes2):
    """ hashes 1 is the goal. Removes everything from hashes 2 thats already there.
    returns all elements that are only in one of the two arrays. """
    deletableHashes = []
    for key, value in hashes1.items():
        if key in hashes2:
            deletableHashes.append(key)
    for h in deletableHashes:
        print("Common item: " + str(h))
        del hashes1[h]
        del hashes2[h]

    return hashes1, hashes2


def printLeftovers(path, leftovers):
    print("Leftovers from " + path)
    for key, value in sorted(leftovers.items(), key=operator.itemgetter(1)):
        print(str(key) + " - " + value)
    print("Found %d files that are missing." % len(leftovers.items()))