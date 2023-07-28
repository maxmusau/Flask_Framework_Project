# sending an sms
import africastalking
africastalking.initialize(
    username="yohalohari",
    api_key="881fd1fe55efd93059daaa1922bbb409e5768f23e5794eae65f8e70895e373e6"
    #justpaste.it/1nua8
)
sms = africastalking.SMS
def send_sms(phone, message):
    recipients = [phone]
    sender = "AFRICASTKNG"
    try:
        response = sms.send(message, recipients)
        print(response)
    except Exception as error:
        print("Error is ", error)
def generate_random():
    # initializing size of string
    import string    
    import random # define the random module  
    S = 5  # number of characters in the string.  
    # call random.choices() string module to find the string in Uppercase + numeric data.  
    ran = ''.join(random.choices(string.ascii_uppercase + string.digits, 
    k = S))    
    print("The randomly generated string is : " + str(ran)) # print the random data  
    return str(ran)
generate_random()