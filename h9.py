#!C:\Users\Taylor\AppData\Local\Microsoft\WindowsApps\python.exe
import cgi
import cgitb
import pymysql
cgitb.enable()

def db() :
    return {'user':'root', 'password':'', 'host':'localhost', 'database':'swim'}

def home(cursor) :
    print('<h3>Please select from the following meets:</h3>')
    print("<ul>")  
    query = '''
    select meet.MeetID, meet.Title, venue.Name, venue.Address
    from meet inner join venue using (VenueID)
    order by meet.MeetID, venue.VenueID;
    '''
    x = 1
    cursor.execute(query)
    pmid = 0  
    for (mMeetID, mTitle, vName, vAddress) in cursor:
        if (pmid != mMeetID):
            if (pmid != 0): 
                print('</li>')
            pmid = mMeetID
            print('<li>')
            hrefTitle = "(" + str(x) + "): " + mTitle + ":"
            print("<a href=?mID=" + str(mMeetID) + ">" + hrefTitle + "</a>")
            print('<t> at ' + vName + ' (address: ' + vAddress + ').</t>')
            x += 1
    print("</ul>")
    quit()
    return

def meets(cursor,mID) :
    x = 1
    query = '''
    select venue.Name,event.EventId,meet.MeetId,meet.Title,meet.Date,meet.StartTime,meet.EndTime,event.Title,
    event.StartTime,event.EndTime,count(1) as Participants from venue
    join meet on venue.VenueId = meet.VenueId
    right join event on meet.MeetId = event.MeetId
    right join participation on event.EventId = participation.EventId
    where meet.MeetId = %s group by event.Title order by event.EventId asc;
    '''
    cursor.execute(query, (int(mID),))
    peid = 0 
    for (vName,eEventID, mMeetID, mTitle, mDate, mStartTime, mEndTime, eTitle, eStartTime, eEndTime, Participants) in cursor:
        if (x == 1) :
            print("<h3>Meet #" + str(mID) + " " + mTitle + "<br></h3>")
            print("<t>Venue: " + vName + "<br></t>")
            print("<t>Date/time: " + str(mDate) + ": " + str(mStartTime) + " to " + str(mEndTime) + "<br><br>Events:<br></t>")
            print("<ul>") 
        if(peid != str(eEventID)) :
            if (peid != 0) :
                print('</li>')
            peid = eEventID
            print("<li>")
            href = "<a href=?eID=" + str(eEventID) + ">" + eTitle + "</a>"
            eventTime = str(eStartTime) + " to " + str(eEndTime)
            print(str(x) + ". " + href + ": " + eventTime + "; with " + str(Participants) + " participants.")
            x += 1
    print("</ul>")
    quit()
    return

def events(cursor,eID) :

    z = 1
    query = '''
    select event.EventId,swimmer.FName,swimmer.LName from event
    right join participation on participation.EventId = event.EventId
    join swimmer on swimmer.SwimmerId = participation.SwimmerId
    where event.EventId = %s order by LName asc,FName asc;
    '''
    cursor.execute(query, (int(eID),))
    peid = 0 
    for (eEventID, sFName, sLName) in cursor:
        if (z == 1) :
            print("<h3>Participants in Event #" + str(eID) + "<br></h3>")
            print("<ul>")
        if(peid != str(eEventID)) :
            if (peid != 0) :
                print('</li>')
            peid = eEventID
            print("<li>")
            print(str(z) + ". " + sFName +  " " + sLName + ".")
            z += 1
    print("</ul>")
    quit()
    return

def main():
    dbLoginInfo = db()
    coredb = pymysql.connect(user=dbLoginInfo['user'], password=dbLoginInfo['password'],
                           host=dbLoginInfo['host'], database=dbLoginInfo['database'])
    try:
        with coredb.cursor() as cursor:
            print("Content-Type: text/html;charset=utf-8\n")
            print("<html>\n<head></head>\n<body>")
            form = cgi.FieldStorage()
            mID = form.getfirst('mID')
            eID = form.getfirst('eID')
            if mID is None and eID is None: 
                home(cursor)
            elif eID is None:   
                meets(cursor, mID)
            else :
                events(cursor,eID)
            print("</body>\</html>")

    finally:
        coredb.close()

main()
