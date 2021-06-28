import time
import hashlib
from pyfingerprint.pyfingerprint import PyFingerprint

##Fingerprint Initialization
try:
    f = PyFingerprint('COM9', 57600, 0xFFFFFFFF, 0x00000000)

    if ( f.verifyPassword() == False ):
        raise ValueError('The given fingerprint sensor password is wrong!')

except Exception as e:
    print('The fingerprint sensor could not be initialized!')
    print('Exception message: ' + str(e))
    exit(1)


print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))

def Enroll():
    try:
        print('Waiting for finger...')

        while ( f.readImage() == False ):
            pass


        f.convertImage(0x01)
        result = f.searchTemplate()
        positionNumber = result[0]

        if ( positionNumber >= 0 ):
            print('Template already exists at position #' + str(positionNumber))
            exit(0)

        print('Remove finger...')
        time.sleep(2)

        print('Waiting for same finger again...')

        while ( f.readImage() == False ):
            pass

        f.convertImage(0x02)

        if ( f.compareCharacteristics() == 0 ):
            raise Exception('Fingers do not match')

        f.createTemplate()

        positionNumber = f.storeTemplate()
        print('Finger enrolled successfully!')
        print('New template position #' + str(positionNumber))

    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        exit(1)

def Read():
    try:
        print('Waiting for finger...')

        while ( f.readImage() == False ):
            pass

        f.convertImage(0x01)

        result = f.searchTemplate()

        positionNumber = result[0]
        accuracyScore = result[1]

        if ( positionNumber == -1 ):
            print('No match found!')
            exit(0)
        else:
            print('Found template at position #' + str(positionNumber))
            print('The accuracy score is: ' + str(accuracyScore))

        f.loadTemplate(positionNumber, 0x01)

        characterics = str(f.downloadCharacteristics(0x01)).encode('utf-8')

        print('SHA-2 hash of template: ' + hashlib.sha256(characterics).hexdigest())

    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        exit(1)

def Delete():
    try:
        positionNumber = input('Please enter the template position you want to delete: ')
        positionNumber = int(positionNumber)

        if ( f.deleteTemplate(positionNumber) == True ):
            print('Template deleted!')

    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        exit(1)

print("Enter 1 to Enroll a New FingerPrint")
print("Enter 2 to Read a FingerPrint")
print("Enter 3 to Delete a FingerPrint\n")
print("So, What Do You Want To Do, Boss?")

command = int(input())
if command == 1:
    Enroll()
elif command == 2:
    Read()
else:
    Delete()