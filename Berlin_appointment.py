import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By

# url for specific department, given url for testing purpose 
url = "https://service.berlin.de/terminvereinbarung/termin/restart/?providerList=122207&requestList=121921&source=dldb"
driver = webdriver.Firefox()    # Webdriver have to be in same folder as script
time_refresh = 5                # Time to wait before refreshing page, DDOS block after about 15 attempts/min or about 50 attempts/hour

name = "Peter Rabbit"           # Enter first name and familyname for appointment
email = "peterrabbit@web.de"    # Enter email for appointment 
phonenumber = "0172123123123"   # Enter phonenumber for appointment

def randwait():
    """Wait for some time to appear human"""
    return(random.uniform(0.02,0.06))

def main():
    chechappointments()

def chechappointments():
    print("------------------------------------")
    print("Webdriver Firefox started")
    driver.get(url)
    
    k = 0
    while True:
        time.sleep(randwait())
        
        try:                    # Test if anti-DDOS is active
            ddos_test = driver.find_element(By.LINK_TEXT, value="Zu viele Zugriffe")
            print("Too many connection attempts. Increase value of time_refresh!")
            break
        except:
            pass

        findmonths = driver.find_elements(By.CLASS_NAME, "month")
        month0 = findmonths[0].text
        month1 = findmonths[1].text

        button_buchbar = driver.find_elements(By.CLASS_NAME, "buchbar")
        button_nichtbuchbar = driver.find_elements(By.CLASS_NAME, "nichtbuchbar")
        nr_buchbar = len(button_buchbar)-1
        nr_nichtbuchbar = len(button_nichtbuchbar)-1
        print("Number of possible appointments in",month0,"and",month1,":",nr_buchbar+nr_nichtbuchbar)
        print("Bookable:",nr_buchbar, "  Not bookable:",nr_nichtbuchbar)

        if nr_buchbar > 0:
            time.sleep(randwait())
            print("First free appointment is being booked...")
            button_buchbar[1].click()

            time.sleep(randwait())
            button_buchbar_zeit = driver.find_element(By.LINK_TEXT, value="Diesen Termin buchen")
            button_buchbar_zeit.click()

            time.sleep(randwait())
            field_name = driver.find_element(By.ID, value="familyName")
            field_email = driver.find_element(By.ID, value="email")
            field_phonenumber = driver.find_element(By.ID, value="telephone")
            field_name.send_keys(name)
            field_email.send_keys(email)
            field_phonenumber.send_keys(phonenumber)

            check_agb = driver.find_element(By.ID, value="agbgelesen")
            check_agb.click()

            time.sleep(randwait())

            button_finish = driver.find_element(By.ID, value="register_submit")
            button_finish.click()       # Remove comment when finished...
            driver.quit()               # Remove comment when finished...
            print("Appointment booked.")
            print("------------------------------------")
            break
            
        if nr_buchbar == 0:
            k += 1
            print("No appointment available! Attempt nr.",k,"Refreshing page...")
            print("------------------------------------")
            time.sleep(time_refresh)
            driver.refresh()
            
            
    print("Webdriver Ende")
    
if __name__ == '__main__':
    main() 
