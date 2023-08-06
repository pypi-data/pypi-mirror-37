This is used to check files stored with the hash from the internet

- Install with `pip install md5-checksum-verifier`
____________
Functions:
```python
from hash-tool import verifytool
verifytool.validHash('md5-hash-here')#this will return True when a hash is valid, and false if invalid (this just checks if it is in the format of an md5 hash)
verifytool.genhash('filenamehere')#this will generate and return the hash of a file
verifytool.validate('hash','original file source via the internet')
```

Example use:
```python
from hash-tool import verifytool
try:
    localFile=verifytool.genhash('text.txt')#generates and stores the hash
    if verifytool.validHash(localFile) == True:
        try:
            if verifytool.validate(localFile,'https://web.org/test-original.txt') == True:
                print("File has not been tampered with")
        except:
            print("Invalid hash - file may have been tampered with")
    else:
        print("Issue generating hash")
except:
    print("Issue generating hash")
```