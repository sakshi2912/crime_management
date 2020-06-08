#!/usr/bin/env python
# coding: utf-8

# In[1]:


import psycopg2

    
try:
    connection = psycopg2.connect(user = "postgres",
                                  password = "q1w2e3",
                                  host = "localhost",
                                  port = "5432",
                                  database = "CrimeRecord")
    cursor = connection.cursor()
    
except (Exception, psycopg2.DatabaseError) as error :
    print ("Error", error)
    
finally:

    
    
    def update_acc():
        

        cursor = connection.cursor()
    
        
        f_id = input("Enter the FIR ID to update details : ")
        a_name= input("Accused Name : ")
        ad_no = input("Aadhar Number : ")
        a_contact = input("Accused contact : ")
        a_address = input("Accused address : ")
        a_age = input("Accused age : ")
        a_gender = input("Accused gender : ")
        a_status = input("Accused status : ")
        a_alias =input("Accused alias : ")
        a_identification = input("Accused identfication : ")

        query3=''' 
        CREATE TEMP TABLE acc_temp AS (SELECT a_id from accused WHERE ad_no = %s);
        CREATE TEMP TABLE old_acc AS (SELECT a_id from fir where f_id = %s);
        '''
        query4 =''' DO $$
        BEGIN 
        IF (SELECT COUNT(a_id) FROM acc_temp)=1 
        THEN 
        UPDATE fir SET a_id = (SELECT a_id FROM acc_temp) WHERE f_id = %s;
        DELETE FROM accused where a_id = (SELECT a_id from old_acc);
        END IF; 
        IF(SELECT COUNT(a_id) FROM acc_temp)=0
        THEN
        UPDATE accused SET 
        a_name=%s, 
        a_contact=%s ,
        a_address=%s ,
        a_age=%s, 
        a_gender=%s,
        ad_no = %s ,
        a_status=%s, 
        a_alias=%s, 
        a_identification=%s 
        WHERE a_id = (SELECT a_id from fir WHERE f_id=%s);
        END IF;
        END $$;
        '''

        cursor.execute(query3,(ad_no,f_id))
        cursor.execute(query4,(f_id,a_name,a_contact,a_address,a_age,a_gender,ad_no,a_status ,a_alias,a_identification,f_id))
        connection.commit()
        print("Updated Accused Details")

    def update_vic():

        cursor = connection.cursor()
    
        
        f_id = input("Enter the FIR ID to update details : ")
        v_name= input("Victim Name : ")
        v_contact = input("Victim contact : ")
        v_address = input("Victim address : ")
        v_age = input("Victim age : ")
        v_gender = input("Victim gender : ")
        

        query2='''
        CREATE TEMP TABLE vic_temp AS 
        (
        SELECT v_id from victim WHERE (v_name=%s AND v_contact=%s AND v_address=%s AND v_age=%s AND v_gender=%s)
        );
        CREATE TEMP TABLE old_vic AS (SELECT v_id from fir where f_id = %s);

        '''
        query3 ='''
        DO $$ 
        BEGIN 
        IF (SELECT COUNT(v_id) FROM vic_temp)=1 
        THEN 
        UPDATE fir SET v_id = (SELECT v_id FROM vic_temp) WHERE f_id = %s;  
        DELETE FROM victim WHERE v_id=(SELECT v_id from old_vic);
        END IF; 
        IF (SELECT COUNT(v_id) FROM vic_temp)=0
        THEN
        UPDATE victim SET 
        v_name=%s, 
        v_contact=%s ,
        v_address=%s ,
        v_age=%s, 
        v_gender=%s 
        WHERE v_id = (SELECT v_id from fir WHERE f_id=%s);
        END IF;
        END $$;

        '''

        cursor.execute(query2,(v_name,v_contact,v_address,v_age,v_gender,f_id))
        cursor.execute(query3,(f_id,v_name,v_contact,v_address,v_age,v_gender,f_id))
        connection.commit()
        print("Updated Victim Details ")
        
        
    def file_fir():
        

        cursor = connection.cursor()
    
        
        p_name=input("Enter your name:")
        p_contact = input("Phone no:")
        p_address =input("Address:")
        p_age= input("Age:")
        p_gender = input("Gender [M/F]")
        i_date = input("Incident date")
        i_time = input("Incident time")
        i_place = input("Incident place")
        crime = input("Crime:")
        l_place=input("Lodge place:")

        query1 = "INSERT INTO petitioner(p_name,p_contact,p_address,p_age,p_gender) VALUES (%s,%s,%s,%s,%s)"
        cursor.execute(query1,(p_name,p_contact,p_address,p_age,p_gender))
        v_gender = input("Victim gender")
        a_gender = input("Accused gender")

        query2 = "INSERT INTO victim(v_gender) VALUES (%s)"
        query3 = "INSERT INTO accused(a_gender) VALUES (%s)"
        query4 = "SELECT MAX(v_id) from victim "
        query5 = "SELECT MAX(a_id) from accused"
        query6 = "INSERT INTO FIR (v_id,l_place,i_place,i_date,i_time,p_name,p_contact,a_id,crime) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        query7 = "SELECT MAX(f_id) FROM FIR"

        cursor.execute(query2,(v_gender,))
        cursor.execute(query3,(a_gender,))

        cursor.execute(query4)
        vid = cursor.fetchall()
        for i in vid:
            v_id = i[0]

        cursor.execute(query5)
        aid = cursor.fetchall()
        for i in aid:
            a_id = i[0]

        cursor.execute(query6,(v_id,l_place,i_place,i_date,i_time,p_name,p_contact,a_id,crime))

        cursor.execute(query7)
        fid = cursor.fetchall()
        for i in fid:
            f_id = i[0]


        query8 = "INSERT INTO case_fir(f_id) VALUES(%s)"
        cursor.execute(query8,(f_id,))

        query9 = "SELECT MAX(c_id) from case_fir"
        cursor.execute(query9)
        cid = cursor.fetchall()
        for i in cid:
            c_id = i[0]


        query10= "INSERT INTO case_details(c_id) VALUES(%s)"
        cursor.execute(query10,(c_id,))
        
        print("\n\nYour FIR ID :") 
        print(f_id)
        print("\n Your CASE ID") 
        print(c_id)
    
        connection.commit()
    
    def update_case():
        
        cursor = connection.cursor()
        c_id = input("Enter CASE ID ")
        c_description= input("Case description")
        c_status = input("Case_status")
        o_id = input("Officer ID")
        query1 = "UPDATE case_details SET c_description = %s,c_status =%s, o_id = %s where c_id = %s"
        cursor.execute(query1,(c_description,c_status,o_id,c_id))
        
        connection.commit()
    
    while(1):
        value=input('''
        CRIME RECORD MANAGEMENT 
        
        1. File an FIR
        2. Update details
        0. Exit\n\n''')

        if value=="1":
            file_fir()

        elif value=="2":
            choice = input('''
            a. Accused
            b. Victim
            c. Case Details
            0. Exit\n\n''')

            if choice=="a":
                update_acc()

            elif choice=="b":
                update_vic()
            
            elif choice=="c":
                update_case()

            elif value=="0":
                connection.commit()
                exit(0)

        else:
            if(connection):
                connection.commit()
                cursor.close()
            exit(0)         

    


# In[ ]:





# In[ ]:




