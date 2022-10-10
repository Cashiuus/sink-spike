import fnmatch
import os



def find_and_build_filelist(pattern, root='/', search_type='file'):
    """ A helper function that only works for Unix filename matching by providing an iterable
        on dirs or files that match the given pattern.

        search_type     Can be either "dir" or "file"

        Usage: 
            SEARCH = ".git"
            for item in find_and_build_filelist(SEARCH, search_type='dir'):
                # Do stuff to each matched directory
                
            SEARCH = "*.php"
            for item in find_and_build_filelist(SEARCH, search_type='file'):
                # Do stuff to each matched file

    """
    for path, dirs, files in os.walk(os.path.abspath(root)):
        if search_type == 'dir':
            for d in fnmatch.filter(dirs, pattern):
                yield os.path.join(path, d)
        elif search_type == 'file':
            for f in files:
                if fnmatch.fnmatch(f, pattern):
                    yield os.path.join(path, f)
            


if __name__ == '__main__':
    # Example
    SEARCH = "*.php"
    results = []
    for item in find_and_build_filelist(SEARCH, root=".", search_type='file'):
        # Do stuff to each matched file
        results.append(item)
        # Could search inside each file here
    print(f"[*] Found {len(results)} matching files")
    if len(results) < 15:
        for i in results:
            print(f"{i}")
    print()
