from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3

#Widget Functions
def submit():
    #Connecting to the database
    conn = sqlite3.connect("mycontacts.db")
    c = conn.cursor()

    '''
    c.execute("""CREATE TABLE contacts(
        firstname text,
        surname text,
        country_code integer,
        phone_number integer,
        city text,
        relationship text
    )""")
    '''
    
    #INSERTING DETAILS INTO CONTACTS TABLE
    c.execute("INSERT INTO contacts VALUES(:fname, :lname, :code, :phone, :city, :relationship)", {
        'fname': fname_entry.get(),
        'lname': lname_entry.get(),
        'code': code_entry.get(),
        'phone': phone_entry.get(),
        'city': city_entry.get(),
        'relationship': relationship_entry.get()
    })

    fname_entry.delete(0, END)
    lname_entry.delete(0, END)
    code_entry.delete(0, END)
    phone_entry.delete(0, END)
    city_entry.delete(0, END)
    relationship_entry.delete(0, END)

    conn.commit()
    conn.close


def show_details():
    #Connecting to the database
    conn = sqlite3.connect("mycontacts.db")
    c = conn.cursor()

    c.execute("SELECT *, oid FROM contacts")
    results = c.fetchall()

    #Displaying Results on Screen
    contact_details = ""
    for result in results:
        contact_details += str(result[0]) + " " + str(result[1]) + " " + str(result[2]) +" "+ str(result[3])+ " "+ "\t"+ str(result[6]) + "\n"
    
    #result_details = Label(root, text=contact_details)
    #result_details.grid(row=8, column=1)

    variable = StringVar(root)
    variable.set('Click Here')

    drop = OptionMenu(root, variable, *results)
    drop.config(width=50, font=('Helvetica', 12))
    drop.grid(row=8, column=1, padx=10)

    conn.commit()
    conn.close

def delete():
    #Deleting Record from database
    conn = sqlite3.connect("mycontacts.db")
    c = conn.cursor()

    answer = messagebox.askquestion("Delete Verification", "Are You Sure?")

    if answer == 'yes':
        c.execute('DELETE FROM contacts WHERE oid=' + select_entry.get())  
        select_entry.delete(0, END)

    conn.commit()
    conn.close


def save_updates():
    conn = sqlite3.connect("mycontacts.db")
    c = conn.cursor()

    #Updating contacts into database
    selected_id = select_entry.get()
    c.execute("""UPDATE contacts SET
        firstname = :fname,
        surname = :lname,
        country_code = :code,
        phone_number = :phone,
        city = :city,
        relationship = :relationship
        
        WHERE oid = :oid""", 
        {
            'fname': fname_entryEdit.get(),
            'lname': lname_entryEdit.get(),
            'code': code_entryEdit.get(),
            'phone': phone_entryEdit.get(),
            'city': city_entryEdit.get(),
            'relationship': relationship_entryEdit.get(),
            'oid': selected_id
        })

    conn.commit()
    conn.close

    update_root.destroy()

def update():
    try:
        global update_root
        update_root = Toplevel(root)
        update_root.title("Update Contact")
        global fname_entryEdit
        global lname_entryEdit
        global code_entryEdit
        global phone_entryEdit
        global city_entryEdit
        global relationship_entryEdit

        conn = sqlite3.connect("mycontacts.db")
        c = conn.cursor()

        #Querying all contacts table records
        entered_id = select_entry.get()

        c.execute("SELECT * FROM contacts WHERE oid=" + entered_id)
        records = c.fetchall()

        #Label Widgets
        f_nameEdit = Label(update_root, text='First Name: ')
        f_nameEdit.grid(row=0, column=0)
        l_nameEdit = Label(update_root, text='Surname: ')
        l_nameEdit.grid(row=1, column=0)
        country_codeEdit = Label(update_root, text='Country Code: ')
        country_codeEdit.grid(row=2, column=0)
        phone_numberEdit = Label(update_root, text='Phone Number: ')
        phone_numberEdit.grid(row=3, column=0)
        cityEdit = Label(update_root, text='City: ')
        cityEdit.grid(row=4, column=0)
        relationshipEdit = Label(update_root, text='Relationship: ')
        relationshipEdit.grid(row=5, column=0)

        #Entry Widgets
        fname_entryEdit = Entry(update_root, width=35)
        fname_entryEdit.grid(row=0, column=1, padx=15, pady=5)
        lname_entryEdit = Entry(update_root, width=35)
        lname_entryEdit.grid(row=1, column=1, padx=15, pady=5)
        code_entryEdit = Entry(update_root, width=35)
        code_entryEdit.grid(row=2, column=1, padx=15, pady=5)
        phone_entryEdit = Entry(update_root, width=35)
        phone_entryEdit.grid(row=3, column=1, padx=15, pady=5)
        city_entryEdit = Entry(update_root, width=35)
        city_entryEdit.grid(row=4, column=1, padx=15, pady=5)
        relationship_entryEdit = Entry(update_root, width=35)
        relationship_entryEdit.grid(row=5, column=1, padx=15, pady=5)
    

        #Button Widget
        save_btn = Button(update_root, text="Save Updates", command=save_updates)
        save_btn.grid(row=6, column=1, columnspan=2, padx=15, pady=5)

        for record in records:
            fname_entryEdit.insert(0, record[0])
            lname_entryEdit.insert(0, record[1])
            code_entryEdit.insert(0, record[2])
            phone_entryEdit.insert(0, record[3])
            city_entryEdit.insert(0, record[4])
            relationship_entryEdit.insert(0, record[5])

        conn.commit()
        conn.close

    except:
        update_root.destroy()
        messagebox.showerror("Invalid ID", "Please Enter Record ID first!")



root = Tk()
root.title("myContactsKeeper")
root.config(background='#808080')
root.geometry('650x460')
#root.iconbitmap('phonebook.ico')

#Label Widgets
f_name = ttk.Label(root, text='First Name: ')
f_name.grid(row=0, column=0,  pady=(10, 0))
l_name = ttk.Label(root, text='Surname: ')
l_name.grid(row=1, column=0)
country_code = ttk.Label(root, text='Country Code: ')
country_code.grid(row=2, column=0)
phone_number = ttk.Label(root, text='Phone Number: ')
phone_number.grid(row=3, column=0)
city = ttk.Label(root, text='City: ')
city.grid(row=4, column=0)
relationship = ttk.Label(root, text='Relationship: ')
relationship.grid(row=5, column=0)
select = ttk.Label(root, text='Enter ID: ')
select.grid(row=9, column=0)

#Entry Widgets
fname_entry = Entry(root, width=40, bd=2)
fname_entry.grid(row=0, column=1, padx=55, pady=(10, 5))
lname_entry = Entry(root, width=40, bd=2)
lname_entry.grid(row=1, column=1, padx=55, pady=5)
code_entry = Entry(root, width=40, bd=2)
code_entry.grid(row=2, column=1, padx=55, pady=5)
phone_entry = Entry(root, width=40, bd=2)
phone_entry.grid(row=3, column=1, padx=55, pady=5)
city_entry = Entry(root, width=40, bd=2)
city_entry.grid(row=4, column=1, padx=55, pady=5)
relationship_entry = Entry(root, width=40, bd=2)
relationship_entry.grid(row=5, column=1, padx=55, pady=5)
select_entry = Entry(root, width=40, bd=2)
select_entry.grid(row=9, column=1, padx=55, pady=5)

#Button Widget
submit_btn = Button(root, text="Submit", command=submit)
submit_btn.grid(row=6, column=1, columnspan=2, padx=55, pady=5)

query_btn = Button(root, text=" Show Details ", command=show_details)
query_btn.grid(row=7, column=1, columnspan=2, padx=55, pady=5, ipadx=25)

delete_btn = Button(root, text="Delete Record", command=delete)
delete_btn.grid(row=10, column=1, columnspan=2, padx=55, pady=5, ipadx=40)

update_btn = Button(root, text="Update Record", command=update)
update_btn.grid(row=11, column=1, columnspan=2, padx=55, pady=(5, 10), ipadx=80)

root.mainloop()