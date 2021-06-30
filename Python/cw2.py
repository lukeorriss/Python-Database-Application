import psycopg2
import getpass
import sys, os

class COLOR:
    GREEN = '\033[92m'
    RED = '\033[91m'
    END = '\033[0m'

green = COLOR.GREEN
red = COLOR.RED
e = COLOR.END

pw = getpass.getpass("Password for xaw17xdu: ")

def getConn():
    # pwFile = open("pw.txt", "r")
    # pw = pwFile.read()
    # pwFile.close()
    conn = psycopg2.connect(
            host = "cmpstudb-01.cmp.uea.ac.uk",
            database = "xaw17xdu",
            user = "xaw17xdu",
            password = pw)
    os.system('clear')
    print(green + "\n### Successfully Connected to database ###\n" + e)
    return conn

def clearOutput():
    with open("output.txt", "w") as clearfile:
        clearfile.write("")

def writeOutput(output):
    with open("output.txt", "a") as myfile:
        myfile.write(output)
    
try:
    conn = None
    conn = getConn()
    cur = conn.cursor()
    cur.execute("SET SEARCH_PATH TO pirean;")
    f = open("input.txt", "r")
    
    for l in f:
        
        if (l[0] == "A"): # Add data into spectator
            try: 
                raw = l.split(" ",1)
                data = raw[1].split(", ")
                sql = sql = "INSERT INTO spectator VALUES ('{}'".format(data[0]) + ", '{}'".format(data[1]) + ", '{}'".format(data[2]) + ");"
                cur.execute(sql)
                cur.execute("SELECT * FROM spectator;")
                conn.commit()
                rows = cur.fetchall()
                clearOutput()
                print(green + "Current Spectators" + e)
                for row in rows: 
                    for item in row:
                        print(item, ",  ", end='')
                        s = str(item) + "\n"
                        writeOutput(s)
                    print()
                print()
                    
            except:
                print(red + "Cannot add data into spectator. Do they aleady exist? Use 'S <sno>' to view information about a spectator.\n" + e)
                break

        elif (l[0] == "B"): # Add data into event
            try:
                raw = l.split(" ",1)
                data = raw[1].split(", ")
                sql = "INSERT INTO event VALUES ('{}'".format(data[0]) + ", '{}'".format(data[1]) + ", '{}'".format(data[2])+ ", '{}'".format(data[3])+ ", '{}'".format(data[4])+ ", '{}'".format(data[5]) + ");"
                cur.execute(sql)
                cur.execute("SELECT * FROM event;") # Change this for the cool code with cancelled.
                conn.commit()
                rows = cur.fetchall()
                clearOutput()
                print(green + "Successfully Inserted Data into Spectator" + e)
                for row in rows: 
                    for item in row:
                        print(item, ", ", end='')
                        s = str(item) + ", \n"
                        writeOutput(s)
                    print()
                print()
            except:
                print(red + "Event already exists." + e)
                break
        
        
           

        elif (l[0] == "C"): # Delete from spectator
            try:
                raw = l.split(" ",1)
                data = raw[1].split(", ")
                sql = "UPDATE cancel SET sno = null WHERE sno = '{}'".format(data[0]) + "; update ticket set sno = null where sno = '{}'".format(data[0]) + "; delete from spectator where sno = '{}'".format(data[0]) + ";"
                cur.execute(sql)
                cur.execute("SELECT * FROM spectator;") 
                conn.commit()
                rows = cur.fetchall()
                clearOutput()
                print(green + "Spectator " + data[0] + " removed and all tickets returned as 'null'." + e)
                for row in rows: 
                    for item in row:
                        print(item, ", ", end='')
                        s = str(item) + " \n"
                        writeOutput(s)
                    print()
                print()
            except:
                print(red + "Cannot remove spectator " + data[0] + ". Do they have any 'active' tickets?" + e)
                break


        elif (l[0] == "D"): # Cancel Event
            try:
                raw = l.split(" ",1)
                data = raw[1].split(", ")
                sql = "insert into cancel select * from ticket t where t.ecode = '{}'".format(data[0]) + ";"
                cur.execute(sql)
                cur.execute("SELECT c.ecode, c.cdate, c.cuser, CASE WHEN c.ecode IS NOT null THEN 'cancelled' ELSE 'valid' END AS status FROM cancel c ORDER BY c.cdate DESC;")
                conn.commit()
                rows = cur.fetchall()
                clearOutput()
                print(green + "ALL CANCELLED EVENTS" + e)
                for row in rows: 
                    for item in row:
                        print(item, ", ", end='')
                        s = str(item) + ", \n"
                        writeOutput(s)
                    print()
                print()
            except:
                print(red + "Cannot delete event. Are there any 'active' tickets?" + e)
        
        elif (l[0] == "d"): # Show all data from event without inserting.
            try:
                raw = l.split(" ",1)
                data = raw[1].split(", ")
                sql = "SELECT c.ecode, c.cdate, c.cuser, CASE WHEN c.ecode IS NOT null THEN 'cancelled' ELSE 'valid' END AS status FROM cancel c WHERE c.ecode = '{}'".format(data[0]) + " ORDER BY c.cdate DESC;"
                cur.execute(sql)
                conn.commit()
                rows = cur.fetchall()
                clearOutput()
                print(green + "Check Cancelled Events" + e)
                for row in rows: 
                    for item in row:
                        print(item, ",  ", end='')
                        s = str(item) + ", \n"
                        writeOutput(s)
                    print()
                print()
            except:
                print(red + "Could not fetch cancelled data. Specify event number.\n" + e)
        
        elif (l[0] == "o"): # Show all data from event without inserting.
            try:
                sql = "SELECT t.tno, s.sname, e.ecode, CASE WHEN c.tno IS NOT null THEN 'cancelled' ELSE 'valid' END AS status FROM ticket t LEFT JOIN cancel c ON t.tno = c.tno INNER JOIN spectator s ON t.sno = s.sno INNER JOIN event e ON t.ecode = e.ecode ORDER BY t.tno ASC;"
                cur.execute(sql)
                conn.commit()
                rows = cur.fetchall()
                clearOutput()
                print(green + "Check All Cancelled Events" + e)
                for row in rows: 
                    for item in row:
                        print(item, ",  ", end='')
                        s = str(item) + ", \n"
                        writeOutput(s)
                    print()
                print()
            except:
                print(red + "Could not fetch cancelled data.\n" + e)


        elif (l[0] == "E"): # Issue a ticket
            try:
                raw = l.split(" ",1)
                data = raw[1].split(", ")
                sql = "INSERT INTO ticket VALUES ('{}'".format(data[0]) + ", '{}'".format(data[1]) + ", '{}'".format(data[2]) + ");"
                cur.execute(sql)
                cur.execute("SELECT * FROM ticket;")
                conn.commit()
                rows = cur.fetchall()
                clearOutput()
                print(green + "Successfully Created Ticket" + e)
                for row in rows: 
                    for item in row:
                        print(item, ", ", end='')
                        s = str(item) + ", \n"
                        writeOutput(s)
                    print()
                print()
            except Exception as er:
                print(red + str(er) + e)
                
        
        elif (l[0] == "e"): # Show ticket information
            try:
                raw = l.split(" ",1)
                data = raw[1].split(", ")
                sql = "SELECT * FROM ticket WHERE tno = '{}'".format(data[0]) + ";"
                cur.execute(sql)
                conn.commit()
                rows = cur.fetchall()
                clearOutput()
                print(green + "Showing Ticket {}".format(data[0]) + " Info" + e)
                for row in rows: 
                    for item in row:
                        print(item, ", ", end='')
                        s = str(item) + ", \n"
                        writeOutput(s)
                    print()
                print()
            except:
                print(red + "Cannot Issue Ticket. Does spectator already have a ticket?\nIf not, check spectator exists and event is not cancelled.\n" + e)
                break


        elif (l[0] == "P"): # Table for number of spectators visiting a location for day
            sql = "SELECT e.edate, e.elocation, COUNT (e.elocation) AS attending FROM event e LEFT JOIN ticket t ON e.ecode = t.ecode GROUP BY edate, elocation ORDER BY elocation ASC;"
            cur.execute(sql)
            conn.commit()
            rows = cur.fetchall()
            clearOutput()
            print(green + "Spectators that Could Travel to a Location" + e)
            for row in rows: 
                for item in row:
                    print(item, ", ", end='')
                    s = str(item) + ", \n"
                    writeOutput(s)
                print()
            print()
       
            
        elif (l[0] == "Q"): # Same as P but order by description no location
            sql2 = "SELECT e.edesc, COUNT (e.edesc) AS attending FROM event e LEFT JOIN ticket t ON e.ecode = t.ecode GROUP BY e.ecode ORDER BY edesc ASC;"
            clearOutput()
            cur.execute(sql2)
            rows = cur.fetchall()
            print(green + "Spectators attending an event" + e)
            for row in rows: 
                for item in row:
                    print(item, ", ", end='')
                    s = str(item) + ", \n"
                    writeOutput(s)
                print()
            print()


        elif (l[0] == "R"): # Table showing number of tickets for each event code
            sql = "SELECT e.ecode, COUNT (e.ecode) AS tickets_sold FROM event e LEFT JOIN ticket t ON e.ecode = t.ecode GROUP BY e.ecode ORDER BY ecode ASC;"
            cur.execute(sql) # Change this for the cool code with cancelled.
            conn.commit()
            rows = cur.fetchall()
            clearOutput()
            print(green + "Total tickets for each event" + e)
            for row in rows: 
                for item in row:
                    print(item, "  ", end='')
                    s = str(item) + ", \n"
                    writeOutput(s)
                print()
            print()


        elif (l[0] == "S"): # Spectator Itinerary
            try:
                raw = l.split(" ",1)
                data = raw[1].split(", ")
                sql = "SELECT s.sname, e.edate, e.etime, e.elocation, e.edesc FROM spectator s JOIN ticket t ON s.sno = t.sno JOIN event e ON e.ecode = t.ecode WHERE s.sno = '{}'".format(data[0]) + " ORDER BY e.etime ASC;"
                cur.execute(sql)
                conn.commit()
                rows = cur.fetchall()
                clearOutput()
                print(green + "Spectator " + data[0] + " Itinerary" + e)
                for row in rows: 
                    for item in row:
                        print(item, ", ", end='')
                        s = str(item) + ", \n"
                        writeOutput(s)
                    print()
                print()
            except:
                print(red + "\nYou must specify a spectator number. Try 'S <sno>'.\n" + e)


        elif (l[0] == "s"): # All spectators Itineraries
            sql = "SELECT s.sname, e.edate, e.etime, e.elocation, e.edesc FROM spectator s JOIN ticket t ON s.sno = t.sno JOIN event e ON e.ecode = t.ecode ORDER BY s.sname, e.etime asc;"
            cur.execute(sql)
            conn.commit()
            rows = cur.fetchall()
            clearOutput()
            for row in rows: 
                for item in row:
                    print(item, ", ", end='')
                    s = str(item) + ", \n"
                    writeOutput(s)
                print()
            print()

        elif (l[0] == "T"): # Display name of spectator, event code, whether is cancelled or not
            raw = l.split(" ",1)
            data = raw[1].split(", ")
            sql = "SELECT t.tno, s.sname, e.ecode, CASE WHEN c.tno IS NOT null THEN 'cancelled' ELSE 'active' END AS status FROM ticket t LEFT JOIN cancel c ON t.tno = c.tno INNER JOIN spectator s ON t.sno = s.sno INNER JOIN event e ON t.ecode = e.ecode WHERE t.tno = '{}'".format(data[0]) + " LIMIT 1;"
            cur.execute(sql)
            conn.commit()
            rows = cur.fetchall()
            clearOutput()
            print(green + "Status of ticket: " + data[0] + "." + e)
            for row in rows: 
                for item in row:
                    print(item, ", ", end='')
                    s = str(item) + ", \n"
                    writeOutput(s)
                print()
            print()


        elif (l[0] == "V"): # View all cancelled events
            raw = l.split(" ",1)
            data = raw[1].split(", ")
            sql = "SELECT t.tno, s.sname, c.ecode, CASE WHEN t.ecode = c.ecode THEN 'cancelled' ELSE 'active' END AS status FROM ticket t, spectator s, cancel c where t.ecode = '{}'".format(data[0]) + " AND s.sno = t.sno AND t.ecode = c.ecode AND c.tno = t.tno;"
            cur.execute(sql)
            conn.commit()
            rows = cur.fetchall()
            clearOutput()
            print(green + "View all ticket details for event: " + data[0] + "." + e)
            for row in rows: 
                for item in row:
                    print(item, ", ", end='')
                    s = str(item) + ", \n"
                    writeOutput(s)
                print()
            print()

            
        elif (l[0] == "X"):  # Disconnect from database
            clearOutput()
            conn.close()
            print(red + "\nShutting down server..." + e)
            print(red + "Disconnected." + e)
            writeOutput("\n\nSuccessfully disconnected from database.")
            sys.exit()
        
        
        elif (l[0] == "Z"): # Reset database to empty tables
            print(red + "WARNING!\n")
            print("This will remove all data from all of the tables.\nAre you sure you want to continue? <y/any other key to cancel>" + e)
            check = input("> ")
            if check.lower().strip() == "y":
                try:
                    print(red + "\nResetting Database Tables" + e)
                    cur.execute("DELETE FROM cancel; DELETE FROM ticket; DELETE FROM spectator; DELETE FROM event;")
                    conn.commit()
                    clearOutput()
                    s = "All data has been removed from pirean."
                    writeOutput(s)
                    print(red + "Database Reset." + e)
                except:
                    print(red + "Unable to reset database. Delete in C>T>S>E.")
            else:
                print("\nNo changes have been made.")
                break


        else:
            print(red + "\nInvalid Task Assignment." + e)


except Exception as e:
    print(e)

            
        