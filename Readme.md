Create SmartCare app for final Desd Project

# all users register as : firstname1 & password : firstname123

connect to django admin : create super user admin 
connect to admin dashbaord usr: admin1 pw: admin123
connect to nurse dashboard usr : ayan1 pw : ayan123
connect to doctor dashboard user: sandra1 pw: sandra123
connect to patient dashboard user: noah1 pw: noah123

- Ensure the consistencies between the burndown chart and the sprint backlog (e.g., in terms of the number of tasks/hours estimated).
- Demonstrate the system architecture (e.g., how many containers used, how they communicate, what they are used for).
- Demonstrate authorisation, especially in terms of protecting views/templates for specific users/roles. Use ‘permissions’ for Django Rest Framework and ‘decorators’ for vanilla Django.
- Django Super Admin dashboard should not be used as the required dashboard for admin users. The groups need to develop a dedicated admin dashboard for their systems.

# Test Cases 
## Test 1 (DONE)
- Register Mr Edmond hobbs, regiter 27 Clifton road london, N32AS, DOB: 20/12/1981, private client (patient). login and book appointment with nurse to change bandage, see nurse, and get invoice to pay, attempt to access admin dashbaord via url without login => (fail authorisation)

## Test 2 : (DONE)
- register Mr Mark healer as new doctor, with address and DOB, approve from admin, rob smith (created patient)request repeated prescription. attempt to access admin dashbaord via url (not authorised).

## Test 3 : (DONE)
- Dr First (doctor) login, and see daily surgery schedule, suppose that 1st patient needs to be rewarded to specialist, (discharged note eye specialist), admin removing second scheduled appointment for the day, admin checks turnover for the last month.


## Test 4 : (DONE)
Ms Lis Brown (patient ), cancels her appointment with mr first (doctor) and books new appointment with the nurse. admin list all NHS patients. admin removes Mr hesitant's from patient's list. attempt to access nurse dashbaord without login. 

## Test 5: (DONE)
- let an existing patient book appoitnemnt with dr First (doctor) on friday afternoon. dr first hold surgery with patient and issue prescription and invoice. let patient pay the bill. admin decides to change the fee for 10min surgery applicable to all patients.


Needs to be done : 
=> description in discharge patient 
* appointment update 

* add date of birth for patient (Done by S ) / doctor  DONE / nurse DONE
* Patient book appointment with nurse  (ayan) (DONE)
* CSS needs to be done and fully finished (ayan)
* get nurse invoice to pay (deon & andrew)
* patient request a repeated prescription from doctor (deon )
* doctor leave a comment for admin & patient (andrew)
* admin check turnover (deon or/ andrew)
* patient cancel appointment and book new one (S) (done)
* doctor issue prescription (deon ) 
* admin decide to change the fee for 10 min surgery applicable to all types of patients  (deon or/ andrew)

CSS to change (ayan): 
 
1. background colour : navy-blue, (in all website)
2. h1 : make it 26px, h2: 16 px. 
3. buttons : green (login), red (sign in)
4. Book now button in home page h1, center in white 
5. align the tables in the in all dashbaords (admin/doctor/nurse)
6. all border-radius : 15px
7. home page background picture (choose a picture of a hospital care)
8. nav bar (white) and make sure the navbar is the same everywhere
9. users card in the home page (sandra)
